import asyncio
import hashlib
import os
from concurrent.futures.thread import ThreadPoolExecutor
from sqlite3 import OperationalError
from typing import List, Optional

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet
from werkzeug.datastructures import FileStorage

from family_foto.const import MAX_UPLOAD_WORKERS
from family_foto.errors import UploadError
from family_foto.logger import log
from family_foto.models.file import File
from family_foto.models.photo import Photo
from family_foto.models.user import User
from family_foto.models.video import Video
from family_foto.services.thumbnail_service import generate_all
from family_foto.utils.session import create_session

VIDEOS = ('mp4',)
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEOS)


# pylint: disable=too-few-public-methods
class UploadService:
    """
    Handles uploads of media files.
    """

    def __init__(self, files: List[FileStorage], user_id: Optional[int], app):
        """
        :param files: is a list of files to be uploaded.
        :param user_id: optional. If not given the program will check for a
        current_user instance. If that is not given it cannot upload the file.
        """
        self._app = app
        self._files = files
        if user_id is None and current_user.is_authenticated:
            self._user = current_user
        elif user_id is not None and User.query.get(user_id) is not None:
            self._user = User.query.get(user_id)
        else:
            message = 'Could not associate user to files.'
            log.warning(message)
            filename = self._files[0].filename if self._files else 'No file given'
            raise UploadError(filename=filename,
                              message=message)

    def upload(self) -> List[Optional[UploadError]]:
        """
        Starts uploading the all files.
        """
        with ThreadPoolExecutor(max_workers=MAX_UPLOAD_WORKERS) as executor:
            results = list(executor.map(self._upload_file, self._files))
            executor.shutdown(wait=True)
            file_ids = [response for response in results if isinstance(response, int)]
            loop = asyncio.new_event_loop()
            task = loop.create_task(generate_all(file_ids, 200, 200))
            loop.run_until_complete(task)
            return [response for response in results if not isinstance(response, int)]

    def _upload_file(self, file):
        """
        Uploads one file to the server.
        :param file: to be uploaded
        """
        log.info(f'Start uploading {file.filename}')
        # this is intentional to shadow the outer scope package
        # pylint: disable=invalid-name
        Session, session = create_session(self._app)
        exists = session.query(File).filter_by(filename=file.filename).first()
        file_content = file.stream.read()
        file_hash = hashlib.sha3_256(file_content).hexdigest()
        file.stream.seek(0)

        if exists and file_hash == exists.hash:
            message = f'File already exists: {exists.filename}'
            log.info(message)
            Session.remove()
            return UploadError(exists.filename, message)
        sub_folder = f'{file_hash[:2]}/{file_hash}'
        if 'image' in file.content_type:
            saved_file = self._upload_photo(file, file_hash, session, sub_folder)
        elif 'video' in file.content_type:
            saved_file = self._upload_video(file, file_hash, session, sub_folder)
        else:
            message = f'file type {file.content_type} not supported.'
            log.info(message)
            Session.remove()
            return UploadError(filename=file.filename, message=message)
        file_id = self._try_commit_file(Session, file, saved_file, session)
        return file_id

    # this is intentional to shadow the outer scope package
    # pylint: disable=invalid-name
    def _try_commit_file(self, Session, file, saved_file, session):
        response = None
        try:
            session.commit()
            response = saved_file.id
            log.info(f'{self._user.username} uploaded {file.filename}')
        except OperationalError as op_error:
            session.rollback()
            log.error(op_error)
            response = UploadError(file.filename, 'There was a database error. See log for more '
                                                  'information.')
        finally:
            session.close()
            Session.remove()
        return response

    def _upload_video(self, file, file_hash, session, sub_folder):
        with self._app.app_context():
            path = self._app.config['UPLOADED_VIDEOS_DEST']
            final_path = os.path.join(path, sub_folder, file.filename)
            if not os.path.exists(final_path):
                os.makedirs(os.path.dirname(final_path))
            file.save(dst=final_path)
        video = Video(filename=file.filename, user=self._user.id,
                      hash=file_hash)
        session.add(video)
        return video

    def _upload_photo(self, file, file_hash, session, sub_folder):
        with self._app.app_context():
            path = self._app.config['UPLOADED_PHOTOS_DEST']
            final_path = os.path.join(path, sub_folder, file.filename)
            dirname = os.path.dirname(final_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            file.save(dst=final_path)
        photo = Photo(filename=file.filename, user=self._user.id,
                      hash=file_hash)
        session.add(photo)
        return photo
