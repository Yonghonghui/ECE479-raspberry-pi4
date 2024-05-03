
import json
from openai import OpenAI

##read key
with open("key.txt", "r") as key_file:
    api_key = key_file.read().strip()

client = OpenAI(api_key=api_key)

##store history message
history_messages = [
    {"role": "system", "content": "You are a helpful assistant and you can analyze both images and texts"}
]


def call_openai_api(new_question):
    global history_messages

    #new_message_content = new_question
    new_message = {"role": "user", "content": new_question}
    history_messages.append(new_message)

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=history_messages
    )
    new_response = {"role": "assistant", "content": response.choices[0].message.content}
    history_messages.append(new_response)
    return response

if __name__ == "__main__":
    message = ""
    while True:
        new_question = input("Enter data: ")
        if(new_question == "quit"):
            break
        message += f"User: {new_question}\n"
        response = call_openai_api(new_question)
        answer = response.choices[0].message.content
        print(response.choices[0].message.content)
        message += f"AI: {answer}\n"

    with open("conversation.txt", "w") as file:
        file.write(message)
    
    
