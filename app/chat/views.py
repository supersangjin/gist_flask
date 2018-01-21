from flask import request, jsonify
from flask_login import current_user

from app import db
from . import chat_blueprint
from app.models import Chat, User


@chat_blueprint.route('/chat/add', methods=['GET', 'POST'])
def add_chat():
    if request.method == 'POST':
        data = request.form.to_dict()
        chat_context = data['comment_context']
        new_chat = Chat(chat_context, current_user.id)
        db.session.add(new_chat)
        db.session.commit()
    all_chats = Chat.query.all()
    result_list = []
    # TODO limit 두기
    for chat in all_chats:
        author = db.session.query(User).filter(User.id == chat.user_id).first()
        result_list.append(
            {
                "id": chat.id,
                "comment_context": chat.chat_context,
                "comment_creDate": chat.chat_creDate,
                "author": author.username,
                "author_id": author.id,
                "author_thumbnail": "http://127.0.0.1:5000/static/image/user/" + author.thumbnail
            }
        )
    return jsonify(result_list)





























"""
@chat_blueprint.route('/chat', methods=['GET', 'POST'])
def index():
    Login form to enter a room.
    form = ChatForm()
    if form.validate_on_submit():
        session['name'] = current_user.username
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
    return render_template('chat/rooms.html', form=form)


@chat_blueprint.route('/chat/room')
def chat():
    Chat room. The user's name and room must be stored in
    the session.
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat/chat.html', name=name, room=room)
"""