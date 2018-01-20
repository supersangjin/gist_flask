import os
from app import db
from instance.config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
from flask import request, redirect, url_for, flash, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import Video, User, Comment, Category
from .forms import UploadVideoForm
from . import videos_blueprint


@videos_blueprint.route('/video')
def index():
    all_videos = Video.query.all()
    return render_template('videos/list.html', videos=all_videos)


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
                                  filename=filename, category_id=form.video_category.data)
                db.session.add(new_video)
                db.session.commit()
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                flash('New Video, {}, uploaded!'.format(new_video.video_title), 'success')
                video_with_user = db.session.query(Video, User, Category).join(User, Category).filter(
                    Video.id == new_video.id).first()
                return render_template('videos/video_detail.html', video=video_with_user)
    return render_template('videos/upload_video.html', form=form)


@videos_blueprint.route('/video/<video_id>')
def video_details(video_id):
    video_with_user = db.session.query(Video, User, Category).join(User, Category).filter(Video.id == video_id).first()
    if video_with_user is not None:
        return render_template('videos/video_detail.html', video=video_with_user)
    else:
        flash('Error! Video does not exist.', 'error')
    return redirect(url_for('videos.index'))


@videos_blueprint.route('/video/<video_id>/comment/add', methods=['GET', 'POST'])
def add_comment(video_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        comment_context = data['comment_context']
        new_comment = Comment(comment_context, current_user.id)
        new_comment.set_video_id(video_id)
        db.session.add(new_comment)
        db.session.commit()
    all_comments = db.session.query(Comment).filter(Comment.video_id == video_id)
    result_list = []
    for comment in all_comments:
        author = db.session.query(User).filter(User.id == comment.user_id).first()
        result_list.append(
            {
                "id": comment.id,
                "comment_context": comment.comment_context,
                "comment_like": comment.comment_like,
                "comment_creDate": comment.comment_creDate,
                "author": author.username,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    result_list.reverse()
    return jsonify(result_list)


# helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

