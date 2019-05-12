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

      return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)