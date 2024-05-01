from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cre2.json"

import pyaudio
import wave
import numpy as np
import sys
os.close(sys.stderr.fileno())

def record_audio(file_path, duration=4, threshold=250, rate=22050, chunk=1024):
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
        

if __name__ == "__main__":
    # bucket name
    audio_detection = True
    if(audio_detection):
        print("1")
        names = audio_client()
        print(names)