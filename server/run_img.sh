#!/bin/sh
echo "圖片名：$1";
python3 /home/ubuntu/img_to_text/img_to_text.py $1
python3 /home/ubuntu/SUM/SummarizerForChinese.py /home/ubuntu/tmp_txt/output_tmp.txt -l 2 > /home/ubuntu/tmp_sum/sum_tmp.txt
python3 /home/ubuntu/img_to_text/text_to_mp3.py
sox /home/ubuntu/tmp_wav/output.mp3 /home/ubuntu/communicate/output.mp3 speed 1.25 pitch -300
