from tkinter import *
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import praw
import time
import webbrowser

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


# def initiate_bot_window():
#     bot_window = Tk()
#
#     def open_comment_url():
#         search_string = str(pull_comment_url_from_database()[box.curselection()[0]])
#         search_string_1 = search_string[2:]
#         search_string_2 = search_string_1[:-3]
#         webbrowser.open(search_string_2)
#         label_status["text"] = "Web browser opened"
#
#     bot_window.title("Reddit bot")
#     # bot_window.geometry('1000x450')
#
#     scrollbar = Scrollbar(bot_window)
#     box = Listbox(bot_window, width=100, yscrollcommand=scrollbar.set)
#     scrollbar.config(command=box.yview)
#
#     box.insert(END, *pull_bot_comments())
#
#     label = Label(bot_window, text='Enter subreddit', width=20)
#     label_0 = Label(bot_window, text='Commonly used', width=20)
#     label_status = Label(bot_window, text="Window open")
#
#     entry_name = Entry(bot_window, width=20)
#
#     button0 = Button(bot_window, text="Initiate", command=make_a_comment)
#     button1 = Button(bot_window, text="Open", command=open_comment_url)
#     ''' Visual '''
#
#     label.grid(row=0, column=0)
#     entry_name.grid(row=1, column=0)
#     button0.grid(row=2, column=0)
#     label_0.grid(row=3, column=0)
#     button1.grid(row=4, column=0)
#     label_status.grid(row=8, columnspan=3, sticky=W+E)
#
#
#     box.grid(row=0, rowspan=6, column=2)
#
#     scrollbar.grid(row=0, rowspan=7, column=4, sticky=N + S)
#
#     bot_window.mainloop()


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

    subreddit = reddit.subreddit(entry_name.get())
    search_string = reddit.subreddit(entry_search.get())
    comment_string = reddit.subreddit(entry_comment.get())


    for submission in subreddit.hot(limit=10):
        for top_level_comment in submission.comments:
            if hasattr(top_level_comment, "body"):
                comment_search = top_level_comment.body
                if str(search_string) in comment_search:
                    comment_body = top_level_comment.body
                    comment_id = top_level_comment.id
                    comment_url = top_level_comment.permalink
                    full_comment_url = f'https://www.reddit.com/{comment_url}'
                    database_input = Reddid_Class_Comments(comment_body, comment_id, full_comment_url)
                    session0.add(database_input)
                    session0.commit()
                    # comment.reply(comment_string)
                    box.delete(0, 'end')
                    box.insert(END, *pull_bot_comments())
                    label_status["text"] = "Comment posted - timeout 10min"
                    break

''' Graphics '''

bot_window = Tk()

def open_comment_url():
    search_string = str(pull_comment_url_from_database()[box.curselection()[0]])
    search_string_1 = search_string[2:]
    search_string_2 = search_string_1[:-3]
    webbrowser.open(search_string_2)
    label_status["text"] = "Web browser opened"


bot_window.title("Reddit bot")
# bot_window.geometry('1000x450')

scrollbar = Scrollbar(bot_window)
box = Listbox(bot_window, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=box.yview)

box.insert(END, *pull_bot_comments())

label_0 = Label(bot_window, text='Enter subreddit:', width=20)
label_1 = Label(bot_window, text='Search for:', width=20)
label_2 = Label(bot_window, text='The comment:', width=20)
label_status = Label(bot_window, text="Window open")
label_top = Label(bot_window, text = 'Commented comments')

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