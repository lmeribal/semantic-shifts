import torch
from torch import Tensor, nn
from torch.nn import functional as F


def tensor_masking(tensor: Tensor, mask: Tensor, value: float = 0.0) -> Tensor:
    return tensor.masked_fill((~(mask.bool())).unsqueeze(-1), value)


class GlobalMaskedPooling(nn.Module):
    POOLING_TYPES = ("mean", "max")

    def __init__(
        self,
        pooling_type: str = "mean",
        dim: int = 1,
        normalize: bool = False,
        length_scaling: bool = False,
        scaling_square_root: bool = False,
        embedding_masking: bool = True,
    ):
        super().__init__()

        if pooling_type not in self.POOLING_TYPES:
            raise ValueError(
                f"{pooling_type} - is unavailable type."
                f' Available types: {", ".join(self.POOLING_TYPES)}'
            )

        if dim < 0:
            raise ValueError("Dimension (dim parameter) must be greater than zero")

        self.pooling_type = pooling_type
        self.dim = dim

        self.normalize = normalize
        self.length_scaling = length_scaling
        self.scaling_square_root = scaling_square_root

        self.embedding_masking = embedding_masking

        if self.pooling_type == "max":
            self.mask_value = -float("inf")
        else:
            self.mask_value = 0.0

    def forward(self, tensor: Tensor, pad_mask: Tensor) -> Tensor:
        lengths = pad_mask.sum(self.dim).float()

        if self.embedding_masking:
            tensor = tensor_masking(tensor, pad_mask, value=self.mask_value)

        if self.pooling_type == "mean":
            scaling = tensor.size(self.dim) / lengths
        else:
            scaling = torch.ones(tensor.size(0), device=tensor.device)

        if self.length_scaling:
            lengths_factor = lengths
            if self.scaling_square_root:
                lengths_factor = lengths_factor**0.5
            scaling /= lengths_factor

        scaling = scaling.masked_fill(lengths == 0, 1.0).unsqueeze(-1)

        if self.pooling_type == "mean":
            tensor = tensor.mean(self.dim)
        else:
            tensor, _ = tensor.max(self.dim)

        tensor *= scaling

        if self.normalize:
            tensor = F.normalize(tensor)

        return tensor


class ShiftClassifier(torch.nn.Module):
    def __init__(self, model_dim):
        super().__init__()
        self.model_dim = model_dim
        self.classification_head = torch.nn.Linear(self.model_dim * 2, 2)

    def forward(self, source_logits, target_logits):
        logits = torch.cat((source_logits, target_logits), -1)
        return self.classification_head(logits)
