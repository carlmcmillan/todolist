from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

while True:
    print("")

    # Menu
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    menu_opt = input()
    print("")

    # Exit
    if menu_opt == '0':
        print("Bye!")
        break

    # Today's tasks
    elif menu_opt == '1':
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline == today.date()).all()
        print("Today {} {}:".format(today.day, today.strftime('%b')))
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(tasks)):
                print("{}. {}".format(i + 1, tasks[i].task))

    # Week's tasks
    elif menu_opt == '2':
        today = datetime.today()
        for i in range(7):
            curr_day = today + timedelta(days=i)
            curr_weekday = weekdays[curr_day.weekday()]
            print("{} {} {}:".format(curr_weekday, curr_day.day, curr_day.strftime('%b')))
            tasks = session.query(Task).filter(Task.deadline == curr_day.date()).all()
            if len(tasks) == 0:
                print("Nothing to do!")
            else:
                for i in range(len(tasks)):
                    print("{}. {}".format(i + 1, tasks[i].task))
            print("")

    # All tasks
    elif menu_opt == '3':
        print("All tasks:")
        tasks = session.query(Task).order_by(Task.deadline).all()
        if len(tasks) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(tasks)):
                print("{}. {}. {} {}".format(i + 1, tasks[i].task, tasks[i].deadline.day, tasks[i].deadline.strftime('%b')))

    # Missed tasks
    elif menu_opt == '4':
        print("Missed tasks:")
        today = datetime.today()
        tasks = session.query(Task).filter(Task.deadline < today.date()).order_by(Task.deadline).all()
        if len(tasks) == 0:
            print("Nothing is missed!")
        else:
            for i in range(len(tasks)):
                print("{}. {}. {} {}".format(i + 1, tasks[i].task, tasks[i].deadline.day, tasks[i].deadline.strftime('%b')))

    # Add task
    elif menu_opt == '5':
        print("Enter task")
        task_name = input()
        print("Enter deadline")
        deadline_str = input()
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
        task = Task(task=task_name, deadline=deadline)
        session.add(task)
        session.commit()
        print("The task has been added!")

    # Delete task
    elif menu_opt == '6':
        tasks = session.query(Task).order_by(Task.deadline).all()
        if len(tasks) == 0:
            print("Nothing to delete")
        else:
            print("Choose the number of the task you want to delete:")
            for i in range(len(tasks)):
                print("{}. {}. {} {}".format(i + 1, tasks[i].task, tasks[i].deadline.day, tasks[i].deadline.strftime('%b')))
            task_num = input()
            task = tasks[int(task_num) - 1]
            session.delete(task)
            session.commit()
            print("The task has been deleted!")
