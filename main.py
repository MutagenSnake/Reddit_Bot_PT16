from tkinter import *
from sqlalchemy.orm import sessionmaker
import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
import praw
import webbrowser
from subprocess import Popen
import subprocess

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

    for submission in subreddit.hot(limit=5):
        title = submission.title
        score = submission.score
        sub_id = submission.id
        print(sub_id)
        url = submission.url
        submission_input = Reddid_Class(title, score, sub_id, url)
        database_sub_ids = pull_from_database_for_id()
        print(database_sub_ids)
        sub_id_converted = reddit_sub_id_convert_to_database_string(sub_id)
        database_sub_ids_normalised = []
        for element in database_sub_ids:
            database_sub_ids_normalised.append(str(element))
        if sub_id_converted not in database_sub_ids_normalised:
            print('Not in database, adding')
            session.add(submission_input)
            session.commit()
            box.delete(0, 'end')
            box.insert(END, *pull_from_database())
        else:
            print('In database, skipping')


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
            # print(top_level_comment.body)
            # print('--------------------')
            comment_list.append(top_level_comment.body)

    root = Tk()
    sizex = 600
    sizey = 400
    posx = 40
    posy = 20
    root.wm_geometry("%dx%d+%d+%d" % (sizex, sizey, posx, posy))
    comments_box = Listbox(root,width=600,height=200)
    comments_box.pack()
    for items in comment_list:
        comments_box.insert(END, items)
    root.mainloop()

# def open_bot_file():
#     Popen("commenter.py")

# import os
#
# def run_program():
#     os.system('commenter.py')

def open_bot_file():
    subprocess.call(["python", "commenter.py"])

''' GUI '''

main_window = Tk()

main_window.title("Reddit register")
# main_window.geometry('1000x450')

scrollbar = Scrollbar(main_window)
box = Listbox(main_window, width=100, yscrollcommand=scrollbar.set)
scrollbar.config(command=box.yview)

# button_frame = Frame(main_window)
# box = Listbox(main_window, selectmode=SINGLE)
box.insert(END, *pull_from_database())


label_top = Label(main_window, text='Submission database')
label = Label(main_window, text='Enter subreddit', width=20)
# label_0 = Label(main_window, text='Commonly used', width=20)

entry_name = Entry(main_window, width=20)

button0 = Button(main_window, text="Enter", command=add_to_database)
button1 = Button(main_window, text="Open", command=open_the_url)
button2 = Button(main_window, text="BOT", command=open_bot_file)
# button3 = Button(main_window, text="URL", command=get_url)
button4 = Button(main_window, text="Comments", command=get_submission_comments)

''' Visual '''
label_top.grid(row=0, column=1, columnspan=3, sticky=W + E)
label.grid(row=1, column=0)
entry_name.grid(row=2, column=0)
button0.grid(row=3, column=0)
button2.grid(row=4, column=0)
button1.grid(row=5, column=0)
# button2.grid(row=6, column=0)
# button3.grid(row=7, column=0)
button4.grid(row=8, column=0)

# box.grid(row=0, rowspan=20, column=1, columnspan=10)
# label.place(x=5, y=5)
#
# entry_name.place(x=5, y=25)
#
# button0.place(x=5, y=45)

# box.place(x=145, y=5, height=400, width=600)

box.grid(row=1, rowspan=8, column=2)

scrollbar.grid(row=1, rowspan=8,column=4, sticky=N+S)

main_window.mainloop()
