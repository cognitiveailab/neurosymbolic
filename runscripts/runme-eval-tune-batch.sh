#!/bin/bash


# Arithmetic -- With calc module
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep2  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep4  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep6  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep8  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep10  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep12  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep14  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep16  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep18  --useSymbolicModules=calc
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep20  --useSymbolicModules=calc


# Mapreader - navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep2  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep4  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep6  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep8  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep10  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep12  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep14  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep16  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep18  --useSymbolicModules=navigation
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep20  --useSymbolicModules=navigation


# Sorting - with sorting module
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep2  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep4  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep6  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep8  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep10  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep12  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep14  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep16  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep18  --useSymbolicModules=sortquantity
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep20  --useSymbolicModules=sortquantity


# TWC - KB
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep2  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep4  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep6  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep8  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep10  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep12  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep14  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep16  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep18  --useSymbolicModules=kb-twc
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=dev --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep20  --useSymbolicModules=kb-twc
