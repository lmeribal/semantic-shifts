import argparse

import pandas as pd
import tensorflow_hub as hub
import tensorflow_text
import torch
from loguru import logger
from scipy.spatial.distance import cosine
from sklearn.metrics import f1_score, precision_score, recall_score
from transformers import AutoModel, AutoTokenizer, MT5EncoderModel, T5EncoderModel
from tabulate import tabulate
from semantic_shifts.config import LEARNING_RATE, AVAILABLE_MODELS_DICT
from semantic_shifts.dataset import prepare_data
from semantic_shifts.model import ShiftClassifier
from semantic_shifts.train import Trainer

if torch.cuda.is_available():
    model_device = torch.device("cuda")
else:
    model_device = torch.device("cpu")

parser = argparse.ArgumentParser(prog="SemanticShifts", description="", epilog="")
parser.add_argument(
    "-m",
    "--method",
    choices=["cosine", "feature", "lm", "muse"],
    help="Classification method",
    required=False,
)
parser.add_argument(
    "-p",
    "--path",
    help="Model name from HuggingFace Hub or path",
    required=False,
)


def load_model(method_type, model_name_or_path):
    if method_type in ("muse", "feature", "cosine"):
        model = hub.load(model_name_or_path)
    elif "mt" in model_name_or_path:
        model = MT5EncoderModel.from_pretrained(model_name_or_path).to(model_device)
    elif "t5" in model_name_or_path:
        model = T5EncoderModel.from_pretrained(model_name_or_path).to(model_device)
    else:
        model = AutoModel.from_pretrained(model_name_or_path).to(model_device)

    tokenizer = None
    if method_type not in ("muse", "cosine", "feature"):
        tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=False)

    return model, tokenizer


def run(method_type, model_name_or_path):
    if method_type in ("muse", "cosine", "feature"):
        model_name_or_path = (
            "https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"
        )
    model, tokenizer = load_model(method_type, model_name_or_path)

    data = pd.read_csv("data/dictionaries_training.csv")
    train_data = data[data["split"] == "train"]
    test_data = data[data["split"] == "test"]
    val_data = data[data["split"] == "val"]

    if "mt" in model_name_or_path:
        emb_size = model.config.d_model
    elif method_type in ("muse", "cosine", "feature"):
        emb_size = 512
    else:
        emb_size = model.config.hidden_size

    val_precision = 0.0
    val_recall = 0.0
    val_f1 = 0.0
    val_rocauc = 0.0

    if method_type in ("lm", "muse"):
        pos_weight = len(train_data[train_data["mark"] == 0]) / len(train_data)
        neg_weight = len(train_data[train_data["mark"] == 1]) / len(train_data)
        class_weight = [neg_weight, pos_weight]
        train_loader, test_loader, val_loader = prepare_data(
            train_data, test_data, val_data, tokenizer, model, method_type
        )

        shift_classifier = ShiftClassifier(emb_size)
        shift_classifier.to(model_device)

        criterion = torch.nn.CrossEntropyLoss(
            weight=torch.Tensor(class_weight), label_smoothing=0.1
        )
        optimizer = torch.optim.Adam(shift_classifier.parameters(), lr=LEARNING_RATE)

        trainer = Trainer(criterion, optimizer, model_device)

        (
            best_model,
            val_loss,
            val_f1,
            val_rocauc,
            val_precision,
            val_recall,
        ) = trainer.train(shift_classifier, train_loader, test_loader, val_loader)
    elif method_type == "feature":
        logger.info(f"Method {method_type} is not implemented yet.")
    elif method_type == "cosine":
        cosine_marks = []
        meaning_1_embeds = model(val_data["meaning_1"])
        meaning_2_embeds = model(val_data["meaning_2"])
        for emb_1, emb_2 in zip(meaning_1_embeds, meaning_2_embeds):
            cosine_marks.append(1 if 1 - cosine(emb_1, emb_2) < 0.5 else 0)
        val_f1 = f1_score(cosine_marks, val_data["mark"], average="macro")
        val_precision = precision_score(cosine_marks, val_data["mark"], average="macro")
        val_recall = recall_score(cosine_marks, val_data["mark"], average="macro")
        val_rocauc = 0.0
    else:
        logger.info(f"Method {method_type} is unknown.")
    return val_precision, val_recall, val_f1, val_rocauc


if __name__ == "__main__":
    args = parser.parse_args()
    method_type = args.method
    model_name_or_path = args.path

    if method_type is None and model_name_or_path is None:
        output_table_dict = {'method_type': [],
                             'model_name': [],
                             'precision': [],
                             'recall': [],
                             'f1': [],
                             'roc-auc': []}
        for method_type, model_name_or_path_lst in AVAILABLE_MODELS_DICT.items():
            for model_name_or_path in model_name_or_path_lst:
                logger.info(f"{method_type=}, {model_name_or_path=}")
                val_precision, val_recall, val_f1, val_rocauc = run(method_type=method_type, model_name_or_path=model_name_or_path)
                output_table_dict['method_type'].append(method_type)
                output_table_dict['model_name'].append(model_name_or_path)
                output_table_dict['precision'].append(round(val_precision, 2))
                output_table_dict['recall'].append(round(val_recall, 2))
                output_table_dict['f1'].append(round(val_f1, 2))
                output_table_dict['roc-auc'].append(round(val_rocauc, 2))
        logger.info('\n' + tabulate(output_table_dict, headers=output_table_dict.keys()))
    else:
        val_precision, val_recall, val_f1, val_rocauc = run(method_type=method_type, model_name_or_path=model_name_or_path)
