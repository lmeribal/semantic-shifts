import torch
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

from semantic_shifts.config import BATCH_SIZE
from semantic_shifts.model import GlobalMaskedPooling

pooling = GlobalMaskedPooling()


def return_pretrained_loader(loader, model, tokenizer, method_type, is_training=True):
    meaning_1_embs = []
    meaning_2_embs = []
    marks_lst = []
    for meaning_1, meaning_2, mark in tqdm(loader, desc=f"Extract embeddings"):
        if method_type != "muse":
            meaning_1_tokens = tokenizer(
                meaning_1, return_tensors="pt", padding=True
            ).to(model.device)
            meaning_2_tokens = tokenizer(
                meaning_2, return_tensors="pt", padding=True
            ).to(model.device)

            with torch.no_grad():
                meaning_1_model_output = model(
                    meaning_1_tokens.input_ids,
                    attention_mask=meaning_1_tokens.attention_mask,
                )
                meaning_1_logits = pooling(
                    meaning_1_model_output.last_hidden_state,
                    meaning_1_tokens.attention_mask,
                )
                meaning_2_model_output = model(
                    meaning_2_tokens.input_ids,
                    attention_mask=meaning_2_tokens.attention_mask,
                )
                meaning_2_logits = pooling(
                    meaning_2_model_output.last_hidden_state,
                    meaning_2_tokens.attention_mask,
                )
        else:
            meaning_1_logits = model(meaning_1).numpy()
            meaning_2_logits = model(meaning_2).numpy()
        marks_lst.extend(mark)
        meaning_1_embs.extend(meaning_1_logits)
        meaning_2_embs.extend(meaning_2_logits)

    dataset = ShiftDataset(meaning_1_embs, meaning_2_embs, marks_lst)
    loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=is_training)
    return loader


def prepare_data(
    train_data,
    test_data,
    val_data,
    tokenizer,
    model,
    method_type,
):
    train_dataset = ShiftDataset(
        train_data["meaning_1"].to_numpy(),
        train_data["meaning_2"].to_numpy(),
        train_data["mark"].to_numpy(),
    )
    test_dataset = ShiftDataset(
        test_data["meaning_1"].to_numpy(),
        test_data["meaning_2"].to_numpy(),
        test_data["mark"].to_numpy(),
    )
    val_dataset = ShiftDataset(
        val_data["meaning_1"].to_numpy(),
        val_data["meaning_2"].to_numpy(),
        val_data["mark"].to_numpy(),
    )

    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False)
    val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    return (
        return_pretrained_loader(train_dataloader, model, tokenizer, method_type, True),
        return_pretrained_loader(test_dataloader, model, tokenizer, method_type, False),
        return_pretrained_loader(val_dataloader, model, tokenizer, method_type, False),
    )


class ShiftDataset(Dataset):
    def __init__(self, meaning_1, meaning_2, mark):
        self.meaning_1 = meaning_1
        self.meaning_2 = meaning_2
        self.mark = mark

    def __len__(self):
        return len(self.meaning_2)

    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
        return self.meaning_1[idx], self.meaning_2[idx], self.mark[idx]
