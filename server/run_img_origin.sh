#!/bin/sh
echo "圖片名：$1";
python3 /home/ubuntu/img_to_text/img_to_text.py $1
python3 /home/ubuntu/img_to_text/origin_text_to_mp3.py
sox /home/ubuntu/tmp_wav/output.mp3 /home/ubuntu/communicate/output.mp3 speed 1.25 pitch -300