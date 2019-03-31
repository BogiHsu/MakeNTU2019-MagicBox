#!/bin/sh

HERE=$(pwd)

cd /home/ubuntu/ASR/daicon/;/home/ubuntu/ASR/daicon/get_asr.sh /home/ubuntu/communicate /home/ubuntu/tmp_txt; cd $HERE

python3 /home/ubuntu/SUM/SummarizerForChinese.py /home/ubuntu/tmp_txt/output_tmp.txt -l 3 > /home/ubuntu/tmp_sum/sum_tmp.txt

python3 /home/ubuntu/img_to_text/text_to_mp3.py

sox /home/ubuntu/tmp_wav/output.mp3 /home/ubuntu/communicate/output.mp3 speed 1.25 pitch -300
