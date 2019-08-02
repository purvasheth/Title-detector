# Title-Detector

It uses a two step process. 
1) Object Detection to get a rough estimation for bounding box of title.
2) Text extraction using tesseract ocr engine along with final bounding box.

**Requirements** 
1) OS : Linux
2) Python 3
3) Keras
4) Pytesseract

**Testing**

Input images can be stored in Images folder or at any other path. This path should be provided while executing run.sh as a commandline argument. For example,

```
$ chmod 777 run.sh
$ ./run.sh Images
```
The bounding boxes detected after the first step are stored in intermediate.json. Every entry in this file consists of image filename as key and bounding box for title as value.
The final output is stored in output.json. Every entry in this file consists of image filename as key and title and bounding box as values.

For visualisation of bounding boxes, the intermediate step predictions are stored in prediction folder and the final predictions are stored in final_prediction folder.

