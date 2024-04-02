from google.cloud import storage
import os

# api
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "cre2.json"


def download_blob_client(bucket_name, source_blob_name, destination_file_name, count):
    """Downloads a blob from the bucket if it exists."""
    # initialize
    client = storage.Client()

    # get specific bucket
    bucket = client.get_bucket(bucket_name)

    # exist
    blob = bucket.blob(source_blob_name)
    if not blob.exists():
        print(f"Blob {source_blob_name} does not exist in {bucket_name}.")
        return count

    # download file
    else:
        blob.download_to_filename(destination_file_name)

        print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
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

    print(f"File {source_file_name} uploaded to {destination_blob_name} in {bucket_name}.")



if __name__ == "__main__":
    # bucket name
    bucket_name = "haoyuh3"
    destination_file_name = "process_file.txt"  #
    count = 0  # counter
    
    while True:
        # receive data
        data = input("Enter data: ")
        if(data == "quit"):
            break
        
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



    
    ## auto destroy all the file in cloud ??  slow down?

        

        
        
       


