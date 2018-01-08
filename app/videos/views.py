import os
from app import db
from instance.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import Video, User
from .forms import UploadVideoForm
from . import videos_blueprint


@videos_blueprint.route('/video')
def index():
    all_videos = Video.query.all()
    return render_template('videos/videos.html', videos=all_videos)


@videos_blueprint.route('/video/add', methods=['GET', 'POST'])
@login_required
def upload_video():
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to upload videos.', 'error')
        return redirect(url_for('videos.index'))
    form = UploadVideoForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part', 'error')
                return redirect(request.url)
            file = request.files['file']
            # if user does not select file, browser also
            # submit a empty part without filename
            if file.filename == '':
                flash('No selected file', 'error')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                new_video = Video(title=form.video_title.data, description=form.video_description.data, user_id=user.id,
                                  filename=filename)
                db.session.add(new_video)
                db.session.commit()
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('New Video, {}, uploaded!'.format(new_video.video_title), 'success')
                video_with_user = db.session.query(Video, User).join(User).filter(Video.id == new_video.id).first()
                return render_template('video_detail.html', video=video_with_user)
    return render_template('videos/upload_video.html', form=form)


@videos_blueprint.route('/video/<video_id>')
def video_details(video_id):
    video_with_user = db.session.query(Video, User).join(User).filter(Video.id == video_id).first()
    if video_with_user is not None:
        return render_template('videos/video_detail.html', video=video_with_user)
    else:
        flash('Error! Video does not exist.', 'error')
    return redirect(url_for('videos.index'))


# helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

