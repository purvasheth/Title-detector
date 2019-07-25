import pytesseract
from pytesseract import Output
import cv2
import pandas as pd
import json
import sys
if len (sys.argv) != 2 :
    print("Usage: python extract_title.py folder_path")
    sys.exit(1)
path = sys.argv[1]

with open("intermediate.json", "r") as read_file:
    data = json.load(read_file)
filenames = list(data.keys())
final_data = {}
for filename in filenames:
    img = cv2.imread(path + '/' +filename)
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    df = pd.DataFrame(d)
    new_df = df
    flag = 0
    btop = data[filename][1]
    bbottom = data[filename][3]

    df = df.loc[(df['conf']!= '-1') & (df['top'] > btop) & (df['top'] < bbottom) & (df['height']/2  <= bbottom - df['top'])]

    if df.empty:
        continue

    title_as_list = list(df['text'])
    title = " "
    title = title.join(title_as_list)
    top_as_list = list(df['top'])
    left_as_list = list(df['left'])
    height_as_list = list(df['height'])
    width_as_list = list(df['width'])
    para_as_list = list(df['par_num'])
    block_as_list = list(df['block_num'])
    line_as_list = list(df['line_num'])
    line_no = line_as_list[0]
    par_num = para_as_list[0]
    block_num = block_as_list[0]
    line_num = 0
    flag = 0


    if(block_as_list and all(block == block_num for block in block_as_list)) and (para_as_list and all(par == par_num for par in para_as_list)):
        flag = 1
    if line_no==1:
        line_num = 0
    elif line_as_list and all(line == line_no for line in line_as_list):
        line_num =line_no
    else:
        flag = 0
    #print(flag)
    top = min(top_as_list)
    left = min(left_as_list)
    x = top
    y = left
    h = 0
    w = 0
    if flag is 1:
        temp_w = new_df.loc[(new_df['block_num']==block_num)&(new_df['par_num']==par_num) & (new_df['line_num']==line_num) & (new_df['word_num']==0) & (new_df['left']== left) & (new_df['top']== top)]['width'].values
        temp_h = new_df.loc[(new_df['block_num']==block_num)&(new_df['par_num']==par_num) & (new_df['line_num']==line_num) & (new_df['word_num']==0) & (new_df['left']== left) & (new_df['top']== top)]['height'].values
        if (temp_w.size==0) or (temp_h.size==0):
            temp_w = new_df.loc[(new_df['block_num']==block_num)&(new_df['par_num']==par_num) & (new_df['line_num']==line_no) & (new_df['word_num']==0) & (new_df['left']== left) & (new_df['top']== top)]['width'].values
            temp_h = new_df.loc[(new_df['block_num']==block_num)&(new_df['par_num']==par_num) & (new_df['line_num']==line_no) & (new_df['word_num']==0) & (new_df['left']== left) & (new_df['top']== top)]['height'].values

        w = temp_w[0]
        h = temp_h[0]
    else:
        for (height,width,t,l) in zip(height_as_list,width_as_list,top_as_list,left_as_list):
            w = max(w,width+l)
            h = max(height+t,h)
        h = h - top
        #print(h,w)
        #print(left,to
    #print(title)
    x = left
    y = top

    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imwrite('final_prediction/'+ filename,img)
    #cv2.imshow('img', img)
    #cv2.waitKey(0)
    #cv2.destroyWindow('img')


    final_data[filename] = {
    "title" : title, "bbox" : [int(x),int(y),int(w),int(h)]
    }

with open("output.json", "w") as write_file:
    json.dump(final_data, write_file)
