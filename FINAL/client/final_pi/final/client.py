from google.cloud import storage
import os
from speech_text import transcribe_audio
from audio_text import text_to_speech
## change folder name to module 
from module.facial_req import face_detection
import argparse
import pyaudio
import wave
import numpy as np
import sys
#api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cre2.json"

def record_audio(file_path, duration=6, threshold=500, rate=22050, chunk=1024):
    # Initialize PyAudio
    audio = pyaudio.PyAudio()

    # Open stream
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=rate,
                        input=True, frames_per_buffer=chunk)

    frames = []
    silent_frames = 0
    started = False

    try:
        while True:
            # Read audio data
            data = stream.read(chunk)
            audio_data = np.frombuffer(data, dtype=np.int16)

            # Check if there is sound input
            if np.max(audio_data) > threshold:
                if not started:
                    print("Recording started.")
                    started = True
                silent_frames = 0
            elif started:
                silent_frames += 1

            # Record audio if recording has started
            if started:
                frames.append(data)

            # Stop recording if there is no sound input for specified duration
            if started and silent_frames >= duration * (rate / chunk):
                print("Recording stopped.")
                break

    except KeyboardInterrupt:
        pass
    finally:
        # Close the stream
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # Save the recorded audio to a WAV file
        with wave.open(file_path, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(rate)
            wf.writeframes(b''.join(frames))

        print(f"Audio saved to {file_path}")





def download_result_from_gcs(bucket_name, source_blob_name, destination_file_path):
    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Get the blob
    blob = bucket.blob(source_blob_name)

    # Download the file to the specified destination
    blob.download_to_filename(destination_file_path)

    print(f"File downloaded from gs://{bucket_name}/{source_blob_name} to {destination_file_path}")

    # Delete the file from Google Cloud Storage
    blob.delete()

    print(f"File gs://{bucket_name}/{source_blob_name} deleted.")




def upload_wav_to_gcs(file_path, bucket_name, destination_blob_name):
    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket
    bucket = storage_client.bucket(bucket_name)

    # Create a blob with the specified destination blob name
    blob = bucket.blob(destination_blob_name)

    # Upload the local file to GCS
    blob.upload_from_filename(file_path)

    print(f"File {file_path} uploaded to gs://{bucket_name}/{destination_blob_name}")

    
def is_file_exist(bucket_name, file_name):

    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob.exists()

def audio_client(file_path = 'test.wav', bucket_name = 'haoyuh3', destination_blob_name = 'example.wav'):

    while True:

        record_audio("test.wav", rate=22050)

        upload_wav_to_gcs(file_path, bucket_name, destination_blob_name)

        while True:
            source_blob_name = 'result.txt'
            destination_file_path = 'result.txt'
            if(is_file_exist(bucket_name, source_blob_name) == False):
                print("waiting for result file")
                continue
            else:
                download_result_from_gcs(bucket_name, source_blob_name, destination_file_path)
                break

        with open('result.txt', 'r') as f:
            result = f.read()

        if(result in ['haoyu', 'cyhh']):
            print("The result is: ", result)
            return result
        else: text_to_speech("you have no access to pi")
            
        

# clean the bucket prepare for the next call
def delete_all_blob(bucket_name):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blobs = bucket.list_blobs()
    for blob in blobs:
        blob.delete()


def download_blob_client(bucket_name, source_blob_name, destination_file_name, count):
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

        #print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
        print("receive response")
        with open(destination_file_name, "r") as audio_file:
            audio_text = audio_file.read().strip()
            
        print("pi start to talk")
        text_to_speech(audio_text)
        
        return count + 1


def upload_blob_client(bucket_name, source_file_name, destination_blob_name,count):
    """Uploads a file to the bucket."""
    # initialize
    client = storage.Client()

    
    bucket = client.get_bucket(bucket_name)

   
    if(count != 0):
        blob = bucket.blob(f"temp_data{count-1}.txt")
        blob.delete()

    # construct blob
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    
    #print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")



def main(audio = False):
    # bucket name
    audio_detection = audio
    if(audio_detection):
        names = audio_client()
        print(names)
    
    else:   
        names = face_detection()
#         if(len(names)>1):
#             text_to_speech("hi, haoyu and honghui")
        names =",".join(names)
    if(names=="cyhh"): text_to_speech("hi, honghui")
    else: text_to_speech(f"hi, {names}")
    print(names)

    bucket_name = "haoyuh3"
    destination_file_name = "process_file.txt"  #
    count = 0  # counter
    
    while True:
        # receive data
        try:

            data = transcribe_audio()
            # if(data == "quit"):
            #     break

            if data is None: continue
            
            # write data
            with open("temp_data.txt", "w") as f:
                f.write(data)
            
            # upload to drive
            upload_blob_client(bucket_name, "temp_data.txt", f"temp_data{count}.txt",count)

            while True:
                source_blob_name = f"process_data{count}.txt"  #
                new_count = download_blob_client(bucket_name, source_blob_name, destination_file_name, count)

                if(new_count == count+1):
                    count = new_count 
                    break
                print("Waiting for response")

        except KeyboardInterrupt:
            print("KeyboardInterrupt detected. Exiting...")
            delete_all_blob(bucket_name)
            print("Bucket cleaned.")
            break


  



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script with optional audio argument")
    parser.add_argument("--audio", type=bool, nargs='?', const=True, default=False, help="Enable audio")

    args = parser.parse_args()
    main(args.audio)

    


        

        
        
       


