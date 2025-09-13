import csv
import itertools
import json
import logging
from multiprocessing import Pool
from pathlib import Path

import numpy as np

from lmentry.constants import (
    RESULTS_DIR, paper_models, get_short_model_name, PREDICTIONS_ROOT_DIR, TASKS_DATA_DIR
)
from lmentry.tasks.lmentry_tasks import all_tasks, core_tasks

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)

def get_language(task_names: str, model_name: str, language_classifier) -> dict:
    # load scored predictions

    for task_name in task_names:
        prediction_path = PREDICTIONS_ROOT_DIR.joinpath(task_name).joinpath(f"{model_name}.json")
        if not prediction_path.exists():
            return dict()
        
        with open(prediction_path) as f_predictions:
            predictions = json.load(f_predictions)

            for id, sample in predictions.items():
                print(id)
                lang_pred = language_classifier.predict(sample["prediction"])
                print(lang_pred)
                exit()
        
