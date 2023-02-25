#!/bin/bash


# Arithmetic -- No calc module
export CUDA_VISIBLE_DEVICES=0
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-150
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-300
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-450
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-600
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-750
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-900
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1050
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1200
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1350
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1500
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1650
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1800
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-1950
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2100
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2250
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2400
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2550
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2700
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-2850
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20/checkpoint-3000


# Mapreader - no module
export CUDA_VISIBLE_DEVICES=1
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-284
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-568
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-852
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-1136
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-1420
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-1704
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-1988
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-2272
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-2556
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-2840
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-3124
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-3408
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-3692
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-3976
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-4260
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-4544
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-4828
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-5112
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-5396
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024-ep20/checkpoint-5680


# Sorting - no module
export CUDA_VISIBLE_DEVICES=2
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-223
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-446
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-669
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-892
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-1115
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-1338
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-1561
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-1784
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-2007
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-2230
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-2453
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-2676
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-2899
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-3122
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-3345
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-3568
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-3791
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-4014
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-4237
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20/checkpoint-4460


# TWC - No Module
export CUDA_VISIBLE_DEVICES=3
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-112
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-224
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-336
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-448
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-560
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-672
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-784
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-896
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1008
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1120
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1232
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1344
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1456
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1568
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1680
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1792
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-1904
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-2016
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-2128
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20/checkpoint-2240
