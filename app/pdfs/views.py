import os
from app import db
from instance.config import ALLOWED_EXTENSIONS_PDF, UPLOAD_FOLDER_PDF
from flask import request, redirect, url_for, flash, render_template, jsonify, session
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from app.models import Pdf, User, Comment, Category, Book
from .forms import UploadPdfForm
from . import pdfs_blueprint
from ..books import googleBook

PDF_LIMIT = 4

@pdfs_blueprint.route('/pdf')
def index():
    all_pdfs = db.session.query(Pdf, User, Book, Category).join(User, Book).filter(Category.id == Book.category_id).limit(PDF_LIMIT)
    return render_template('pdfs/list.html', pdfs=all_pdfs)


@pdfs_blueprint.route('/pdf/add', methods=['GET', 'POST'])
@login_required
def upload_pdf():
    user = current_user
    if not user.email_confirmed:
        flash('Your email address must be confirmed to upload files.', 'error')
        return redirect(url_for('pdfs.index'))
    form = UploadPdfForm(request.form)
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
                file.save(os.path.join(UPLOAD_FOLDER_PDF, filename))

                # check book if its in our db
                if db.session.query(Book).filter(Book.isbn == form.pdf_isbn.data).count():
                    book = db.session.query(Book).filter(Book.isbn == form.pdf_isbn.data).first()
                else:  # TODO request google book api
                    book = googleBook.search_isbn(form.pdf_isbn.data)

                new_pdf = Pdf(title=form.pdf_title.data, filename=filename, user_id=user.id, book_id=book.id, description=form.pdf_description.data, thumbnail=book.thumbnail)
                db.session.add(new_pdf)
                db.session.commit()
                flash('New file, {}, uploaded!'.format(new_pdf.pdf_title), 'success')
                pdf_with_user = db.session.query(Pdf, User, Book, Category)\
                    .join(User)\
                    .join(Book)\
                    .join(Category)\
                    .filter(Pdf.id == new_pdf.id).first()
                return render_template('pdfs/pdf_detail.html', pdf=pdf_with_user)
    return render_template('pdfs/upload_pdf.html', form=form)


@pdfs_blueprint.route('/pdf/<pdf_id>')
def pdf_details(pdf_id):
    pdf_with_user = db.session.query(Pdf, User, Category, Book).join(User, Book).filter(Pdf.id == pdf_id, Category.id == Book.category_id).first()
    if pdf_with_user is not None:
        visited = session.get('pdf' + pdf_id, '')
        if visited == '':  # 이번 세션동안 방문한적 없음
            session['pdf' + pdf_id] = "visited"
            pdf_with_user.Pdf.pdf_hit += 1
            db.session.commit()
        return render_template('pdfs/pdf_detail.html', pdf=pdf_with_user, current_user_id=current_user.id)
    else:
        flash('Error! File does not exist.', 'error')
    return redirect(url_for('pdfs.index'))


@pdfs_blueprint.route('/pdf/<pdf_id>/comment/add', methods=['GET', 'POST'])
def add_comment(pdf_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        comment_context = data['comment_context']

        # new comment added
        new_comment = Comment(comment_context, current_user.id)
        new_comment.set_pdf_id(pdf_id)

        # pdf comment num += 1
        pdf = db.session.query(Pdf).filter(Pdf.id == pdf_id).first()
        pdf.add_comment()

        db.session.add(new_comment)
        db.session.commit()
    all_comments = db.session.query(Comment).filter(Comment.pdf_id == pdf_id)
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
                "author_id": author.id,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    result_list.reverse()
    return jsonify(result_list)


@pdfs_blueprint.route('/pdf/<pdf_id>/comment/delete', methods=['POST'])
def delete_comment(pdf_id):
    if request.method == 'POST':
        data = request.form.to_dict()
        comment_id = data['id']
        # delete comment
        comment = db.session.query(Comment).filter(Comment.id == comment_id).first()

        if current_user.id == comment.user_id:
            # pdf comment num -= 1
            pdf = db.session.query(Pdf).filter(Pdf.id == pdf_id).first()
            pdf.delete_comment()

            db.session.delete(comment)
            db.session.commit()

    all_comments = db.session.query(Comment).filter(Comment.pdf_id == pdf_id)
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
                "author_id": author.id,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    result_list.reverse()
    return jsonify(result_list)



# helper functions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_PDF

