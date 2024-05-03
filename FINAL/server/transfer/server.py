from google.cloud import storage
import os
from audio_recognition_server import audio_recognition_server
from request_gpt import call_openai_api
from Image_request_gpt import call_openai_image_api
import argparse
import json
from openai import OpenAI

# read key from txt
with open("key.txt", "r") as key_file:
    api_key = key_file.read().strip()

client = OpenAI(api_key=api_key)

# global messages
history_messages = [
    {"role": "system", "content": "You are a helpful assistant and you can analyze both images and texts"}
]

conversation_history = ""

#google drive api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cre2.json"
def is_file_exist(bucket_name, file_name):

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.exists()

def is_bucket_empty(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = list(bucket.list_blobs())
    print("bucket is empty")
    return len(blobs) == 0


def process_data(file_path):
    try:
        # Open the file in read mode
        with open(file_path, 'r') as file:
            # Read the text from the file
            text = file.read()
        
        # Convert the text to uppercase
        answer = process_data_with_gpt(text)
        
        # Write the uppercase text to a new file
        with open("processed_data.txt", "w") as processed_file:
            processed_file.write(answer)
        
        print("Text processed and saved to processed_data.txt")
        
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print("An error occurred:", e)


def process_data_with_gpt(new_question):
    global conversation_history
    conversation_history += f"User: {new_question}\n"
    if (new_question[0]=="/"):
        response = call_openai_image_api(new_question)
        print("call gpt4")
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response into a Python dictionary
            data = response.json()

            # Access the content text from the response
            if 'choices' in data and len(data['choices']) > 0:
                answer = data['choices'][0]['message']['content']
                print("Generated content:")
                print(answer)
            else:
                print("No valid content found in the response.")
        else:
            print(f"Error: API request failed with status code {response.status_code}")
    else: 
        response = call_openai_api(new_question)
        answer = response.choices[0].message.content
    conversation_history += f"AI: {answer}\n"

    return answer


def upload_blob_server(bucket_name, source_file_name, destination_blob_name,count):
    """Uploads a file to the bucket."""
    # initialize
    client = storage.Client()

    
    bucket = client.get_bucket(bucket_name)

   
    if(count != 0):
        blob = bucket.blob(f"process_data{count-1}.txt")
        blob.delete()

    # construct blob
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)

    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")



def download_blob_server(bucket_name, source_blob_name, destination_file_name, count):
    """Downloads a blob from the bucket if it exists."""
    # initialize
    client = storage.Client()

    # get specific bucket
    bucket = client.get_bucket(bucket_name)

    # exist
    blob = bucket.blob(source_blob_name)
    if not blob.exists():
        #print(f"Blob {source_blob_name} does not exist in {bucket_name}.")
        return count

    # download file
    else:
        blob.download_to_filename(destination_file_name)

        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")

        process_data(destination_file_name)
        process_datafile = "processed_data.txt"
        ##upload the file
        upload_blob_server(bucket_name, process_datafile, f"process_data{count}.txt",count)

        return count + 1
    




def main(audio = False):
    count = 0
    bucket_name = "haoyuh3"
    destination_file_name = "destination_file.txt"  #
    
    audio_detection = audio
    try:
        if(audio_detection):
                print("speech recognition started...")
                audio_recognition_server()
    except KeyboardInterrupt:
        print("\nExiting loop audio...")

    try:
        while True:
            source_blob_name = f"temp_data{count}.txt"

            if is_bucket_empty(bucket_name): count = 0
                
            new_count = download_blob_server(bucket_name, source_blob_name, destination_file_name, count)
            if count == new_count:
                print("wait for response")
            else:
                print("make response")
            count = new_count
    except KeyboardInterrupt:
        print("\nExiting loop...")
        # store as a file
        with open("conversation.txt", "w") as file:
            file.write(conversation_history)

    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with optional audio argument")
    parser.add_argument("--audio", type=bool, nargs='?', const=True, default=False, help="Enable audio")

    args = parser.parse_args()
    main(args.audio)