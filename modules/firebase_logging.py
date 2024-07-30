import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import pytz

# Firebase Configuration
cred = credentials.Certificate('path/to/serviceAccountKey.json')
firebase_admin.initialize_app(cred, {'databaseURL': 'https://your-database-url.firebaseio.com'})
db_ref = db.reference('/')

def get_current_time_in_taiwan():
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    return now.strftime("%Y-%m-%d %H:%M:%S")

def log_query_to_firebase(user_id, query, sentiment, response, final_response):
    current_time = get_current_time_in_taiwan()
    log_entry = {
        'query': query,
        'sentiment': sentiment,
        'response': response,
        'final_response': final_response,
        'timestamp': current_time
    }
    db_ref.child(user_id).push(log_entry)
