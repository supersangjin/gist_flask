from flask import render_template, request, redirect, url_for, flash, session
from .forms import *
from flask_login import current_user
from . import chat_blueprint


@chat_blueprint.route('/chat', methods=['GET', 'POST'])
def index():
    """Login form to enter a room."""
    form = ChatForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        return redirect(url_for('.chat'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
        form.room.data = session.get('room', '')
    return render_template('chat/rooms.html', form=form)


@chat_blueprint.route('/chat/room')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat/chat.html', name=name, room=room)