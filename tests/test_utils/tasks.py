import os


def upload_test_file(client, filename='test.jpg'):
    """
    Uploads a file from data dir to the client.
    :param client: where the file should be uploaded to
    :param filename: name of the test file
    """
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data/example.jpg')
    file = open(path, 'rb')
    data = dict(file=(file, filename))
    client.post('/upload',
                content_type='multipart/form-data',
                data=data)
    file.close()
