import importlib.resources as ires
import json
import os

import numpy as np
import yaml

from .. import Context
from ..nodes import (
    Node,
    PredictionNode,
    RegExpNode,
    RetrievalNode,
    ScoringNode,
)
from .utils import NumpyEncoder


class Pipeline:
    available_nodes = {
        "regexp": RegExpNode,
        "retrieval": RetrievalNode,
        "scoring": ScoringNode,
        "prediction": PredictionNode,
    }

    def __init__(self, config_path: os.PathLike, mode: str, verbose: bool):
        # TODO add config validation
        self.config = load_config(config_path, mode)
        self.verbose = verbose

    def optimize(self, context: Context):
        self.context = context
        for node_config in self.config["nodes"]:
            node: Node = self.available_nodes[node_config["node_type"]](
                modules_search_spaces=node_config["modules"], metric=node_config["metric"], verbose=self.verbose
            )
            node.fit(context)
            print("fitted!")

    def dump(self, logs_dir: os.PathLike, run_name: str):
        optimization_results = self.context.optimization_logs.dump()

        # create appropriate directory
        if logs_dir == "":
            logs_dir = os.getcwd()
        logs_dir = os.path.join(logs_dir, run_name)
        if not os.path.exists(logs_dir):
            os.makedirs(logs_dir)

        # dump config and optimization results
        logs_path = os.path.join(logs_dir, "logs.json")
        json.dump(optimization_results, open(logs_path, "w"), indent=4, ensure_ascii=False, cls=NumpyEncoder)
        config_path = os.path.join(logs_dir, "config.yaml")
        yaml.dump(self.config, open(config_path, "w"))

        if self.verbose:
            print(
                make_report(
                    optimization_results, nodes=[node_config["node_type"] for node_config in self.config["nodes"]]
                )
            )

        # dump train and test data splits
        train_data, test_data = self.context.data_handler.dump()
        train_path = os.path.join(logs_dir, "train_data.json")
        test_path = os.path.join(logs_dir, "test_data.json")
        json.dump(train_data, open(train_path, "w"), indent=4, ensure_ascii=False)
        json.dump(test_data, open(test_path, "w"), indent=4, ensure_ascii=False)


def load_config(config_path: os.PathLike, mode: str):
    """load config from the given path or load default config which is distributed along with the autointent package"""
    if config_path != "":
        file = open(config_path)
    else:
        config_name = "default-multilabel-config.yaml" if mode != "multiclass" else "default-multiclass-config.yaml"
        file = ires.files("autointent.datafiles").joinpath(config_name).open()
    return yaml.safe_load(file)


def make_report(logs: dict[str], nodes: list[str]) -> str:
    ids = [np.argmax(logs["metrics"][node]) for node in nodes]
    configs = []
    for i, node in zip(ids, nodes):
        cur_config = logs["configs"][node][i]
        cur_config["metric_value"] = logs["metrics"][node][i]
        configs.append(cur_config)
    messages = [json.dumps(c, indent=4) for c in configs]
    return "\n".join(messages)
