#!/bin/bash
if [ $# -eq 0 ]; then
	echo "give the path to images"
	exit 1
fi
python KerasModel/yolo_image.py $1
python extract_title.py $1
