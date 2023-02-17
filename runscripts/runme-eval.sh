#!/bin/bash

# No fine-tuning
#python main.py --game_name=takethisaction --num_variations 10 --max_steps=10 --train_or_eval=eval --set=dev --lm_path=t5-small

# Fine-tuning
#python main.py --game_name=takethisaction --num_variations 10 --max_steps=10 --train_or_eval=eval --set=dev --lm_path=t5twx-game-takethisaction
#python main.py --game_name=takethisaction --num_variations 10 --max_steps=10 --train_or_eval=eval --set=test --lm_path=t5twx-game-takethisaction


# Arithmetic -- No calc module
#python main.py --game_name=arithmetic --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-nomodule-base-1024

# Arithmetic -- With calc module
#python main.py --game_name=arithmetic --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024  --useSymbolicModules=calc


# Mapreader - no module
#python main.py --game_name=mapreader --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-nomodule-base-1024  --useSymbolicModules=navigation

# Mapreader - navigation
#python main.py --game_name=mapreader --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024  --useSymbolicModules=navigation


# Sorting - with sorting module
#python main.py --game_name=sorting --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024  --useSymbolicModules=sortquantity

# Sorting - no module
#python main.py --game_name=sorting --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-nomodule-base-1024


# TWC - No Module
#python main.py --game_name=twc-easy --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-nomodule-base-1024
#python main.py --game_name=twc-easy --num_variations 20 --max_steps=20 --train_or_eval=eval --set=test --lm_path=t5twx-game-twc-nomodule-base-1024

# TWC - KB
python main.py --game_name=twc-easy --num_variations 20 --max_steps=20 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024  --useSymbolicModules=kb-twc
#python main.py --game_name=twc-easy --num_variations 20 --max_steps=20 --train_or_eval=eval --set=test --lm_path=t5twx-game-twc-withtwcmodule-base-1024  --useSymbolicModules=kb-twc

