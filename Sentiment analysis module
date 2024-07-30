import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import random
# 初始化VADER情感分析工具
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def analyze_prompt(query):
    # 使用VADER分析情感
    sentiment = sia.polarity_scores(query)
    return sentiment


def categorize_question(message):
    message = message.lower()

    # 定義關鍵字或模式來分類問句
    complaint_keywords = ["煩","無聊","累","那麼多","不值得","沒空","痛苦"
    ,"沮喪","心情差","不想","沒用","不需要"]
    doubt_keywords = ["為什麼","有甚麼用","有什麼用","有用嗎","有必要","是否","不理解"]
    insecurity_keywords = ["不自信", "沒信心", "害怕", "擔心", "怕","難","做不到"
    ,"無法完成","無法達成","不確定"]

    # 判斷是否包含特定關鍵字
    if any(keyword in message for keyword in complaint_keywords):
        return "complaint"
    elif any(keyword in message for keyword in doubt_keywords):
        return "doubt"
    elif any(keyword in message for keyword in insecurity_keywords):
        return "insecurity"
    else:
        return "neutral"

def generate_response(query, complaint_keywords, doubt_keywords, insecurity_keywords):
    sentiment_scores = analyze_prompt(query)
    question_type = categorize_question(query)

    complaint_responses = [
        "運動一定要做，不要再幫自己找理由。",
        "運動一定要做，不然不會好。",
        "不管事無聊還是累，都要繼續做。"
        "不努力就別指望有百分之百的康復效果"
    ]
    doubt_responses = [
        "這些運動是根據醫學研究設計的，能夠有效幫助您的康復。",
        "每一次的努力都在為你的康復打下堅實的基石，請繼續堅持復健",
        "相信醫生的建議，這些運動對您的健康是有科學依據的。"
    ]
    insecurity_responses = [
        "康復過程中遇到困難是正常的，但請相信您能夠完成這些運動。",
        "我們會根據您的進展調整康復計劃，確保您能夠應對。",
        "如果您有任何擔心，請隨時與我們溝通，我們會給予支持。"
    ]
    neutral_response = ""
    if question_type == "complaint":
        return random.choice(complaint_responses)
    elif question_type == "doubt":
        return random.choice(doubt_responses)
    elif question_type == "insecurity":
        return random.choice(insecurity_responses)
    else:
        return neutral_response



