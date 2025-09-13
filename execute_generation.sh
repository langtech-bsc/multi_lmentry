#!/bin/bash


# see the constants.py for the correct name to refer to the models

MODELS="Llama-3_2-1B-Instruct Llama-3_2-3B-Instruct Qwen2_5-1_5B-Instruct Qwen2_5-3B-Instruct Qwen2_5-7B-Instruct"

# it
python execute.py \
    --lang it \
    --model_list $MODELS

# ca
python execute.py \
    --lang ca \
    --model_list $MODELS

# de
python execute.py \
    --lang de \
    --model_list $MODELS

# en
python execute.py \
    --lang en \
    --model_list $MODELS

# es
python execute.py \
    --lang es \
    --model_list $MODELS

# eu
python execute.py \
    --lang eu \
    --model_list $MODELS

# gl
python execute.py \
    --lang gl \
    --model_list $MODELS

# pt_br
python execute.py \
    --lang pt_br \
    --model_list $MODELS