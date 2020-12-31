import hashlib
from concurrent.futures.thread import ThreadPoolExecutor

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet
from werkzeug.exceptions import abort

from family_foto import File, db, log
from family_foto.const import MAX_UPLOAD_WORKERS
from family_foto.errors import UploadError
from family_foto.models.photo import Photo
from family_foto.models.user import User
from family_foto.models.video import Video

VIDEOS = ('mp4',)
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEOS)


class UploadService:
    """
    Handles uploads of media files.
    """

    def __init__(self, files: [File], user_id: [int, None]):
        """
        :param files: is a list of files to be uploaded.
        :param user_id: optional. If not given the program will check for a
        current_user instance. If that is not given it cannot upload the file.
        """
        self._files = files
        if user_id is None and current_user.is_authenticated:
            self._user = current_user
        elif user_id is not None:
            self._user = User.query.get(user_id)
        else:
            raise UploadError(filename=self._files[0].filename,
                              message='Could not associate user to files.')

    def upload(self) -> None:
        """
        Starts uploading the all files.
        """
        with ThreadPoolExecutor(max_workers=MAX_UPLOAD_WORKERS) as executor:
            executor.map(self._upload_file, self._files)

    def _upload_file(self, file):
        """
        Uploads one file to the server.
        :param file: to be uploaded
        """
        log.info(f'Start uploading {file.filename}')
        exists: File = File.query.filter_by(filename=file.filename).first()
        file_content = file.stream.read()
        file_hash = hashlib.sha3_256(file_content).hexdigest()
        file.stream.seek(0)
        if exists and file_hash == exists.hash:
            raise UploadError(exists.filename, f'File already exists: {exists.filename}')
        sub_folder = f'{file_hash[:2]}/{file_hash}'
        if 'image' in file.content_type:
            filename = photos.save(file, folder=sub_folder).split('/')[-1]
            photo = Photo(filename=filename, user=self._user.id,
                          hash=file_hash)
            db.session.add(photo)
        elif 'video' in file.content_type:
            filename = videos.save(file, folder=sub_folder).split('/')[-1]
            video = Video(filename=filename, user=self._user.id,
                          hash=file_hash)
            db.session.add(video)
        else:
            abort(400, f'file type {file.content_type} not supported.')
        db.session.commit()
        log.info(f'{self._user.username} uploaded {filename}')
