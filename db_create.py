from app.models import *

# drop all of the existing database tables
db.reflect()
db.drop_all()

# create the database and the database table
db.create_all()

# insert admin
admin_user = User(username="admin", email='gistkaist@gmail.com', plaintext_password='kaistgist', role='admin')
sample_user = User(username="sample_user", email='sample@gmail.com', plaintext_password='sample', role='user')
sample_user.email_confirmed = True
sample_user.set_thumbnail("user-sample.jpeg")
sample_user.set_description("Hello I am sample user hahahahaha")

db.session.add(admin_user)
db.session.add(sample_user)

# Commit
db.session.commit()


# insert category data
CATEGORY = [{'name':'career & money', 'icon':'money-bill-alt'},
        {'name':'personal growth', 'icon':'users'},
        {'name':'science & tech', 'icon':'flask'},
        {'name':'health & fitness', 'icon':'heartbeat'},
        {'name':'lifestyle', 'icon':'utensils'},
        {'name':'entertainment', 'icon':'gamepad'},
        {'name':'biographies & history', 'icon':'history'},
        {'name':'fiction', 'icon':'bookmark'}]

for category in CATEGORY:
    db.session.add(Category(category['name'], category['icon']))

# Commit
db.session.commit()

book0 = Book("0", "Book not found", "", "https://hoursofidleness.files.wordpress.com/2012/06/gray-card.jpg", "invalid isbn", 1)
db.session.add(book0)
db.session.commit()


"""
# insert book
book0 = Book("0", "Book not found", "", "http://andrewcmaxwell.com/wp-content/themes/acm_2014/images/book_not_found.png", "invalid isbn", 1)
book1 = Book("1328683788", "Tools of Titans", "Timothy Ferriss", "http://books.google.com/books/content?id=gjuvDAEACAAJ&printsec=frontcover&img=1&zoom=1&source=gbs_api", "description 1", 1)
book2 = Book("0439136369", "Harry Potter And The Chamber Of Secrets", "J. K. Rowling", "https://images-na.ssl-images-amazon.com/images/I/51NbOxBO%2BBL._SL160_.jpg", "Harry Potter Great", 2)

db.session.add(book0)
db.session.add(book1)
db.session.add(book2)

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
article4 = Article('Yo Soy Sujin', "I learned Spanish"
                   , sample_user.id)

db.session.add(article1)
db.session.add(article2)
db.session.add(article3)
db.session.add(article4)


# insert pdfs
pdf1 = Pdf('Hello Operating System', 'The process of the CS330 course is covered.', 'cs330.pdf', '1.jpg', admin_user.id, 1)
pdf2 = Pdf('I hate Inipay', 'Fucking Inipay', 'INIpay.pdf', '2.jpeg', sample_user.id, 2)
pdf3 = Pdf('Cool resume', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 1)
pdf4 = Pdf('This is sample for PDF', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', sample_user.id, 3)
pdf5 = Pdf('Sublime text, file, edit, selection, find, view, goto.', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 1)
pdf6 = Pdf('siba daeng-daeng-i', 'Resume of Sangjin', 'Resume.pdf', '1.jpg', sample_user.id, 2)
pdf7 = Pdf('head shoulder knee', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 1)
pdf8 = Pdf('Loreal professional paris', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 3)
pdf9 = Pdf('sample1', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 3)
pdf10 = Pdf('sample2', 'Resume of Sangjin', 'Resume.pdf', '1.jpg', sample_user.id, 2)
pdf11 = Pdf('sample3', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 3)
pdf12 = Pdf('sample4', 'Resume of Sangjin', 'Resume.pdf', '2.jpeg', admin_user.id, 1)

db.session.add(pdf1)
db.session.add(pdf2)
db.session.add(pdf3)
db.session.add(pdf4)
db.session.add(pdf5)
db.session.add(pdf6)
db.session.add(pdf7)
db.session.add(pdf8)
db.session.add(pdf9)
db.session.add(pdf10)
db.session.add(pdf11)
db.session.add(pdf12)

# Commit
db.session.commit()

# insert chat
chat1 = Chat("My name is Sangjin", admin_user.id)
chat2 = Chat("Hello. Nice to meet you", sample_user.id)
chat3 = Chat("Pintos is beautiful", admin_user.id)

db.session.add(chat1)
db.session.add(chat2)
db.session.add(chat3)

# Commit
db.session.commit()"""
