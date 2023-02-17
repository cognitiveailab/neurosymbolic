#!/bin/bash


# Arithmetic -- No calc module
# ep16 had the best results on dev (0.510)
python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=test --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep16


# Mapreader (random) - no module
# ep18 had the best results on dev (0.700)
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=test --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep18


# Sorting - no module
# ep20 had the best results on dev (0.760)
python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=test --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20


# TWC - No Module
# ep8 had the best results on dev (0.860)
python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=test --lm_path=t5twx-game-twc-nomodule-base-1024-ep8

