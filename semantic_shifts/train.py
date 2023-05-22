import copy

import numpy as np
import torch
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from tqdm import tqdm

from semantic_shifts.config import EPOCHS


class Trainer:
    def __init__(self, criterion, optimizer, model_device):
        self.criterion = criterion
        self.optimizer = optimizer
        self.model_device = model_device

    def _compute_epoch_metrics(self, epoch_stats_dict):
        epoch_f1 = f1_score(
            epoch_stats_dict["marks"], epoch_stats_dict["preds"], average="macro"
        )
        epoch_rocauc = roc_auc_score(
            epoch_stats_dict["marks"],
            np.array(epoch_stats_dict["probas"])[:, 1],
            average="macro",
        )
        epoch_precision = precision_score(
            epoch_stats_dict["marks"], epoch_stats_dict["preds"], average="macro"
        )
        epoch_recall = recall_score(
            epoch_stats_dict["marks"], epoch_stats_dict["preds"], average="macro"
        )
        return epoch_f1, epoch_rocauc, epoch_precision, epoch_recall

    def _loop(self, classifier, is_training, loader, return_metrics=False):
        epoch_stats_dict = {"losses": [], "marks": [], "probas": [], "preds": []}

        if is_training:
            classifier.eval()
        else:
            classifier.train()

        for meaning_1, meaning_2, mark in loader:
            with torch.set_grad_enabled(mode=is_training):
                output = classifier(
                    meaning_1.to(self.model_device), meaning_2.to(self.model_device)
                ).cpu()

            loss = self.criterion(output, mark)
            epoch_stats_dict["losses"].append(loss.item())
            if return_metrics:
                epoch_stats_dict["marks"].extend(mark)
                epoch_stats_dict["probas"].extend(output.detach().numpy())
                epoch_stats_dict["preds"].extend(output.argmax(1).detach().numpy())

            if is_training:
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

        epoch_loss = np.mean(epoch_stats_dict["losses"])
        if return_metrics:
            (
                epoch_f1,
                epoch_rocauc,
                epoch_precision,
                epoch_recall,
            ) = self._compute_epoch_metrics(epoch_stats_dict)
            return epoch_loss, epoch_f1, epoch_rocauc, epoch_precision, epoch_recall
        return epoch_loss

    def train(self, classifier, train_loader, test_loader, val_loader):
        train_losses = []
        test_losses = []
        best_loss = 1000
        best_model = copy.deepcopy(classifier)

        for _ in tqdm(range(EPOCHS), desc="Training"):
            train_loss = self._loop(
                classifier=classifier,
                is_training=True,
                loader=train_loader,
                return_metrics=False,
            )
            test_loss = self._loop(
                classifier=classifier,
                is_training=False,
                loader=test_loader,
                return_metrics=False,
            )

            train_losses.append(train_loss)
            test_losses.append(test_loss)
            if test_loss < best_loss:
                best_loss = test_loss
                best_model = copy.deepcopy(classifier)

        val_loss, val_f1, val_rocauc, val_precision, val_recall = self._loop(
            classifier=best_model,
            is_training=False,
            loader=val_loader,
            return_metrics=True,
        )
        return best_model, val_loss, val_f1, val_rocauc, val_precision, val_recall
