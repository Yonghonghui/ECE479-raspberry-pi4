
import numpy as np
from google.cloud import storage
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cre2.json"
import librosa
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras import layers, models, utils
import tensorflow as tf
from tensorflow import keras

# Function to extract MFCC features from audio files
def extract_features(file_path, mfcc=True, chroma=True, mel=True,sr=22050):
    audio_data, _ = librosa.load(file_path)  # Load audio data directly without a context manager
    features = []
    if mfcc:
        mfccs = np.mean(librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13), axis=1)
        features.extend(mfccs)
    if chroma:
        chroma = np.mean(librosa.feature.chroma_stft(y=audio_data, sr=sr), axis=1)
        features.extend(chroma)
    if mel:
        mel = np.mean(librosa.feature.melspectrogram(y=audio_data, sr=sr), axis=1)
        features.extend(mel)
    return features


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

def audio_recognition_server(bucket_name = 'haoyuh3', source_blob_name = 'example.wav',  destination_file_path = 'test.wav'):

    while True:
        if(is_file_exist(bucket_name, source_blob_name) == False):
            print("waiting for audio file")
            continue
        else:
            download_result_from_gcs(bucket_name, source_blob_name, destination_file_path)


        # Load the model
        model_path = "speaker_recognition_model_17/speaker_recognition_model"
        model = keras.models.load_model(model_path)
        sr= 22050
        # Define class names
        class_names = ["cyhh","haoyu","stranger"]
        # preprocessing
        test_feature= extract_features("test.wav", mfcc=True, chroma=True, mel=True,sr=22050)
        # test_feature= extract_features("audio_files/haoyu_audio_70.wav", mfcc=True, chroma=True, mel=True,sr=22050)
        
        test_feature= np.array(test_feature)
      
        test_feature= test_feature.reshape(1,153,1)
       

        # Make prediction

        predictions = model.predict(test_feature)
        print(predictions)
        # Post-process predictions (e.g., choose the class with the highest probability)
        predicted_label = np.argmax(predictions)

        print("Predicted label:", class_names[predicted_label])

        file_path = "output.txt"

        # Open the file in write mode ('w')
        with open(file_path, 'w') as file:
            # Write the string to the file
            file.write(class_names[predicted_label])
        
        # Upload the file to Google Cloud Storage
        destination_blob_name = 'result.txt'
        upload_wav_to_gcs(file_path, bucket_name, destination_blob_name)
        print("result uploaded")

        if(class_names[predicted_label] in ['haoyu', 'cyhh']):
            break
def maintest():
    model_path = "speaker_recognition_model/speaker_recognition_model"
    model = keras.models.load_model(model_path)
    sr= 22050
    # Define class names
    class_names = ["cyhh","haoyu","stranger"]
    # preprocessing
    test_feature= extract_features("test.wav", mfcc=True, chroma=True, mel=True,sr=22050)
    # test_feature= extract_features("audio_files/haoyu_audio_70.wav", mfcc=True, chroma=True, mel=True,sr=22050)
    
    test_feature= np.array(test_feature)
    
    test_feature= test_feature.reshape(1,153,1)
    

    # Make prediction

    predictions = model.predict(test_feature)
    print(predictions)
    # Post-process predictions (e.g., choose the class with the highest probability)
    predicted_label = np.argmax(predictions)

    print("Predicted label:", class_names[predicted_label])

    

if __name__ == "__main__":
    maintest()