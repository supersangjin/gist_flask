from app import db
from app.models import Article, User

# drop all of the existing database tables
db.drop_all()

# create the database and the database table
db.create_all()

# admin
admin_user = User(email='gistkaist@gmail.com', plaintext_password='kaistgist', role='admin')
db.session.add(admin_user)

# commit the changes
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
article2 = Article('Markdown Guide', "## Lists\n\nUnordered lists can be started using the toolbar or by typing `* `, `- `, or `+ `. Ordered lists can be started by typing `1. `.\n\n#### Unordered\n* Lists are a piece of cake\n* They even auto continue as you type\n* A double enter will end them\n* Tabs and shift-tabs work too\n\n#### Ordered\n1. Numbered lists...\n2. ...work too!\n\n## What about images?\n![Yes](https://i.imgur.com/sZlktY7.png)"
                   , admin_user.id)

db.session.add(article1)
db.session.add(article2)
# commit the changes
db.session.commit()
