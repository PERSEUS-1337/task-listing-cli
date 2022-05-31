from multiprocessing import connection
import sys
from database import cursor, mConnect, mariadb

def dateInput():
    print("Deadline: [Write !NULL on Month if no Deadline]")
    dayInMonth = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) 
    while (True):
        month = (input("Month (MM): "))
        if (month == "!NULL"): return None
        if (int(month) in range(1,13)): 
            month = int(month)
            break
    while (True):
        day = int(input("Day (DD): "))
        if (day in range(1,dayInMonth[month]+1)): break
    year = int(input("Year (YYYY): "))
    date = "{}-{}-{}".format(year, month, day)
    return date

def getCatName(catID):
    if (catID == None): return None
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

    while (True):
        if (type == 0): 
            print("Write !NULL for NULL")
            selected = (input("Enter the index of the chosen category: "))
            if (selected == "!NULL"): return None
        elif (type == 1): selected = input("Enter the index of the chosen task: ")

        if int(selected) in range(0, index): return query[int(selected)]
    

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

    deadline = dateInput()
    
    category = list(0) # category_id of selected category
    if (category != None):
        category = category[1]

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

def updateSQL(newValue, task, attrib):
    if ((newValue == "!NULL") or (newValue == None)):
        cursor.execute(
            "UPDATE task SET " + attrib + "=NULL WHERE task_id={}".format(task)
        )
    else:
        cursor.execute(
            "UPDATE task SET " +  attrib + "=%s WHERE task_id=%s", (newValue, task)
        )

def editTask():
    print("\t---- Edit Tasks ----\n")
    task = list(1)[1] # task_id of selected task

    flag = True

    while(flag):
        cursor.execute(
            "SELECT * FROM task WHERE task_id = {}".format(task)
        )
        taskTuple = cursor.fetchone() # tuple containing current values of the selected task

        print("Information of Task to Edit")
        printTask(getCatName(taskTuple[1]), taskTuple[2], taskTuple[3], taskTuple[4], taskTuple[5]) # CatName, title, content, deadline, isDone

        print("What would you like to edit? WARNING: CHANGE IS PERMANENT")
        print("[1] Title | [2] Content | [3] Category of Task | [4] Deadline | [5] Done!")

        choice = int(input("Choice: "))

        if (choice == 1):
            newTitle = input("New Title: ")
            cursor.execute(
                "UPDATE task SET title=%s WHERE task_id=%s", (newTitle, task)
            )
        elif (choice == 2):
            newContent = input("New Content [Write !NULL for NULL]: ")
            updateSQL(newContent, task, 'content')
        elif (choice == 3):
            category = list(0)
            if (category != None): category = category[1]
            updateSQL(category, task, 'category_id')
        elif (choice == 4):
            print("Write !NULL for NULL")
            deadline = dateInput()
            updateSQL(deadline, task, 'deadline')
        elif (choice == 5):
            mConnect.commit()
            flag = False    

def deleteTask():    
    print("\t---- Delete Tasks ----\n")
    task = list(1)[1] # task_id of selected task
    cursor.execute(
        "DELETE FROM task WHERE task_id={}".format(task)
    )
    mConnect.commit()

def viewAllTasks():
    print("\t---- All tasks ----\n")

    cursor.execute(
        "SELECT category_id, title, content, deadline, is_done FROM task ORDER BY is_done, title"
    )
    tasks = cursor.fetchall()

    for categoryId, title, content, deadline, isDone in tasks:
        if (categoryId == None): (printTask(None, title, content, deadline, isDone))
        else: printTask(getCatName(categoryId), title, content, deadline, isDone)

def doneTask(is_done, index):
    cursor.execute( 
        "SELECT title, task_id, content, category_id FROM task WHERE is_done={} ORDER BY category_id DESC, title".format(is_done)
    )
    query = cursor.fetchall()

    for value in query:
        if (value[3] == None): print(f"\t[{index}] {value[0]} - {value[2]}")
        else: print(f"\t[{index}] [{getCatName(value[3])}] {value[0]} - {value[2]}")
        index += 1

    return (query, index)

def markTaskAsDone():
    print("\t---- Change Task Status ----\n")
    print("[UNFINISHED TASKS] (Select task to Mark as DONE)")
    unfinished = doneTask(0, 0) # 0 for False, 0 as index
    print("\n[FINISHED TASKS] (Select task to Mark as NOT DONE)")
    finished = doneTask(1, unfinished[1]) # 1 for False, index returned by first doneTask()

    selected = int(input("\nEnter the index of the chosen task: "))
    if (selected in range(0, unfinished[1])): 
        updateSQL(1, unfinished[0][selected][1], 'is_done')
    elif (selected in range(unfinished[1], finished[1])):
        selected -= unfinished[1]
        updateSQL(0, finished[0][selected][1], 'is_done')
    else: print("Invalid index.")

    mConnect.commit()

def createCategory():
    pass

def editCategory():
    pass

def deleteCategory():
    pass

def viewCategory():
    print("\t---- All categories ----\n")
    categoryChoice = list(0)
    print(categoryChoice[0])

    try: 
        cursor.execute(
            "SELECT name, category_id, description FROM category WHERE name = (?)", (categoryChoice)
        )
        categories = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 

    # print(categories)
    print("\t---- Selected category ----\n")
    for name, category_id, description in categories:
        print("\t[" + name + "]\n\tDescription: " + description)

        cursor.execute(
            "SELECT category_id, title FROM task WHERE category_id = (?)", (categoryChoice)
        )
        tasks = cursor.fetchall()
        index = 1
        print("\tTasks:")
        for title in tasks:
            print(f"\t\t[{index}]" + title[1])
            # ++index
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

        input("Press Enter to continue...")


if __name__ == "__main__":
    main()
