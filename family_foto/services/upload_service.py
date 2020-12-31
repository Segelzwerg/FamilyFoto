import hashlib
import os
from concurrent.futures.thread import ThreadPoolExecutor

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from werkzeug.exceptions import abort

from family_foto.const import MAX_UPLOAD_WORKERS
from family_foto.errors import UploadError
from family_foto.logger import log
from family_foto.models.file import File
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

    def __init__(self, files: [File], user_id: [int, None], app):
        """
        :param files: is a list of files to be uploaded.
        :param user_id: optional. If not given the program will check for a
        current_user instance. If that is not given it cannot upload the file.
        """
        self._app = app
        self._files = files
        if user_id is None and current_user.is_authenticated:
            self._user = current_user
        elif user_id is not None:
            self._user = User.query.get(user_id)
        else:
            message = 'Could not associate user to files.'
            log.warning(message)
            raise UploadError(filename=self._files[0].filename,
                              message=message)

    def upload(self) -> None:
        """
        Starts uploading the all files.
        """
        with ThreadPoolExecutor(max_workers=MAX_UPLOAD_WORKERS) as executor:
            executor.map(self._upload_file, self._files)
            executor.shutdown(wait=True)

    def _upload_file(self, file):
        """
        Uploads one file to the server.
        :param file: to be uploaded
        """
        log.info(f'Start uploading {file.filename}')
        engine = create_engine(self._app.config['DATABASE_URL_TEMPLATE'])
        session_factory = sessionmaker(bind=engine)
        Session = scoped_session(session_factory)
        session = Session()
        exists = session.query(File).filter_by(filename=file.filename).first()
        file_content = file.stream.read()
        file_hash = hashlib.sha3_256(file_content).hexdigest()
        file.stream.seek(0)

        if exists and file_hash == exists.hash:
            message = f'File already exists: {exists.filename}'
            log.info(message)
            raise UploadError(exists.filename, message)
        sub_folder = f'{file_hash[:2]}/{file_hash}'
        if 'image' in file.content_type:
            with self._app.app_context():
                try:
                    path = self._app.config['UPLOADED_PHOTOS_DEST']
                    final_path = os.path.join(path, sub_folder, file.filename)
                    if not os.path.exists(final_path):
                        os.makedirs(os.path.dirname(final_path))
                    file.save(dst=final_path)
                except Exception as e:
                    log.error(e)
            photo = Photo(filename=file.filename, user=self._user.id,
                          hash=file_hash)
            session.add(photo)
        elif 'video' in file.content_type:
            with self._app.app_context():
                try:
                    path = self._app.config['UPLOADED_VIDEOS_DEST']
                    final_path = os.path.join(path, sub_folder, file.filename)
                    if not os.path.exists(final_path):
                        os.makedirs(os.path.dirname(final_path))
                    file.save(dst=final_path)
                except Exception as e:
                    log.error(e)
            video = Video(filename=file.filename, user=self._user.id,
                          hash=file_hash)
            session.add(video)
        else:
            message = f'file type {file.content_type} not supported.'
            log.info(message)
            abort(400, message)
        session.commit()
        Session.remove()
        log.info(f'{self._user.username} uploaded {file.filename}')
