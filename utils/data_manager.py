user_data = {}

def save_user_data(chat_id, key, value):
    if chat_id not in user_data:
        user_data[chat_id] = {}
    user_data[chat_id][key] = value

