# Semantic shifts
This repository is related to the paper [Computer-assisted detection of typologically relevant semantic shifts in world languages](https://www.dialog-21.ru/media/5898/gruntoviplusrykove036.pdf)

# Data
We have published all the data we used in our experiments:
- [data/dictionaries.gz](https://github.com/lmeribal/semantic-shifts/blob/main/data/dictionaries.gz) is a collection of parsed polysemous words from 75 dictionaries
- [data/dictionaries_training.csv](https://github.com/lmeribal/semantic-shifts/blob/main/data/dictionaries_training.csv) is the annotated collection with over 2'500 polysemous words
- [data/dictionaries_inferenced_mark.gz](https://github.com/lmeribal/semantic-shifts/blob/main/data/dictionaries_inferenced_mark.gz) is the collection of polysemous words with classes that were inferred by the best classifier
- [data/dictionaries_inferenced_clusters.gz](https://github.com/lmeribal/semantic-shifts/blob/main/data/dictionaries_inferenced_clusters.gz) is the collection of realisations with inferred clusters. Only the "good" examples were used for clustering

# ML classifier
## Running training scripts
1. The project requires `Poetry`, so if you don't have it, install it like this:
```bash
make poetry-download
```
2. Download dependencies:
```bash
make install
```
3. Run the project:
```bash
make run
```

## Results
The results of the method evaluation are shown in the table:
| **Method**                              | **Model**                    | **Precision** | **Recall** | **F1**   | **ROC-AUC** |
|-----------------------------------------|------------------------------|---------------|------------|----------|-------------|
| Cosine measure                          | -                            | 0.40          | 0.41       | 0.40     | -           |
| Feature-based                           | -                            | 0.59          | 0.58       | 0.56     | 0.67        |
| Multilingual Universal Sentence Encoder | -                            | 0.65          | 0.63       | 0.62     | 0.71        |
| Frozen LM fine-tuning                   | bert-base-multilingual-cased | 0.62          | 0.60       | 0.59     | 0.64        |
| Frozen LM fine-tuning                   | xlm-roberta-base             | 0.65          | 0.64       | 0.63     | 0.69        |
| Frozen LM fine-tuning                   | xlm-roberta-large            | 0.63          | 0.62       | 0.61     | 0.66        |
| Frozen LM fine-tuning                   | flan-t5-small                | 0.58          | 0.57       | 0.56     | 0.61        |
| Frozen LM fine-tuning                   | flan-t5-base                 | 0.61          | 0.61       | 0.61     | 0.65        |
| Frozen LM fine-tuning                   | flan-t5-large                | 0.61          | 0.59       | 0.59     | 0.65        |
| Frozen LM fine-tuning                   | mt0-small                    | **0.68**      | **0.67**   | **0.67** | **0.74**    |
| Frozen LM fine-tuning                   | mt0-base                     | 0.67          | 0.65       | 0.65     | 0.71        |
| Frozen LM fine-tuning                   | mt0-large                    | 0.65          | 0.64       | 0.63     | 0.71        |

Fine-tuning of the frozen [mt0-small](https://huggingface.co/bigscience/mt0-small) model outperforms all other models and methods.


# Clustering
## Running clustering scripts

## Results
