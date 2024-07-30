from flask import Flask, request, abort
from linebot.v3 import (
    WebhookHandler, Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
)
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from pyngrok import ngrok
import os
from modules.firebase_logging import log_query_to_firebase
from modules.sentiment_analysis import analyze_prompt
from modules.response_generation import generate_response
from modules.doc_search import setup_doc_search, search_documents
from modules.load_pdf import load_pdf

app = Flask(__name__)

# Setup document search
docsearch, qa_chain = setup_doc_search()

# Load PDF (Example: for demonstration)
load_pdf('/content/gdrive/My Drive/人工膝關節置換術.pdf')

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_id = event.source.user_id
    query = event.message.text

    # 分析情感
    sentiment = analyze_prompt(query)
    
    # 根據關鍵字生成回應
    response = generate_response(query, complaint_keywords=[], doubt_keywords=[], insecurity_keywords=[])

    # 文檔查詢
    docs = search_documents(docsearch, query)
    input_data = {"input_documents": docs, "question": query}
    result = qa_chain.invoke(input_data)
    final_response = result['output_text']
    
    # 合併最終回應
    full_response = f"{response}{final_response}"

    # 發送回應
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=full_response)]
        )
    )
    
    # 記錄查詢到 Firebase
    log_query_to_firebase(user_id, query, sentiment, response, final_response)

if __name__ == "__main__":
    app.run(port=5000)
