from firebase import firebase
import firebase_admin
from firebase_admin import credentials, db
from google.colab import drive
from datetime import datetime
import pytz
import time
import os
drive.mount('/content/drive/')

config = {
  'apiKey': "AIzaSyAv3CGpAWsmV0xJ7I7bo7rnlWjkmKIDNwI",
  'authDomain': "text-history-add87.firebaseapp.com",
  'databaseURL': "https://text-history-add87-default-rtdb.firebaseio.com",
  'projectId': "text-history-add87",
  'storageBucket': "text-history-add87.appspot.com",
  'messagingSenderId': "658426114408",
  'appId': "1:658426114408:web:ead534732ca17d271e66dd",
  'measurementId': "G-QLEKHX92HZ"
};

# 設定 Firebase 服務帳戶憑證並確保只初始化一次
if not firebase_admin._apps:
    cred = credentials.Certificate('/content/drive/MyDrive/serviceAccountKey.json')
    firebase_admin.initialize_app(cred, {
        'databaseURL': config['databaseURL']
    })

# 使用 python-firebase 初始化 FirebaseApplication
url = config['databaseURL']
fdb = firebase.FirebaseApplication(url, None)

def get_current_time_in_taiwan():
    # 定義台灣時區
    taiwan_tz = pytz.timezone('Asia/Taipei')
    # 獲取當前時間並轉換為台灣時區
    current_time = datetime.now(taiwan_tz).strftime('%Y-%m-%d %H:%M:%S')
    return current_time
