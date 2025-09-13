from lmentry.constants import initialize_variables
import argparse

def main(args):

    lang = args.language
    num_procs = args.num_procs

    initialize_variables(lang)

    import lmentry
    from lmentry import evaluate
    from lmentry.evaluate import main as eval_main

    eval_main(num_procs)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
                    prog='Execute Prediction')
    parser.add_argument('-l', '--language', type=str, required=True)
    parser.add_argument("--num-procs",
                        default=1,
                        type=int,
                        help="the number of processes to use when scoring the predictions.\n"
                             "can be up to the number of models you want to evaluate * 41."
                        )
    args = parser.parse_args()
    main(args)