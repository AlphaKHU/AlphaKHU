# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/youtube', methods=['POST'])
def youtube():
   if request.method == 'POST':
        url = request.form['url']
        second = request.form['second']
        print(url, second)

        """
            유튜브 동영상 주소를 다운로드 받아
            이미지를 프레임(시간 간격)으로 특정 폴더에 저장하는 코드 작성
        """

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