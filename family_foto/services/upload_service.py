import hashlib

from flask_login import current_user
from flask_uploads import IMAGES, UploadSet
from werkzeug.exceptions import abort

from family_foto import File, db, log
from family_foto.errors import UploadError
from family_foto.models.photo import Photo
from family_foto.models.video import Video

VIDEOS = ('mp4',)
photos = UploadSet('photos', IMAGES)
videos = UploadSet('videos', VIDEOS)


def upload_file(file):
    exists: File = File.query.filter_by(filename=file.filename).first()
    file_content = file.stream.read()
    file_hash = hashlib.sha3_256(file_content).hexdigest()
    file.stream.seek(0)
    if exists and file_hash == exists.hash:
        raise UploadError(exists.filename, f'File already exists: {exists.filename}')
    sub_folder = f'{file_hash[:2]}/{file_hash}'
    if 'image' in file.content_type:
        filename = photos.save(file, folder=sub_folder).split('/')[-1]
        photo = Photo(filename=filename, user=current_user.id,
                      hash=file_hash)
        db.session.add(photo)
    elif 'video' in file.content_type:
        filename = videos.save(file, folder=sub_folder).split('/')[-1]
        video = Video(filename=filename, user=current_user.id,
                      hash=file_hash)
        db.session.add(video)
    else:
        abort(400, f'file type {file.content_type} not supported.')
    db.session.commit()
    log.info(f'{current_user.username} uploaded {filename}')
