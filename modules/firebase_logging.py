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
def get_user_history(user_id):
    ref = db.reference(f'users/{user_id}/queries')
    history = ref.order_by_child('timestamp').get()
    #測試
    print(f"Retrieved history for user : {history}")
    return history
def log_query_to_firebase(user_id, query, sentiment, response, final_response):
    current_time_in_taiwan = get_current_time_in_taiwan()
    # 確定要存儲的資料
    data = {
        'query': query,
        'sentiment': sentiment,
        'response': response,
        'final_response': final_response,
        'time': current_time_in_taiwan  # 添加當前時間戳
       }
    # 確定要存儲的位置
    ref =  db.reference(f'users/{user_id}/queries').push(data)  # 這裡使用 'user_queries' 作為存儲的根節點
    # 將資料寫入 Firebase
    ref.push(data)

def generate_response_based_on_history(user_id, query):
    # 檢索過去對話
    history = get_user_history(user_id)
    if history:
        # 可以選擇使用全部歷史對話或只使用最近的幾次對話來生成回應
        recent_history = list(history.values())[-5:]
        history_text = "\n".join([f"User: {item['query']}\nBot: {item['response']}" for item in recent_history])
    else:
        history_text = ""
    print(f"History text for user {user_id} : {history_text}")
    sentiment = analyze_prompt(query)

    # 3. 基於過去對話和當前query生成回應
    response = generate_response(query, complaint_keywords=[], doubt_keywords=[], insecurity_keywords=[])

    # 4. 執行文檔檢索
    docs = docsearch.similarity_search(query)
    shortened_docs = docs[:3]  # 確保選取部分文檔避免超過上下文長度限制

    # 5. 使用 invoke 方法並提供正確的參數
    input_data = {"input_documents": shortened_docs, "question": query}
    result = chain.invoke(input_data)
    final_response = result['output_text']

    # 6. 將查詢結果合併到最終回應中
    full_response = f"{history_text}\nUser: {query}\nBot: {response}{final_response}"
    print(full_response)

    # 7. 記錄這次對話
    log_query_to_firebase(user_id, query, sentiment, response, final_response)

    return full_response
