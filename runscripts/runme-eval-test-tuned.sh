#!/bin/bash

# Arithmetic -- With calc module
# many epochs had 1.00 performance on dev -- picked ep4
python main.py --game_name=arithmetic --num_variations 100 --max_steps=50 --train_or_eval=eval --set=test --lm_path=t5twx-game-arithmetic-withcalcmodule-base-1024-ep4  --useSymbolicModules=calc

# Mapreader - navigation
# Many episodes had 1.00 performance on dev -- picked ep4
python main.py --game_name=mapreader --num_variations 100 --max_steps=50 --train_or_eval=eval --set=test --lm_path=t5twx-game-mapreader-withnavmodule-base-1024-ep4  --useSymbolicModules=navigation

# Sorting - with sorting module
# Many episodes had 1.00 performance on dev -- picked ep12
python main.py --game_name=sorting --num_variations 100 --max_steps=50 --train_or_eval=eval --set=test --lm_path=t5twx-game-sorting-withsortmodule-base-1024-ep12  --useSymbolicModules=sortquantity

# TWC - KB
# ep14 had 1.00 on dev.  (Note, ep10 had 0.99)
python main.py --game_name=twc-easy --num_variations 100 --max_steps=50 --train_or_eval=eval --set=test --lm_path=t5twx-game-twc-withtwcmodule-base-1024-ep14  --useSymbolicModules=kb-twc
