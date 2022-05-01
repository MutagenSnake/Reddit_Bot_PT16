from tkinter import *
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import praw
import webbrowser
import subprocess
import logging

''' Logger '''

logger = logging.getLogger(__name__)
file_handler = logging.FileHandler('Log.log')
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

''' Common'''

engine = create_engine('sqlite:///Reddit.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


''' Classes'''

class Reddid_Class(Base):
    __tablename__ = 'Reddit post'
    id = Column(Integer, primary_key=True)
    title = Column('Submission title', String)
    score = Column('Submission score', Integer)
    sub_id = Column('Submission id', String)
    url = Column('Sumission url', String)
    time = Column('Submission register time', DateTime, default=datetime.datetime.now)

    def __init__(self, title, score, sub_id, url):
        self.title = title
        self.score = score
        self.sub_id = sub_id
        self.url = url

    def __repr__(self):
        return f'{self.id},{self.title},{self.score},{self.sub_id},{self.url},{self.time}'

if __name__ == '__main__':
    Base.metadata.create_all(engine)

''' Functions '''

def add_to_database():
    client_id = "JWwTf43anrrDx2WbFjLK6w"
    client_secret = "oBicZXN60VolKeE5OSQ7Hm1q5Guv2A"
    username = "Python_training_bot"
    password = "botbotbotbaigiamasis"
    user_agent = "Paksas bot 1.0 u/Python_training_bot"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    subreddit = reddit.subreddit(entry_name.get())

    logger.info(f'Connected to Reddit')

    for submission in subreddit.hot(limit=5):
        title = submission.title
        score = submission.score
        sub_id = submission.id
        url = submission.url
        submission_input = Reddid_Class(title, score, sub_id, url)
        database_sub_ids = pull_from_database_for_id()
        sub_id_converted = reddit_sub_id_convert_to_database_string(sub_id)
        database_sub_ids_normalised = []
        for element in database_sub_ids:
            database_sub_ids_normalised.append(str(element))
        if sub_id_converted not in database_sub_ids_normalised:
            session.add(submission_input)
            session.commit()
            box.delete(0, 'end')
            box.insert(END, *pull_from_database())
            logger.info(f'Submission {sub_id} added to the database')
        else:
            logger.info(f'Submission {sub_id} skipped. Already in the database')


def pull_from_database():
    return session.query(Reddid_Class).all()

def pull_from_database_for_url():
    return session.query(Reddid_Class.url).all()

def pull_from_database_for_id():
    return session.query(Reddid_Class.sub_id).all()

def open_the_url():
    search_string = str(pull_from_database_for_url()[box.curselection()[0]])
    search_string_1 = search_string[2:]
    search_string_2 = search_string_1[:-3]
    webbrowser.open(search_string_2)
    logger.info(f'submission URL opened: {search_string_2}')

def get_url():
    search_string = str(pull_from_database_for_url()[box.curselection()[0]])
    search_string_1 = search_string[2:]
    search_string_2 = search_string_1[:-3]
    return search_string_2

def identify():
    search_string = str(pull_from_database_for_id()[box.curselection()[0]])
    new_search_string = ''
    for symbol in search_string:
        if symbol == '(':
            continue
        elif symbol == ')':
            continue
        elif symbol == ',':
            continue
        elif symbol == "'":
            continue
        else:
            new_search_string += symbol

    return new_search_string

def reddit_sub_id_convert_to_database_string(original_string):
    return f"('{original_string}',)"

def get_submission_comments():
    client_id = "JWwTf43anrrDx2WbFjLK6w"
    client_secret = "oBicZXN60VolKeE5OSQ7Hm1q5Guv2A"
    username = "Python_training_bot"
    password = "botbotbotbaigiamasis"
    user_agent = "Paksas bot 1.0 u/Python_training_bot"

    reddit = praw.Reddit(client_id=client_id,
                         client_secret=client_secret,
                         username=username,
                         password=password,
                         user_agent=user_agent)

    comment_list = []

    submission = reddit.submission(id=identify())
    for top_level_comment in submission.comments:
        if hasattr(top_level_comment, "body"):
            comment_list.append(top_level_comment.body)

    root = Tk()
    sizex = 600
    sizey = 400
    posx = 40
    posy = 20
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    comments_box = Listbox(root, width=600, height=200)
    comments_box.pack()
    for items in comment_list:
        comments_box.insert(END, items)
    root.mainloop()


def open_bot_file():
    subprocess.call(["python", "commenter.py"])
    logger.info(f'Bot opened')

''' GUI '''

main_window = Tk()

logger.info(f'Program opened.')

main_window.title("Reddit register")

scrollbar = Scrollbar(main_window)
box = Listbox(main_window, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=box.yview)

box.insert(END, *pull_from_database())


label_top = Label(main_window, text='Submission database')
label = Label(main_window, text='Enter subreddit', width=20)

entry_name = Entry(main_window, width=20)

button0 = Button(main_window, text="Enter", command=add_to_database)
button1 = Button(main_window, text="Open", command=open_the_url)
button2 = Button(main_window, text="Comments", command=get_submission_comments)
button3 = Button(main_window, text="BOT", command=open_bot_file)

''' Visual '''
label_top.grid(row=0, column=1, columnspan=3, sticky=W + E)
label.grid(row=1, column=0)
entry_name.grid(row=2, column=0)
button0.grid(row=3, column=0)
button1.grid(row=4, column=0)
button2.grid(row=5, column=0)
button3.grid(row=8, column=0)

box.grid(row=1, rowspan=8, column=2)

scrollbar.grid(row=1, rowspan=8,column=4, sticky=N+S)

main_window.mainloop()
