

####  Image read and  return response #####

import json
from openai import OpenAI
import requests
# 从 key.txt 文件中读取密钥
with open("key.txt", "r") as key_file:
    api_key = key_file.read().strip()

client = OpenAI(api_key=api_key)

# 全局变量，用于存储历史消息

##store history message
history_messages = [
    {"role": "system", "content": "You are a helpful assistant and you can analyze both images and texts"}
]

def call_openai_image_api(new_question):
    global history_messages
    #new_message_content = new_question
    new_message = {"role": "user", "content": new_question}
    history_messages.append(new_message)

    headers = {"Content-Type": "application/json","Authorization": f"Bearer {api_key}"}

    payload = {
    "model": "gpt-4-turbo",
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": "What can you see in this image? If there is person, describe him or her. If there are some other stuffs, describe them,too. Assume that you are watching them."
            },
            {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{new_question}"
            }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    data = response.json()
    new_response = {"role": "assistant", "content": data['choices'][0]['message']['content']}
    history_messages.append(new_response)
    return response

if __name__ == "__main__":
    message = ""
    while True:
        new_question = input("Enter data: ")
        if(new_question == "quit"):
            break
        message += f"User: {new_question}\n"
        response = call_openai_image_api(new_question)
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response into a Python dictionary
            data = response.json()

            # Access the content text from the response
            if 'choices' in data and len(data['choices']) > 0:
                content_text = data['choices'][0]['message']['content']
                print("Generated content:")
                print(content_text)
            else:
                print("No valid content found in the response.")
        else:
            print(f"Error: API request failed with status code {response.status_code}")
        message += f"AI: {content_text}\n"
        

    with open("conversation.txt", "w") as file:
        file.write(content_text)
    
    