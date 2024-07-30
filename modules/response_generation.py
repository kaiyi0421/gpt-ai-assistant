from modules.sentiment_analysis import analyze_prompt
from modules.doc_search import search_documents
from modules.firebase_logging import log_query_to_firebase

def generate_response(user_id, query, docsearch, qa_chain):
    # 分析情感
    sentiment = analyze_prompt(query)
    
    # 根據關鍵字生成回應
    complaint_keywords = []  # 這裡應該填入實際的關鍵字
    doubt_keywords = []
    insecurity_keywords = []
    response = "根據情感分析的回應"

    # 文檔查詢
    docs = search_documents(docsearch, query)
    input_data = {"input_documents": docs, "question": query}
    result = qa_chain.invoke(input_data)
    final_response = result['output_text']
    
    # 合併最終回應
    full_response = f"{response}{final_response}"
    
    # 記錄查詢到 Firebase
    log_query_to_firebase(user_id, query, sentiment, response, final_response)
    
    return full_response
