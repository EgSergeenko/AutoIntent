import itertools as it

import numpy as np
from sentence_transformers import CrossEncoder
from ..base import Context, ScoringModule
from .head_training import CrossEncoderWithLogreg


class DNNCScorer(ScoringModule):
    """
    TODO:
    - think about other cross-encoder settings
    - implement training of cross-encoder with sentence_encoders utils
    - inspect batch size of model.predict?
    """

    def __init__(self, model_name: str, k: int, train_head=False):
        self.model_name = model_name
        self.k = k
        self.train_head = train_head

    def fit(self, context: Context):
        self.model = CrossEncoder(self.model_name, trust_remote_code=True, device=context.device)
        self._collection = context.get_best_collection()

        if self.train_head:
            model = CrossEncoderWithLogreg(self.model)
            model.fit(context.data_handler.utterances_train, context.data_handler.labels_train)
            self.model = model

    def predict(self, utterances: list[str]):
        """
        Return
        ---
        `(n_queries, n_classes)` matrix with zeros everywhere except the class of the best neighbor utterance
        """
        query_res = self._collection.query(
            query_texts=utterances,
            n_results=self.k,
            include=["metadatas", "documents"],  # one can add "embeddings", "distances"
        )

        cross_encoder_scores = self._get_cross_encoder_scores(
            utterances, query_res["documents"]
        )

        labels_pred = [
            [cand["intent_id"] for cand in candidates]
            for candidates in query_res["metadatas"]
        ]

        res = self._build_result(cross_encoder_scores, labels_pred)

        return res

    def _get_cross_encoder_scores(
        self, utterances: list[str], candidates: list[list[str]]
    ):
        """
        Arguments
        ---
        `utterances`: list of query utterances
        `candidates`: for each query, this list contains a list of the k the closest sample utterances (from retrieval module)

        Return
        ---
        for each query, return a list of a corresponding cross encoder scores for the k the closest sample utterances
        """
        assert len(utterances) == len(candidates)

        text_pairs = [
            [[query, cand] for cand in docs]
            for query, docs in zip(utterances, candidates)
        ]

        flattened_text_pairs = list(it.chain.from_iterable(text_pairs))

        assert len(flattened_text_pairs) == len(utterances) * len(candidates[0])

        flattened_cross_encoder_scores = self.model.predict(flattened_text_pairs)
        cross_encoder_scores = [
            flattened_cross_encoder_scores[i : i + self.k]
            for i in range(0, len(flattened_cross_encoder_scores), self.k)
        ]
        return cross_encoder_scores

    def _build_result(self, scores: list[list[float]], labels: list[list[int]]):
        """
        Arguments
        ---
        `scores`: for each query utterance, cross encoder scores of its k closest utterances
        `labels`: corresponding intent labels

        Return
        ---
        `(n_queries, n_classes)` matrix with zeros everywhere except the class of the best neighbor utterance
        """
        scores = np.array(scores)
        labels = np.array(labels)
        n_classes = self._collection.metadata["n_classes"]

        return build_result(scores, labels, n_classes)
    
    def clear_cache(self):
        model = self._collection._embedding_function._model
        model.to(device='cpu')
        del model
        self._collection = None


def build_result(scores: np.ndarray, labels: np.ndarray, n_classes: int):
    res = np.zeros((len(scores), n_classes))
    best_neighbors = np.argmax(scores, axis=1)
    idx_helper = np.arange(len(res))
    best_classes = labels[idx_helper, best_neighbors]
    best_scores = scores[idx_helper, best_neighbors]
    res[idx_helper, best_classes] = best_scores
    return res
