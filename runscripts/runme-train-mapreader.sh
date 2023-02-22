#!/bin/bash

export NUMEPOCHS=$1

python run_summarization.py \
    --model_name_or_path t5-base \
    --do_train \
    --do_eval \
    --train_file training-data/t5goldout-withnavmodule-gamemapreader-numepisodes100.train.sourcetarget.json \
    --validation_file training-data/t5goldout-withnavmodule-gamemapreader-numepisodes100.dev.sourcetarget.json \
    --output_dir t5twx-game-mapreader-withnavmodule-base-1024-ep${NUMEPOCHS} \
    --overwrite_output_dir \
    --per_device_train_batch_size=2 \
    --per_device_eval_batch_size=2 \
    --predict_with_generate \
    --text_column source \
    --summary_column target \
    --save_strategy epoch \
    --logging_steps 1 \
    --num_train_epochs ${NUMEPOCHS} \
    --max_source_length 1024 \
    --max_target_length 128 \
    --pad_to_max_length=True \
    --ignore_pad_token_for_loss=True \
