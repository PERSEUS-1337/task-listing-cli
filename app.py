from multiprocessing import connection
import sys
from database import cursor, mConnect, mariadb

def getCatName(catID):
    cursor.execute(
        "SELECT name FROM category where category_id = {}".format(catID)
    )

    return cursor.fetchone()[0]

def list(type):
    if (type == 0) : # type = 0 is for category
        cursor.execute(
            "SELECT name, category_id, description FROM category ORDER BY name"
        )
    elif (type == 1) : # type = 1 is for task
        cursor.execute(
            "SELECT title, task_id, content FROM task ORDER BY title"
        )
    
    query = cursor.fetchall()
    index = 0

    for value in query:
        print(f"[{index}] {value[0]} - {value[2]}")
        index += 1

    if (type == 0): selected = int(input("Enter the index of the chosen category: "))
    elif (type == 1): selected = int(input("Enter the index of the chosen task: "))
    return query[selected]

def printTask(categoryName, title, content, deadline, isDone):
    print(f"\t[{categoryName}]") if categoryName else print("\t[UNCATEGORIZED]")

    if isDone:
        print("\t(FINISHED) " + title)
    else:
        print("\t" + title)

    if content:
        print("\t-", content)

    if deadline:
        print("\tDeadline:", deadline)

    print()

def createTask():
    print("---- Create Task ----\n")
    title_input = (input("Enter the task title: "))
    content_input = input("(Optional) Contents: ")

    flag = True
    while (flag == True):
        deadline_flag = input("Does your task have a deadline? (Y/N)\n")
        if (deadline_flag == "Y"):
            month = int(input("Month (MM): "))
            day = int(input("Day (DD): "))
            year = int(input("Year (YYYY)"))
            deadline = "{}-{}-{}".format(year, month, day)
            flag = False
        elif (deadline_flag == "N"):
            deadline = None
            flag = False
        
    category = list(0)[1] # category_id of selected category

    # To get new task_id: Get the highest task-id in task table then add one.
    cursor.execute(
        "SELECT MAX(task_id)+1 FROM task"
    )
    id =  cursor.fetchone()[0]

    # Values of the new task in tuple
    args = (id, category, title_input, content_input, deadline)

    # Insert the values of the new task to the task table
    cursor.execute(
        "INSERT INTO task(task_id, category_id, title, content, deadline) VALUES(%s, %s, %s, %s, %s)", args
    )

    mConnect.commit()

def editTask():
    print("\t---- Edit Tasks ----\n")
    task = list(1)[1] # task_id of selected task

    cursor.execute(
        "SELECT * FROM task WHERE task_id = {}".format(task)
    )

    taskTuple = cursor.fetchone() # tuple containing current values of the selected task

    printTask(getCatName(taskTuple[1]), taskTuple[2], taskTuple[3], taskTuple[4], taskTuple[5])

def deleteTask():
    pass

def viewAllTasks():
    print("\t---- All tasks ----\n")

    cursor.execute(
        "SELECT category_id, title, content, deadline, is_done FROM task ORDER BY is_done, title"
    )
    tasks = cursor.fetchall()

    for categoryId, title, content, deadline, isDone in tasks:
        printTask(getCatName(categoryId), title, content, deadline, isDone)

def markTaskAsDone():
    pass

def createCategory():
    print("---- Create Category ----\n")
    category_input = input("Enter the category title: ")
    descripton_input = input("(Optional) Description: ")
        
    # To get new task_id: Get the highest task-id in task table then add one.
    cursor.execute(
        "SELECT MAX(category_id)+1 FROM category"
    )
    id = cursor.fetchone()[0]

    # Values of the new task in tuple
    args = (id, category_input, descripton_input)

    # Insert the values of the new task to the task table
    cursor.execute(
        "INSERT INTO category(category_id, name, description) VALUES(%s, %s, %s)", args
    )

    mConnect.commit()

def editCategory():
    pass

def deleteCategory():
    pass

def viewCategory():
    print("\t---- All categories ----\n")
    categoryChoice = list(0)
    print(categoryChoice)

    try: 
        cursor.execute(
            "SELECT name, category_id, description FROM category WHERE name = (%s)", (categoryChoice)
        )
        categories = cursor.fetchall()
        print(categories)
        print(categories[0])
        print(categories[0][0])
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    print("\t---- Selected category ----\n")
    for name, category_id, description in categories:
        print("\t[" + name + "]\n\tDescription: " + description)

        try:
            cursor.execute(
                "SELECT category_id, title FROM task WHERE category_id = (%s)", (categoryChoice)
            )
            tasks = cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        index = 1
        print("\tTasks:")
        for title in tasks:
            print(f"\t\t[{index}]" + title[1])
            index += 1

def addTaskToCategory():
    pass

def viewTaskByCalendar(): 
    pass

def quitApp():
    print("Quitting application\n")
    sys.exit(1)

actions = {
    "ct": {"name": "Create task", "function": createTask},
    "et": {"name": "Edit task", "function": editTask},
    "dt": {"name": "Delete task", "function": deleteTask},
    "vat": {"name": "View all tasks", "function": viewAllTasks},
    "mt": {"name": "Mark task as done", "function": markTaskAsDone},
    "cc": {"name": "Create category", "function": createCategory},
    "ec": {"name": "Edit category", "function": editCategory},
    "dc": {"name": "Delete category", "function": deleteCategory},
    "vc": {"name": "View category", "function": viewCategory},
    "attc": {"name": "Add a task to a category", "function": addTaskToCategory},
    "vtc": {"name": "View task by calendar", "function": viewTaskByCalendar},
    "q": {"name": "Quit application", "function": quitApp},
}


def printActionsList():
    print("Actions: ")
    for actionCode in actions:
        print("•", actions[actionCode]["name"], f"({actionCode})")


def askInput(prompt):
    inputString = input(f"\n{prompt}: ")
    print()

    return inputString


def main():
    while True:
        print("\n==== Task Listing CLI ====\n")

        printActionsList()

        chosenActionCode = askInput("Enter action code")

        if chosenActionCode in actions:
            actions[chosenActionCode]["function"]()
        else:
            print("Action code not recognized\n")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
