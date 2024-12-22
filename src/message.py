import requests
import pandas as pd
import os

def fetch_conversations(access_token):
    url = f"https://graph.facebook.com/v21.0/me/conversations"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Will raise an HTTPError for bad responses (400, 404, etc.)
    except requests.exceptions.HTTPError as e:
        if response.status_code == 400:
            print(f"Bad request (400) for access token {access_token}. Skipping...")
            return None  # Return None when the token is invalid or returns a 400 error
        else:
            raise e  # For other HTTP errors, re-raise the exception
    
    conversations = response.json().get("data", [])  # List of conversation objects
    conversation_data = []
    
    for conversation in conversations:
        conversation_data.append({
            "conversation_id": conversation["id"]
        })
    
    df = pd.DataFrame(conversation_data)
    return df

def fetch_messages_info(access_token, conversation_id):
    params = {
        "fields": "messages",
    }
    url = f"https://graph.facebook.com/v21.0/{conversation_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    messages_info_data = []
    
    messages_info = response.json().get("messages", {}).get("data", [])  # List of message info objects
    for message in messages_info:
        message_id = message["id"]
        messages_info_data.append({
            "id": message_id
        })
    
    df = pd.DataFrame(messages_info_data)
    return df

def fetch_message_data(access_token, message_id):
    params = {
        "fields": "id,created_time,from,to,message",
    }
    url = f"https://graph.facebook.com/v21.0/{message_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    message_data = response.json()  # Detailed message data
    return {
        "created_time": message_data.get("created_time", None),
        "from_name": message_data.get("from", {}).get("name", None),
        "from_id": message_data.get("from", {}).get("id", None),
        "to_name": message_data.get("to", {}).get("data", [{}])[0].get("name", None),
        "to_id": message_data.get("to", {}).get("data", [{}])[0].get("id", None),
        "message_content": message_data.get("message", "No message content")
    }

def save_messages_to_csv(all_message_data, access_token, business_name):
    message_df = pd.DataFrame(all_message_data)
    
    dir_path = './conversations_data/'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    file_path = f"{dir_path}{business_name}_messages.csv"

    message_df.to_csv(file_path, index=False)
    print(f"All message data for access token saved to {file_path}")

def process_token_with_pandas(tru_data):
    all_message_data = []
    access_token = tru_data["access_token"]
    business_name = tru_data["business_name"]
    
    # Fetch conversations for the current token
    conversations = fetch_conversations(access_token)
    
    if conversations is None:  # Skip the current access_token if fetching conversations failed
        return  # Move to the next token

    for _, conversation_row in conversations.iterrows():
        conversation_id = conversation_row["conversation_id"]
        print(f"Conversation ID DataFrame: {conversation_id}")
        
        # Fetch messages for the conversation
        messages_info = fetch_messages_info(access_token, conversation_id)
        
        for _, message_info_row in messages_info.iterrows():
            message_id = message_info_row["id"]
            print(f"Message ID DataFrame: {message_id}")
            
            # Fetch detailed message data
            message_data = fetch_message_data(access_token, message_id)
            all_message_data.append(message_data)
    
    save_messages_to_csv(all_message_data, access_token, business_name)
