BATCH_SIZE = 32
EPOCHS = 50
LEARNING_RATE = 1e-3
AVAILABLE_MODELS_DICT = {
    "cosine": ["https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"],
    "feature": ["https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"],
    "muse": ["https://tfhub.dev/google/universal-sentence-encoder-multilingual/3"],
    "lm": [
        "bert-base-multilingual-cased",
        # "xlm-roberta-base",
        # "xlm-roberta-large",
        "bigscience/mt0-small",
        # "bigscience/mt0-base",
        # "bigscience/mt0-large",
        "google/flan-t5-small",
        # "google/flan-t5-base",
        # "google/flan-t5-large",
    ],
}
