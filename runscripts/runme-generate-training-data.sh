#!/bin/bash

# Arithmetic (no calc module)
python main.py --game_name=arithmetic --num_variations 100 --train_or_eval=train-gen --set=train --traindataSavePrefix=t5goldout
python main.py --game_name=arithmetic --num_variations 100 --train_or_eval=train-gen --set=dev --traindataSavePrefix=t5goldout

# Arithmetic game + calc module
python main.py --game_name=arithmetic --num_variations 100 --train_or_eval=train-gen --set=train --useSymbolicModules=calc --traindataSavePrefix=t5goldout-withcalcmodule
python main.py --game_name=arithmetic --num_variations 100 --train_or_eval=train-gen --set=dev --useSymbolicModules=calc --traindataSavePrefix=t5goldout-withcalcmodule

# mapreader game
python main.py --game_name=mapreader --num_variations 100 --train_or_eval=train-gen --set=train --traindataSavePrefix=t5goldout
python main.py --game_name=mapreader --num_variations 100 --train_or_eval=train-gen --set=dev --traindataSavePrefix=t5goldout

# mapreader game + navigation module
python main.py --game_name=mapreader --num_variations 100 --train_or_eval=train-gen --set=train --useSymbolicModules=navigation --traindataSavePrefix=t5goldout-withnavmodule
python main.py --game_name=mapreader --num_variations 100 --train_or_eval=train-gen --set=dev --useSymbolicModules=navigation --traindataSavePrefix=t5goldout-withnavmodule

# sorting game (no module)
python main.py --game_name=sorting --num_variations 100 --train_or_eval=train-gen --set=train --traindataSavePrefix=t5goldout
python main.py --game_name=sorting --num_variations 100 --train_or_eval=train-gen --set=dev --traindataSavePrefix=t5goldout

# sorting game + sorting module
python main.py --game_name=sorting --num_variations 100 --train_or_eval=train-gen --set=train --useSymbolicModules=sortquantity --traindataSavePrefix=t5goldout-withsortmodule
python main.py --game_name=sorting --num_variations 100 --train_or_eval=train-gen --set=dev --useSymbolicModules=sortquantity --traindataSavePrefix=t5goldout-withsortmodule

# TWC + kb module
python main.py --game_name=twc-easy --num_variations 100 --train_or_eval=train-gen --set=train --useSymbolicModules=kb-twc --traindataSavePrefix=t5goldout-withkbtwcmodule
python main.py --game_name=twc-easy --num_variations 100 --train_or_eval=train-gen --set=dev --useSymbolicModules=kb-twc --traindataSavePrefix=t5goldout-withkbtwcmodule

# TWC (no KB module)
python main.py --game_name=twc-easy --num_variations 100 --train_or_eval=train-gen --set=train  --traindataSavePrefix=t5goldout
python main.py --game_name=twc-easy --num_variations 100 --train_or_eval=train-gen --set=dev  --traindataSavePrefix=t5goldout
