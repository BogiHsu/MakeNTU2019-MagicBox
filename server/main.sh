# !/bin/bash

DIR="/home/ubuntu/communicate/"
img_file=$DIR"/image.jpg"
img_origin_file=$DIR"/image_origin.jpg"
wav_file=$DIR"/wav2asr.wav"
wav_tts_file=$DIR"/wav2asr_tts.wav"
dcmd="date +%Y-%m-%d-%H:%M:%S"

while true; do

	echo $($dcmd)': Server OK.'
	if [ -f $img_file ]; then
		echo ''
		echo $($dcmd)': OCR'
		python3 wait_file.py $img_file
		bash /home/ubuntu/run_img.sh $img_file
	fi
	
	if [ -f $img_origin_file ]; then
		echo ''
		echo $($dcmd)': OCR origin'
		python3 wait_file.py $img_origin_file
		bash /home/ubuntu/run_img_origin.sh $img_origin_file
	fi
	
	if [ -f $wav_file ]; then
		echo ''
		echo $($dcmd)': ASR'
		python3 wait_file.py $wav_file
		bash /home/ubuntu/run_wav.sh 
	fi
	
	if [ -f $wav_tts_file ]; then
		echo ''
		echo $($dcmd)': ASR tts'
		python3 wait_file.py $wav_tts_file
		bash /home/ubuntu/run_wav_tts.sh 
	fi
	
	while [ "$(ls -A $DIR)" ]; do
		echo $($dcmd)': Waiting for client.'
		sleep 0.1
	done
	
	rm -rf tmp_*/*
	sleep 0.1
	
done
