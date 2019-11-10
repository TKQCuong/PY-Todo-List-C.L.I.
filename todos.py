import os
import sqlite3
import sys
from termcolor import colored
from colored import fg, bg, attr
from datetime import datetime
from tabulate import tabulate
from colour import Color

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)
cur = conn.cursor()

sql = """
  CREATE TABLE IF NOT EXISTS todos(f
    Id INTEGER PRIMARY KEY,
    Name TEXT NOT NULL,
    due_date TEXT NOT NULL,
    ProjectID INTERGER,
    UserID INTERGER,
    Status TEXT DEFAULT "incomplete"
  )
"""
cur.execute(sql)
conn.commit()

def list():
    sql = """
      SELECT * FROM todos
    """
    cur.execute(sql)
    results = cur.fetchall()
    print(colored('*' * 89, 'yellow'))
    print(tabulate(results, 
      headers=[
        ('Id'),
        ('Name'),
        ('Due_date'),
        ('Project ID'),
        ('User ID'),
        ('Status')
      ],
      tablefmt="grid"))
    print(colored('*' * 89, 'yellow'))

# def show_help_menu():
#     print(tabulate(results, 
#       headers=[
#         ('Id'),


def show_help_menu():
  os.system('cls' if os.name == 'nt' else 'clear')
  print(colored('Todo List Options:', 'yellow'))
  print(colored('*' * 50, 'green'))
  print(colored('1. List all todos:', 'blue'))
  print(colored('\t enter - "list" or "l"', 'white'))
  print(colored('2. Add a new todo:', 'blue'))
  print(colored('\t enter - "add" or "a"', 'white'))
  print(colored('3. Delete a todo:', 'blue'))
  print(colored('\t enter - "remove" or "r"', 'white'))
  print(colored('4. Mark a todo complete:', 'blue'))
  print(colored('\t enter - "done" or "d"', 'white'))
  print(colored('5. Mark a todo uncomplete:', 'blue'))
  print(colored('\t enter - "undone" or "u"', 'white'))
  print(colored('6. Show completed todos only:', 'blue'))
  print(colored('\t enter - "complete" or "c"', 'white'))
  print(colored('6. Update the title of a todo:', 'blue'))
  print(colored('\t enter - "update" or "up"', 'white'))
  print(colored('6. Deleted all todos:', 'blue'))
  print(colored('\t enter - "reset"', 'white'))
  print(colored('-' * 100, 'green'))

def selectComplete():
    sql = """
      SELECT * FROM todos
      WHERE Status = 'completed'
    """
    cur.execute(sql)
    results = cur.fetchall()
    print(colored('*' * 89, 'yellow'))
    print(tabulate(results, 
      headers=[
        ('Id'),
        ('Name'),
        ('Due_date'),
        ('Project ID'),
        ('User ID'),
        ('Status')
      ],
      tablefmt="grid"))
    print(colored('*' * 89, 'yellow'))

def add():
    sql = """
      INSERT INTO todos
        (Name, due_date, ProjectID, UserID)
      VALUES (?,?,?,?)
    """
    Name = input()
    print(colored("Successfully added!!", 'yellow'))
    cur.execute(sql, (Name,datetime.now(),1,1))
    conn.commit()

def remove():
    sql = """
      DELETE FROM todos 
        WHERE Id = ?
    """
    remove = input()
    print(colored("Deleted !", 'red'))
    cur.execute(sql, (remove,))
    conn.commit()

def decideDelete():
      print("-->Type any key to Reset all or Ctrl+C to Exit")
      reset = input()
      if reset == 'yes' or 'y':
          sql = """
              DELETE FROM todos 
          """
          print(colored("Deleted all !", 'red'))
          cur.execute(sql)
          conn.commit()

def complete():
    sql = """
      UPDATE todos
        SET Status = ? WHERE Id = ?
    """
    complete = input()
    print(colored("Updated !", 'yellow'))
    cur.execute(sql, ('completed',complete))
    conn.commit()

def uncomplete():
    sql = """
      UPDATE todos
        SET Status = ? WHERE Id = ?
    """
    uncomplete = input()
    print(colored("Updated !", 'yellow'))
    cur.execute(sql, ('incomplete',uncomplete))
    conn.commit()

def update():
  sql = """
    UPDATE todos
      SET Name = ? WHERE Id = ?
  """
  print("-- Enter an ID")
  Id = input()
  print("-- Enter new title")
  title = input()
  print(colored("Updated !",'green'))
  cur.execute(sql, (title, Id))
  conn.commit()



if __name__ == '__main__':
    # try:
        while True:
            print(colored('Please select an action', 'green'),'OR',colored('Press "Help" to find approriate keys', 'green'))
            choice = input()
            if choice == 'help' or choice == 'h' or choice == 'menu' or choice == 'Help':
                show_help_menu()
            elif choice == 'add' or choice == 'a':
                print(colored("What do you want to ADD?", 'green'))
                add()
            elif choice == 'list' or choice == 'l':
                list()
            elif choice == 'remove' or choice == 'r':
                print(colored("What task do you want to remove? (Enter an ID number)", 'green'))
                remove()
            elif choice == 'done' or choice == 'd':
                print(colored("What task have you completed? (Enter an ID number)", 'green'))
                complete()
            elif choice == 'undone' or choice == 'u':
                print(colored("What task have you NOT completed? (Enter an ID number)", 'green'))
                uncomplete()
            elif choice == 'reset':
                print(colored("Reset all?",'red'))
                decideDelete()
            elif choice == 'complete' or choice == 'c':
                selectComplete()
            elif choice == 'update' or choice == 'up':
                update()
            else:
                show_help_menu()
                print(colored("Wrong keyword! Please check menu above", 'red'))

    # except IndexError:
    # #     print(colored('Error', 'red'))
    #   show_help_menu()
    

