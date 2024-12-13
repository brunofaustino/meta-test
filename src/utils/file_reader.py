import os

def list_json_files(directory):
    return [os.path.join(directory, file) for file in os.listdir(directory) if file.endswith(".json")]
