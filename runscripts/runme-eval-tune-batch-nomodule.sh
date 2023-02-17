#!/bin/bash


# Arithmetic -- No calc module
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep2
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep4
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep6
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep8
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep10
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep12
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep14
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep16
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep18
#python main.py --game_name=arithmetic --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024-ep20

# Arithmetic -- With calc module
#python main.py --game_name=arithmetic --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024  --useSymbolicModules=calc


# Mapreader (random) - no module
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep2
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep4
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep6
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep8
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep10
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep12
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep14
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep16
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep18
python main.py --game_name=mapreader-random --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-random-nomodule-base-1024-ep20

# Mapreader - navigation
#python main.py --game_name=mapreader --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024  --useSymbolicModules=navigation


# Sorting - no module
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep2
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep4
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep6
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep8
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep10
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep12
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep14
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep16
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep18
#python main.py --game_name=sorting --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024-ep20

# Sorting - with sorting module
#python main.py --game_name=sorting --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024  --useSymbolicModules=sortquantity


# TWC - No Module
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep2
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep4
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep6
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep8
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep10
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep12
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep14
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep16
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep18
#python main.py --game_name=twc-easy --num_variations 100 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024-ep20

# TWC - KB
#python main.py --game_name=twc-easy --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024  --useSymbolicModules=kb-twc

