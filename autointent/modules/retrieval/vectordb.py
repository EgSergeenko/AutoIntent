from functools import partial
from typing import Callable

import numpy as np
from chromadb import Collection

from ...context import (
    Context,
    multiclass_metadata_as_labels,
    multilabel_metadata_as_labels,
)
from .base import RetrievalModule


class VectorDBModule(RetrievalModule):
    def __init__(self, k: int, model_name: str):
        self.model_name = model_name
        self.k = k

    def fit(self, context: Context):
        self.collection = context.vector_index.create_collection(self.model_name, context.data_handler)

    def score(self, context: Context, metric_fn: Callable) -> tuple[float, str]:
        """
        Return
        ---
        - metric calculated on test set
        - name of embedding model used
        """
        labels_pred = retrieve_candidates(self.collection, self.k, context.data_handler.utterances_test)
        metric_value = metric_fn(context.data_handler.labels_test, labels_pred)
        return metric_value, self.model_name

    def clear_cache(self):
        model = self.collection._embedding_function._model
        model.to(device="cpu")
        del model
        self.collection = None


def retrieve_candidates(
    collection: Collection,
    k: int,
    utterances: list[str],
) -> list[int] | list[list[int]]:
    """
    Return
    ---
    `labels`:
        - multiclass case: np.ndarray of shape (n_samples, n_candidates) with integer labels from `[0,n_classes-1]`
        - multilabel case: np.ndarray of shape (n_samples, n_candidates, n_classes) with binary labels
    """
    n_classes = collection.metadata["n_classes"]
    multilabel = collection.metadata["multilabel"]

    query_res = collection.query(
        query_texts=utterances,
        n_results=k,
        include=["metadatas", "documents", "distances"],  # one can add "embeddings"
    )

    if not multilabel:
        convert = multiclass_metadata_as_labels
    else:
        convert = partial(multilabel_metadata_as_labels, n_classes=n_classes)

    res_labels = np.array([convert(candidates) for candidates in query_res["metadatas"]])
    return res_labels
