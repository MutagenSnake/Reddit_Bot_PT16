from tkinter import *
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import praw
import time
import webbrowser
import pickle
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

engine0 = create_engine('sqlite:///Reddit_bot_comments.db')
Base0 = declarative_base()
Session0 = sessionmaker(bind=engine0)
session0 = Session0()

''' Classes'''

class Reddid_Class_Comments(Base0):
    __tablename__ = 'Reddit post'
    id = Column(Integer, primary_key=True)
    target_comment = Column('Target comment', String)
    target_comment_id = Column('Comment id', String)
    target_comment_url = Column('Comment url', String)
    time = Column('Comment register time', DateTime, default=datetime.datetime.now)

    def __init__(self, target_comment, target_comment_id, target_comment_url):
        self.target_comment = target_comment
        self.target_comment_id = target_comment_id
        self.target_comment_url = target_comment_url

    def __repr__(self):
        return f'{self.id},{self.target_comment},{self.target_comment_id},{self.target_comment_url}'

if __name__ == '__main__':
    Base0.metadata.create_all(engine0)

''' Functions '''

def pull_bot_comments():
    return session0.query(Reddid_Class_Comments).all()

def pull_comment_url_from_database():
    return session0.query(Reddid_Class_Comments.target_comment_url).all()

def pull_from_database_for_comment_id():
    return session0.query(Reddid_Class_Comments.target_comment_id).all()

def reddit_comment_id_convert_to_database_string(commnet_id_string):
    return f"('{commnet_id_string}',)"

def check_if_commented(comment_id):
    database_comment_ids = pull_from_database_for_comment_id()
    database_comment_ids_normalised = []
    sub_id_converted = reddit_comment_id_convert_to_database_string(comment_id)
    for element in database_comment_ids:
        database_comment_ids_normalised.append(str(element))
    if sub_id_converted not in database_comment_ids_normalised:
        return False
    else:
        return True


def make_a_comment():
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

    logger.info(f'Bot connected to Reddit')

    subreddit = reddit.subreddit(entry_name.get())
    search_string = reddit.subreddit(entry_search.get())
    comment_string = reddit.subreddit(entry_comment.get())

    try:
        for submission in subreddit.hot(limit=20):
            with open('last_comment_time.pkl', 'rb') as f:
                last_comment_time = pickle.load(f)
            # last_comment_time = datetime.datetime.now() - datetime.timedelta(days=1)

            if datetime.datetime.now() - last_comment_time > datetime.timedelta(minutes=10):
                for top_level_comment in submission.comments:
                    if hasattr(top_level_comment, "body"):
                        comment_search = top_level_comment.body
                        if str(search_string) in comment_search:
                            comment_body = top_level_comment.body
                            comment_id = top_level_comment.id
                            comment_url = top_level_comment.permalink
                            full_comment_url = f'https://www.reddit.com/{comment_url}'
                            if check_if_commented(comment_id) is True:
                                print('Already commented, skipping')
                                label_status["text"] = "Commented already"
                                break
                            else:
                                database_input = Reddid_Class_Comments(comment_body, comment_id, full_comment_url)
                                session0.add(database_input)
                                session0.commit()
                                # comment.reply(comment_string)
                                logger.info(f'Comment posted. Commented on "{comment_body}", comment id: {comment_id}')
                                box.delete(0, 'end')
                                box.insert(END, *pull_bot_comments())
                                label_status["text"] = "Comment posted - timeout 10min"
                                time_of_posting = datetime.datetime.now()
                                f = open("last_comment_time.pkl", "wb")
                                pickle.dump(time_of_posting, f)
                                raise StopIteration
                        else:
                            label_status["text"] = "Nothing to comment upon"

            else:
                label_status["text"] = f"Too early. Time since the last comment: {datetime.datetime.now() - last_comment_time}"
                raise StopIteration
    except StopIteration:
        pass

''' Graphics '''

bot_window = Tk()

def open_comment_url():
    search_string = str(pull_comment_url_from_database()[box.curselection()[0]])
    search_string_1 = search_string[2:]
    search_string_2 = search_string_1[:-3]
    webbrowser.open(search_string_2)
    label_status["text"] = "Web browser opened"


bot_window.title("Reddit bot")

scrollbar = Scrollbar(bot_window)
box = Listbox(bot_window, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=box.yview)

box.insert(END, *pull_bot_comments())

label_0 = Label(bot_window, text='Enter subreddit:', width=20)
label_1 = Label(bot_window, text='Search for:', width=20)
label_2 = Label(bot_window, text='The comment:', width=20)
label_status = Label(bot_window, text="Window open")
label_top = Label(bot_window, text='Commented comments')

entry_name = Entry(bot_window, width=20)
entry_search = Entry(bot_window, width=20)
entry_comment = Entry(bot_window, width=20)

button0 = Button(bot_window, text="Initiate", command=make_a_comment)
button1 = Button(bot_window, text="Open", command=open_comment_url)

''' Visual '''

label_0.grid(row=0, column=0)
entry_name.grid(row=1, column=0)
label_1.grid(row=2, column=0)
entry_search.grid(row=3, column=0)
label_2.grid(row=4, column=0)
entry_comment.grid(row=5, column=0)

button0.grid(row=6, column=0)
button1.grid(row=7, column=0)

label_top.grid(row=0, column=1, columnspan=3, sticky=W + E)
label_status.grid(row=8, columnspan=3, sticky=W + E)

box.grid(row=1, rowspan=6, column=2)

scrollbar.grid(row=0, rowspan=7, column=4, sticky=N + S)

bot_window.mainloop()