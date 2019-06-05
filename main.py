# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys
from pytube import YouTube
import cv2
import os
from src import imago
import goClassifier
import re

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)', text) ]

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/logger')
def dir_listing():
    files = os.listdir('static/logger')
    files = ['static/logger/' + file for file in files]
    return render_template('files.html', files=files)

@app.route('/youtube', methods=['POST'])
def youtube():
   if request.method == 'POST':
        url = request.form['url']
        second = int(request.form['second'])
        print url, second
        yt = YouTube(url)
        yt.streams.first().download(os.getcwd(), filename='temp')

        cap = cv2.VideoCapture("temp.mp4")

        try:
            if not os.path.exists('./static/frame'):
                os.makedirs('./static/frame')
        except OSError:
            print 'Error: Creating directory of frame'

        vidcap = cv2.VideoCapture('temp.mp4')
        currentFrame = 0
        currentSavedFrame = 0
        while(True):
            success,image = vidcap.read()
            if not success:
                break
            ret, frame = cap.read()

            if(currentFrame % (second*30) == 0):
                    name = './static/frame/' + str(currentSavedFrame) + '.jpg'
                    currentSavedFrame += 1
                    print 'Creating...' + name
                    cv2.imwrite(name, frame)

            currentFrame += 1
        cap.release()
        vidcap.release()

        path = 'temp.mp4'
        os.remove(path)

        image_names = os.listdir('./static/frame')
        image_names.sort(key=natural_keys)
        image_names = ['./static/frame/' + image for image in image_names]

        return render_template('index.html', image_names=image_names)

@app.route('/cropping', methods=['GET'])
def cropping():
    if request.method == 'GET':
        # Save path to read and write image.
        try:
            if not os.path.exists('./static/processedframe'):
                os.makedirs('./static/processedframe')
        except OSError:
            print 'Error: Creating directory of frame'

        # Save path directory.
        inputFileDir = os.path.abspath("./static/frame/")
        inputFileDirList = os.listdir(inputFileDir)
        inputFileDirList.sort(key=natural_keys)
        print inputFileDirList

        for imageName in inputFileDirList:
            # Read image.
            if str(imageName) == ".keep":
                continue

            originalImage = cv2.imread(os.path.join("./static/frame/", imageName))
            originalHeight, originalWidth, originalChanels = originalImage.shape
            originalHeight += 0.1
            originalWidth += 0.1

            goClassifier.processingImage(originalImage, goClassifier.preprocessingImage(originalImage), originalHeight, originalWidth, "./static/processedframe")

        image_names = os.listdir('./static/processedframe')
        image_names.sort(key=natural_keys)
        image_names = ['./static/processedframe/' + image for image in image_names]

        return render_template('index.html', image_names=image_names)

@app.route('/detect', methods=['GET'])
def detect():
    try:
        if not os.path.exists('./static/logger'):
            os.makedirs('./static/logger')
    except OSError:
        print 'Error: Creating directory of frame'

    inputFileDir = os.path.abspath("./static/processedframe/")
    inputFileDirList = os.listdir(inputFileDir)
    inputFileDirList.sort(key=natural_keys)
    print inputFileDirList

    inputFileDirList = ['./static/processedframe/' + image for image in inputFileDirList]
    imago.main(inputFileDirList, './static/logger/')

    return render_template('index.html')

@app.route('/view', methods=['GET'])
def view():
    try:
        if not os.path.exists('./static/logger'):
            os.makedirs('./static/logger')
    except OSError:
        print 'Error: Creating directory of result'

    logDir = os.path.abspath("./static/logger/")
    logList = os.listdir(logDir)
    logList.sort(key=natural_keys)
    print logList

    resultFile = open(logDir + "/result.txt", 'w') #결과 저장할 텍스트파일

    for lognum in range(0, len(logList) -1):
    #로그리스트 크기 -1만큼 반복
        log_prev = open(logDir + logList[lognum] + ".txt",'r') #이전 수 상황 0~ n-1
        log_curr = open(logDir + logList[lognum +1] + ".txt",'r') #현재 수 상황 1~n

        for rownum in range(0,19): #파일 끝까지 읽음
            line_prev = log_prev.readline() #이전 수 파일 한줄 읽음
            if not line_prev: break #없으면 나옴
            line_curr = log_prev.readline() #현재 수 파일 한줄 읽음
            if not line_curr: break #없으면 나옴

            for colnum in range(0,len(line_curr)): #두 파일의 한줄당 글자수는 같을것이므로
                if(line_prev[colnum] != line_curr[colnum]): 
                    #읽다가 다른 수가 발견되면 여기 둔것임
                    resultFile.write(line_curr[colnum] + " (" + str(rownum) + "," + str(colnum) + ")\n")
                    break 
                    #B (x,y) 또는 W (x,y)형식으로 한줄씩 기록후 break

            
    f.close() #기록이 끝나면 닫음

    #pass

if __name__ == '__main__':
    app.run(host='0.0.0.0')

