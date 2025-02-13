from pprint import pprint


class OptimizationLogs:
    """TODO continous IO with file system (to be able to restore the state of optimization)"""

    def __init__(
        self,
    ):
        self.cache = dict(
            best_assets=dict(
                regexp=None,  # TODO: choose the format
                retrieval=None,  # str, name of best retriever
                scoring=dict(
                    test_scores=None, oos_scores=None
                ),  # dict with values of two np.ndarrays of shape (n_samples, n_classes), from best scorer
                prediction=None,  # np.ndarray of shape (n_samples,), from best predictor
            ),
            metrics=dict(regexp=[], retrieval=[], scoring=[], prediction=[]),
            configs=dict(regexp=[], retrieval=[], scoring=[], prediction=[]),
        )

    def log_module_optimization(
        self,
        node_type: str,
        module_type: str,
        module_config: dict,
        metric_value: float,
        metric_name: str,
        assets,
        verbose=False,
    ):
        """
        Purposes:
        - save optimization results in a text form (hyperparameters and corresponding metrics)
        - update best assets
        """

        # "update leaderboard" if it's a new best metric
        metrics_list = self.cache["metrics"][node_type]
        previous_best = max(metrics_list, default=-float("inf"))
        if metric_value > previous_best:
            self.cache["best_assets"][node_type] = assets

        # logging
        logs = dict(
            module_type=module_type,
            metric_name=metric_name,
            metric_value=metric_value,
            **module_config,
        )
        self.cache["configs"][node_type].append(logs)
        if verbose:
            pprint(logs)
        metrics_list.append(metric_value)

    def get_best_embedder(self):
        return self.cache["best_assets"]["retrieval"]

    def get_best_test_scores(self):
        return self.cache["best_assets"]["scoring"]["test_scores"]

    def get_best_oos_scores(self):
        return self.cache["best_assets"]["scoring"]["oos_scores"]

    def dump(self):
        res = dict(
            metrics=self.cache["metrics"],
            configs=self.cache["configs"],
        )
        return res
