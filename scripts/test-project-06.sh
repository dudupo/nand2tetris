python ./projects/06/asmsrc/main.py ./projects/06/add/Add.asm
python ./projects/06/asmsrc/main.py ./projects/06/max/Max.asm
python ./projects/06/asmsrc/main.py ./projects/06/rect/Rect.asm
python ./projects/06/asmsrc/main.py ./projects/06/pong/Pong.asm

./tools/TextComparer.bat ./projects/06/add/Add_out.hack ./projects/06/add/Add.hack
./tools/TextComparer.bat ./projects/06/pong/Pong_out.hack ./projects/06/pong/Pong.hack
./tools/TextComparer.bat ./projects/06/max/Max_out.hack ./projects/06/max/Max.hack
./tools/TextComparer.bat ./projects/06/rect/Rect_out.hack ./projects/06/rect/Rect.hack
