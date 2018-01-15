from app import db
from app.models import Article, User, Video, Question, Answer, Comment

# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# admin
admin_user = User(username="admin", email='gistkaist@gmail.com', plaintext_password='kaistgist', role='admin')
db.session.add(admin_user)

sample_user = User(username="sample_user", email='sample@gmail.com', plaintext_password='sample', role='user')
sample_user.email_confirmed = True
db.session.add(sample_user)

# Commit
db.session.commit()

# insert article data
article1 = Article('Welcome to Gist', "For those of us who love to read, not having enough time to even make a dent "
                                      "in everything that we would want to know about the world that we live in has "
                                      "been a bane of our existence. Even those among us that manage to read more "
                                      "than the others end up forgetting most of what we read. \n\n In an attempt to "
                                      "solve this problem we are suggesting a platform in which people can make a "
                                      "video or written summary of the book that they read and upload it on a website "
                                      "that we call Gist to share it with other people or simply creating a library "
                                      "for themselves while the material is still fresh in their mind. \n\n Join the "
                                      "website and watch the video summaries of the book that you wanted to read but "
                                      "didn't have the time,  and if you can’t find it or you think it does not "
                                      "capture the book fully, then join your friends and other people on the website "
                                      "that are interested in the book and make a summary of the book. "
                   , admin_user.id)
article2 = Article('Markdown Guide',
                   "## Lists\n\nUnordered lists can be started using the toolbar or by typing `* `, `- `, or `+ `. "
                   "Ordered lists can be started by typing `1. `.\n\n#### Unordered\n* Lists are a piece of cake\n* "
                   "They even auto continue as you type\n* A double enter will end them\n* Tabs and shift-tabs work "
                   "too\n\n#### Ordered\n1. Numbered lists...\n2. ...work too!\n\n## What about images?\n![Yes]("
                   "https://i.imgur.com/sZlktY7.png) "
                   , admin_user.id)
article3 = Article('I Love Pintos', "Pintos is beautiful ^^"
                   , sample_user.id)

db.session.add(article1)
db.session.add(article2)
db.session.add(article3)

# insert video data
video1 = Video('Big Bunny 1', '2MB', '2mb.mp4', admin_user.id)
video2 = Video('Big Bunny 2', '5MB', '5mb.mp4', admin_user.id)
video3 = Video('Big Bunny 3', '10MB', '10mb.mp4', admin_user.id)

db.session.add(video1)
db.session.add(video2)
db.session.add(video3)

# Commit
db.session.commit()

# insert forum data
question1 = Question('Build agent ID via TFS sdk',
                     'I am using the TFS2018 api and I need to get the build agent id for different team projects. '
                     'How can I get the list of agent queue ids using the TFS sdk?',
                     admin_user.id)

answer1 = Answer('Using a transaction', question1.id, admin_user.id)
answer2 = Answer(
    'Your question is difficult to follow, but I\'ll try: It looks like you are using php to dump values in your form '
    'via PHP before you load the values later with your include statement.',
    question1.id, admin_user.id)

question1.answers = [answer1, answer2]

db.session.add(question1)

# insert comments
comment1 = Comment("this is one comment", admin_user.id)
comment1.set_article_id(article1.id)

comment2 = Comment("this is a **second** comment", sample_user.id)
comment2.set_video_id(video1.id)

db.session.add(comment1)
db.session.add(comment2)

# Commit
db.session.commit()
