#!/bin/sh

HERE=$(pwd)

cd /home/ubuntu/ASR/daicon/;/home/ubuntu/ASR/daicon/get_asr.sh /home/ubuntu/communicate /home/ubuntu/tmp_txt; cd $HERE

python3 /home/ubuntu/SUM/SummarizerForChinese.py /home/ubuntu/tmp_txt/output_tmp.txt -l 3 > /home/ubuntu/tmp_sum/sum_tmp.txt

/home/ubuntu/MFA/run_ali.sh /home/ubuntu/communicate/wav2asr.wav /home/ubuntu/tmp_txt/output_tmp.txt /home/ubuntu/tmp_sum/sum_tmp.txt /home/ubuntu/tmp_wav/wav_tmp.wav

sox /home/ubuntu/tmp_wav/wav_tmp.wav /home/ubuntu/communicate/output.mp3

