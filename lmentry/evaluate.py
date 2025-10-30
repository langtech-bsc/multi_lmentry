import argparse
import logging
from collections import defaultdict
from pathlib import Path

from lmentry.constants import initialize_variables

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S', level=logging.INFO)


ALL_TASKS = None

def check_for_missing_predictions(predictions_root_dir: Path, all_task_names: set):
    # In English, predictions_root_dir should include exactly 41 directories, each one named after one of the 25
    # "core" tasks + the 16 "argument content robustness" (analysis) tasks. For Spanish and Catalan, 40 
    # directories due to the 15 analysis tasks.
    existing_predictions = defaultdict(set)

    for task_predictions_dir in predictions_root_dir.iterdir():
        if not task_predictions_dir.is_dir():
            continue
        task_name = task_predictions_dir.name
        for model_predictions_path in task_predictions_dir.iterdir():
            model_name = model_predictions_path.stem.replace("_with_metadata", "")
            existing_predictions[model_name].add(task_name)

    missing_predictions = dict()
    for model_name in existing_predictions:
        missing_predictions_for_model = sorted(all_task_names - existing_predictions[model_name])
        missing_predictions[model_name] = missing_predictions_for_model

    return missing_predictions


def eval_main(num_procs):
    from lmentry.analysis.accuracy import score_all_predictions, create_per_task_accuracy_csv, \
    create_per_template_accuracy_csv
    from lmentry.analysis.lmentry_score import create_lmentry_scores_csv
    from lmentry.analysis.robustness import create_robustness_csv, create_argument_order_robustness_csv
    from lmentry.constants import PREDICTIONS_ROOT_DIR, RESULTS_DIR
    from lmentry.tasks.lmentry_tasks import all_tasks

    if not PREDICTIONS_ROOT_DIR.exists():
        logging.error(f"Predictions not found at {PREDICTIONS_ROOT_DIR}. aborting.\n")
        return

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    missing_predictions = check_for_missing_predictions(PREDICTIONS_ROOT_DIR, set(all_tasks))
    if any([len(missing_predictions[model_name]) > 0 for model_name in missing_predictions]):
        missing_predictions_str = "\n".join([f"{model_name}: {task_names}" for
                                            model_name, task_names in
                                            sorted(missing_predictions.items())])
        logging.error("Some models don't have all task predictions. aborting.\n"
                    "missing predictions (<model>: <predictions>):\n"
                    f"{missing_predictions_str}\n"
                    "for scoring an individual task, see `score_task_predictions` from `accuracy.py`.")
        return

    model_names = sorted(missing_predictions.keys())
    
    logging.info(f"scoring LMentry predictions for models {sorted(missing_predictions.keys())}")

    score_all_predictions(task_names=sorted(all_tasks.keys()),
                            model_names=model_names,
                            num_processes=num_procs
                            )
    logging.info(f"finished scoring all LMentry predictions for models {model_names}")
    
    create_per_task_accuracy_csv(model_names=model_names)
    create_per_template_accuracy_csv(model_names=model_names)
    create_robustness_csv(model_names)
    create_lmentry_scores_csv(model_names=model_names)
    create_argument_order_robustness_csv(model_names=model_names)


def main(args):

    lang = args.language
    num_procs = args.num_procs

    ## initialize the global variables
    initialize_variables(lang)
    ## ----

    eval_main(num_procs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Execute Evaluation')
    parser.add_argument('-l', '--language', 
                        type=str, 
                        required=True)
    parser.add_argument("-n", "--num-procs",
                        default=1,
                        type=int,
                        help="the number of processes to use when scoring the predictions.\n"
                             "can be up to the number of models you want to evaluate * 41."
                        )
    args = parser.parse_args()
    main(args)