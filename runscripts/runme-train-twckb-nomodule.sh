#!/bin/bash

#deepspeed --num_gpus 4 run_summarization.py \
#--source_prefix "" \
#    --model_name_or_path t5-base \

#export CUDA_VISIBLE_DEVICES=3
export NUMEPOCHS=$1
#deepspeed --num_gpus 4 run_summarization.py \

python run_summarization.py \
    --model_name_or_path t5-base \
    --do_train \
    --do_eval \
    --train_file training-data/t5goldout-gametwc-numepisodes100.train.sourcetarget.json \
    --validation_file training-data/t5goldout-gametwc-numepisodes100.dev.sourcetarget.json \
    --output_dir t5twx-game-twc-nomodule-base-1024-ep${NUMEPOCHS} \
    --overwrite_output_dir \
    --per_device_train_batch_size=4 \
    --per_device_eval_batch_size=4 \
    --predict_with_generate \
    --text_column source \
    --summary_column target \
    --save_total_limit 1 \
    --logging_steps 1 \
    --num_train_epochs ${NUMEPOCHS} \
    --max_source_length 1024 \
    --max_target_length 128 \
    --pad_to_max_length=True \
    --ignore_pad_token_for_loss=True \
 
#    --deepspeed ds_config-zero2.json \
#    --bf16 \
#    --do_predict \    
#    --deepspeed ds_config-zero2.json \
#    --bf16 \
    
