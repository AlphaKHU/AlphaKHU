## notice

- git checkout -b `브랜치 이름`으로 브랜치 변경 후 master에 말고 브랜치에 push 해주세요.
- 코드 리뷰 후 merge 해드리겠습니다.



## Environment

- Ubuntu 16.04(for building `make`)
- python 2.7



## Configuration

1. ```shell
   $ sudo apt-get update  
   ```

2. ```shell
   $ sudo apt-get install -y python git make gcc build-essential python-dev \
     python-pip libsm6 libxext6 libxrender-dev python-matplotlib
   ```

3. ```shell
   $ git clone https://github.com/AlphaKHU/AlphaKHU && cd AlphaKHU && make
   ```

4. ```shell
   $ pip install -r requirements.txt
   ```

5. ```shell
   $ python main.py
   ```


