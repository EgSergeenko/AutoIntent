import numpy as np
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV
from sklearn.multioutput import MultiOutputClassifier

from ...context import multiclass_metadata_as_labels, multilabel_metadata_as_labels
from .base import Context, ScoringModule


class LinearScorer(ScoringModule):
    """
    TODO:
    - implement different modes (incremental learning with SGD and simple learning with LogisticRegression)
    - control n_jobs
    - adjust cv
    - separate the sklearn fit() process and transformers tokenizers process (from vector_index embedding function) to avoid the warnings:
    ```
    huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks...
    To disable this warning, you can either:
        - Avoid using `tokenizers` before the fork if possible
        - Explicitly set the environment variable TOKENIZERS_PARALLELISM=(true | false)
    ```
    """

    def __init__(self, multilabel=False):
        self.multilabel = multilabel

    def fit(self, context: Context):
        collection = context.get_best_collection()
        dataset = collection.get(include=["embeddings", "metadatas"])
        features = dataset["embeddings"]

        if self.multilabel:
            labels = multilabel_metadata_as_labels(dataset["metadatas"], context.n_classes)
            base_clf = LogisticRegression()
            clf = MultiOutputClassifier(base_clf)
        else:
            labels = multiclass_metadata_as_labels(dataset["metadatas"])
            clf = LogisticRegressionCV(cv=3, n_jobs=8)

        clf.fit(features, labels)

        self._clf = clf
        self._emb_func = collection._embedding_function

    def predict(self, utterances: list[str]):
        features = self._emb_func(utterances)
        probas = self._clf.predict_proba(features)
        if self.multilabel:
            probas = np.stack(probas, axis=1)[..., 1]
        return probas

    def clear_cache(self):
        model = self._emb_func._model
        model.to(device="cpu")
        del model
        self.collection = None
