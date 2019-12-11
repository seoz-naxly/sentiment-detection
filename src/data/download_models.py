import requests
import os

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"
    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
    else:
        print("Could not download file")

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                
if __name__ == "__main__":
    file_ids = ['1S8fwDPEGQET5haFZ-FQlYboPjsPkdoIp', '11JWj0uy-X27L-6Hzoi1ZE73ieBkvzhPe']
    filenames = ["lstm_11.pth", "net_9.pth"]
    for file_id, filename in zip(file_ids, filenames):
        destination = os.path.join(os.path.realpath(os.path.dirname(__file__)), os.path.join(os.path.dirname(__file__), "../../data/models/{}".format(filename)))
        download_file_from_google_drive(file_id, destination)