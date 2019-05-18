# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import sys
from pytube import YouTube
import cv2
import os

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/youtube', methods=['POST'])
def youtube():
   if request.method == 'POST':
        url = request.form['url']
        second = int(request.form['second'])
        print(url, second)
        yt = YouTube(url)
        yt.streams.first().download(os.getcwd())

        cap = cv2.VideoCapture(yt.title + ".mp4")

        try:
            if not os.path.exists('frame'):
                os.makedirs('frame')
        except OSError:
            print ('Error: Creating directory of frame')

        vidcap = cv2.VideoCapture(yt.title + '.mp4')
        currentFrame = 0
        currentSavedFrame = 0
        while(True):
            success,image = vidcap.read()
            if not success:
                break
            ret, frame = cap.read()

            if(currentFrame % (second*30) == 0):
                    name = './frame/frame' + str(currentSavedFrame) + '.jpg'
                    currentSavedFrame += 1
                    print ('Creating...' + name)
                    cv2.imwrite(name, frame)

            currentFrame += 1
        cap.release()
        vidcap.release()

        path =  yt.title + '.mp4'
        os.remove(path)
        
        return render_template('index.html')

@app.route('/cropping', methods=['GET'])
def cropping():
    """
        youtube() 함수에서 폴더에 저장된 이미지들을 Cropping하여 새로운 폴더에 옮기는 코드 작성
    """
    pass

@app.route('/detect', methods=['GET'])
def detect():
    pass

@app.route('/view', methods=['GET'])
def view():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
