import os
import time
import boto3
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

s3_client = boto3.client('s3')

def upload_to_s3(file_name, bucket, object_name=None):
    if object_name is None:
        object_name = os.path.basename(file_name)

    try:
        print(f"Uploading {file_name} to S3 bucket {bucket}...")
        s3_client.upload_file(file_name, bucket, object_name)
        print(f"Uploaded {file_name} to {bucket} as {object_name}")
    except Exception as e:
        print(f"Error occurred while uploading {file_name}: {e}")

class MyHandler(FileSystemEventHandler):
    def __init__(self, bucket):
        self.bucket = bucket

    def on_created(self, event):
        if event.src_path.endswith('.json'):
            print(f"New JSON file detected: {event.src_path}")
            upload_to_s3(event.src_path, self.bucket)

def start_watching(directory, bucket_name):
    event_handler = MyHandler(bucket_name)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=False)
    observer.start()
    print(f"Monitoring directory: {directory} for new JSON files...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

directory_to_watch = '/Users/helen/Desktop/2024-mini/json_file/'  #change it to your own path
bucket_name = 'ec463game'  #It connect to my AWS account

start_watching(directory_to_watch, bucket_name)
