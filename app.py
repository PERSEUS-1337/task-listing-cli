import sys
import mariadb
from database import cursor, connection
from collections import defaultdict

####################### UNIFIED FUNCTIONS SECTION #######################

# ernest
def dateInput():    # asks the user for a Date (Deadline)
    print("Deadline: [Write !NULL on Month if no Deadline]")
    dayInMonth = (0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31) # Days in every month. February set to 29.
    while (True):   # Prevent invalid input for Month
        month = (input("Month (MM): "))
        if (month == "!NULL"): return None  # No Deadline
        if (int(month) in range(1,13)):     # Check if Month is Valid
            month = int(month)
            break
    while (True):   # prevent invalid input for Day
        day = int(input("Day (DD): "))      
        if (day in range(1,dayInMonth[month]+1)): break # Using the dayInMonth tuple, would check if day valid in accordance with selected Month
    year = int(input("Year (YYYY): "))
    date = "{}-{}-{}".format(year, month, day)  # Format accepted by SQL
    return date


# ernest
def getCatName(catID):  # returns the category_name, accepts category_id as parameter
    if (catID == None): return None     # No Category
    try:
        cursor.execute(
            "SELECT name FROM category where category_id = ?", (catID,)
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    return cursor.fetchone()[0]


# ernest
def chooseFromList(type): # lists tasks/categories with index, to make it easier for the user to select.
    try:
        if (type == 0) : # type = 0 is for category
            try:
                cursor.execute(
                    "SELECT name, category_id, description FROM category ORDER BY name"
                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")

        elif (type == 1) : # type = 1 is for task
            try:
                cursor.execute(
                    "SELECT title, task_id, content FROM task ORDER BY title"
                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
        elif (type == 2) : # type = 2 addCategToTask
            try:
                cursor.execute(
                    "SELECT title, task_id, content, category_id FROM task WHERE category_id IS NULL ORDER BY title DESC"
                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    
    query = cursor.fetchall()
    index = 0                   

    # Prints the [index] Title - Description
    for value in query:
        print(f"[{index}] {value[0]} - {value[2]}")
        index += 1

    while (True): # prevents out of bound index inputs
        selected = 0
        if (type == 0): # for category
            selected = (input("Enter the index of the chosen category [Write !NULL for NULL]: "))
            if (selected == "!NULL"): return None # No category
        elif (type == 1 or type == 2): selected = input("Enter the index of the chosen task: ") # for task

        if int(selected) in range(0, index): return query[int(selected)] # checks if input is a proper index


# ernest
def updateSQL(newValue, task, attrib): # update the task table, one attribute at a time | Parameters: new value, task_id, attribute to be changed
    if ((newValue == "!NULL") or (newValue == None)): # dedicated SQL for NULL values since None doesn't work.
        try:
            cursor.execute(
                "UPDATE task SET " + attrib + "=NULL WHERE task_id=?", (task,)
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
    else:
        try:
            cursor.execute(
                "UPDATE task SET " +  attrib + "=%s WHERE task_id=%s", (newValue, task)
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    connection.commit()


# ernest
def doneTask(type, xVal, index): # similar to list but specialized for markTaskAsDone()
    if (type == 0):
        try:
            cursor.execute( 
                "SELECT title, task_id, content, category_id FROM task WHERE is_done=? ORDER BY category_id DESC, title", (xVal,)
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            
    elif (type == 1): # NULL
        try:
            cursor.execute( 
                "SELECT title, task_id, content, category_id FROM task WHERE category=NULL ORDER BY title"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    elif (type == 2): # with Category
        try:
            cursor.execute( 
                "SELECT title, task_id, content, category_id FROM task WHERE category_id IS NOT NULL ORDER BY category_id DESC, title"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

    query = cursor.fetchall()

    # prints:
    #   if no category: [index] Title - Description
    #   if with category: [index] [category_name] Title - Description
    for value in query:
        if (value[3] == None): print(f"\t[{index}] {value[0]} - {value[2]}")
        else: print(f"\t[{index}] [{getCatName(value[3])}] {value[0]} - {value[2]}")
        index += 1

    return (query, index) # returns the 2d tasks tuple, and the index


# garth
def getGroupedTasksBy(chosenTimeFrameType):
    if chosenTimeFrameType not in ["day", "month"]:
        return None

    cursor.execute(
        "SELECT category_id, title, content, deadline, is_done, MONTHNAME(deadline), DAY(deadline), DAYNAME(deadline), YEAR(deadline) FROM task ORDER BY deadline, is_done, title"
    )
    allTasks = cursor.fetchall()

    groupedTasks = defaultdict(list)
    for (
        categoryId,
        title,
        content,
        deadline,
        isDone,
        deadlineMonthName,
        deadlineDay,
        deadlineDayName,
        deadlineYear,
    ) in allTasks:
        categoryName = getCatName(categoryId)

        if deadline and chosenTimeFrameType == "day":
            timeFrame = (
                f"{deadlineMonthName} {deadlineDay}, {deadlineYear} ({deadlineDayName})"
            )

        elif deadline and chosenTimeFrameType == "month":
            timeFrame = f"{deadlineMonthName} {deadlineYear}"

        else:
            timeFrame = None

        groupedTasks[timeFrame].append(
            {
                "categoryName": categoryName,
                "title": title,
                "content": content,
                "deadline": deadline,
                "isDone": isDone,
            }
        )

    return groupedTasks


# ernest
def printTask(categoryName, title, content, deadline, isDone, tabCount=0):
    indent = "\t" * tabCount

    print(f"{indent}[{categoryName or 'UNCATEGORIZED'}]")

    if isDone:
        print(f"{indent}(FINISHED) " + title)
    else:
        print(f"{indent}" + title)

    if content:
        print(f"{indent}-", content)

    if deadline:
        print(f"{indent}Deadline:", deadline)

    print()


# ernest
def createTask(): # create/add new task
    print("---- Create Task ----\n")

    # To get new task_id: Get the highest task-id in task table then add one.
    try:
        cursor.execute(
            "SELECT MAX(task_id)+1 FROM task"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
    id =  cursor.fetchone()[0]

    title_input = (input("Enter the task title: "))
    if (title_input == ""): title_input = "Task {}".format(id)
    content_input = input("Contents: ")

    print("\nEnter Deadline of Task: ")
    deadline = dateInput()
    
    print("\nCategory of Task:")
    category = chooseFromList(0) # category tuple if a category is selected, None if no category is selected
    if (category != None): # checks if category is a category tuple
        category = category[1] # category_id

    # Values of the new task in tuple
    args = (id, category, title_input, content_input, deadline)

    # Insert the values of the new task to the task table
    try:
        cursor.execute(
            "INSERT INTO task(task_id, category_id, title, content, deadline) VALUES(%s, %s, %s, %s, %s)", args
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    connection.commit()


# ernest
def editTask():
    print("\t---- Edit Tasks ----\n")
    task = chooseFromList(1)[1]  # task_id of selected task

    flag = True
    while(flag):
        try:
            cursor.execute(
                "SELECT * FROM task WHERE task_id = ?", (task,) 
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        taskTuple = cursor.fetchone() # tuple containing current values of the selected task

        print("\nInformation of Task to Edit")
        printTask(getCatName(taskTuple[1]), taskTuple[2], taskTuple[3], taskTuple[4], taskTuple[5]) # category_name, title, content, deadline, is_done

        print("What would you like to edit? WARNING: CHANGE IS PERMANENT")
        print("[1] Title | [2] Content | [3] Category of Task | [4] Deadline | [5] Done!")

        choice = (input("Choice: "))
        print()

        if ((choice) == "1"): # Title
            # title doesn't use updateSQL since it can't be NULL.
            newTitle = input("New Title: ")
            if (newTitle == ""): print("Title can't be blank.")
            else:
                try:
                    cursor.execute(
                        "UPDATE task SET title=%s WHERE task_id=%s", (newTitle, task)
                    )
                except mariadb.Error as e:
                    print(f"Error connecting to MariaDB Platform: {e}")

        elif (choice == "2"): # Content
            newContent = input("New Content [Write !NULL for NULL]: ")
            updateSQL(newContent, task, 'content')
        elif (choice == "3"): # Category
            category = chooseFromList(0)
            if (category != None): category = category[1]
            updateSQL(category, task, 'category_id')
        elif (choice == "4"): # Deadline
            print("Write !NULL for NULL")
            deadline = dateInput()
            updateSQL(deadline, task, 'deadline')
        elif (choice == "5"): # Exit
            flag = False    
        else: print("Invalid Choice.")


# ernest
def deleteTask():    
    print("\t---- Delete Tasks ----\n")
    task = chooseFromList(1)[1]  # task_id of selected task
    try:
        cursor.execute(
            "DELETE FROM task WHERE task_id=?", (task,)
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    connection.commit()


# garth
def viewAllTasks():
    print("\t---- All tasks ----\n")
    try:
        cursor.execute(
            "SELECT category_id, title, content, deadline, is_done FROM task ORDER BY is_done, title"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    tasks = cursor.fetchall()

    for categoryId, title, content, deadline, isDone in tasks:
        printTask(getCatName(categoryId), title, content, deadline, isDone, tabCount=1)


# ernset
def markTaskAsDone():
    print("\t---- Change Task Status ----\n")
    print("[UNFINISHED TASKS] (Select task to Mark as DONE)")
    unfinished = doneTask(0, 0, 0) # 0 for False, 0 as index |
    print("\n[FINISHED TASKS] (Select task to Mark as NOT DONE)")
    finished = doneTask(0, 1, unfinished[1]) # 1 for True, index returned by first doneTask()

    selected = int(input("\nEnter the index of the chosen task: "))
    if (selected in range(0, unfinished[1])): # checks if selected is in unfinished
        updateSQL(1, unfinished[0][selected][1], 'is_done') # Parameters: True, category_id of selected task, attribute to be changed
    elif (selected in range(unfinished[1], finished[1])): # checks if selected is in finished
        selected -= unfinished[1] # change the value of selected to be accurate with index of finished[0] (2d finished tuple)
        updateSQL(0, finished[0][selected][1], 'is_done') # Parameters: False, category_id of selected task, attribute to be changed
    else: print("Invalid index.")

    connection.commit()


# resty
def viewCategory():
    print("\t---- All categories ----\n")
    categoryChoice = chooseFromList(0)      # Gets category details (name, id, desc) and stores it in an array

    if (categoryChoice == None):
        return
    else:
        print("\t[" + categoryChoice[0] + "]\n\tDescription: " + categoryChoice[2])     # 0 for name, 2 for description

        try:
            cursor.execute("SELECT category_id, title FROM task WHERE category_id = (%s)", (categoryChoice[1],))        # get id using 1, added a comma to the end for python to treat it as a tuple
            tasks = cursor.fetchall()
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
        
        if not tasks: print("\t\tThere are no tasks as of the moment")
        else:
            print("\tTasks:")
            index = 1
            for category_id, title in tasks:
                print(f"\t\t[{index}]" + title)
                index += 1


# resty
def createCategory():
    print("---- Create Category ----\n")
    category_input = input("Enter the category title: ")
    descripton_input = input("(Optional) Description: ")
    
    try:
        cursor.execute("SELECT MAX(category_id)+1 FROM category")       # To get new category_id: Get the highest category_id in category table then add one.
        id = cursor.fetchone()[0]       # Get the first value (which is the max value returned) using 0

        args = (id, category_input, descripton_input)       # Values of the new category in tuple
        cursor.execute("INSERT INTO category(category_id, name, description) VALUES(%s, %s, %s)", args)     # Insert the values of the new category to the category table
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 
    
    connection.commit()


# resty
def editCategory():
    print("\t---- Edit category ----\n")
    args = ()
    attrib = ''

    categoryChoice = chooseFromList(0)
    choiceInput = int(input("\n\t[1] Category name\n\t[2] Category description\n\nWhat do you want to edit? [Write 0 to EXIT): "))

    if (choiceInput == 1): 
        changeNameInput = input(">> Enter new category name: ")
        attrib = 'name'
        args = (changeNameInput, categoryChoice[1])         # select 1 for id

    elif (choiceInput == 2):
        changeDescInput = input(">> Enter new category description: ")
        attrib = 'category'
        args = (changeDescInput, categoryChoice[1])         # select 1 for id
    
    elif (choiceInput == 0):
        return

    try:
        cursor.execute("UPDATE category SET " + attrib + " = (%s) WHERE category_id = (%s)", args)
        connection.commit()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}") 


# resty
def deleteCategory():
    print("\t---- Delete category ----\n")
    categoryChoice = chooseFromList(0)        # Gets category details (name, id, desc) and stores it in an array

    if categoryChoice == None:
        return
    else:
        try:
            cursor.execute("UPDATE task SET category_id = NULL WHERE category_id = (%s)", (categoryChoice[1],))
            cursor.execute("DELETE FROM category WHERE category_id = (%s)", (categoryChoice[1],))
            
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        connection.commit()


# resty
def addTaskToCategory():
    print("\t---- Add Task to Category ----\n")
    print("(Select task to Categorize)")
    taskChoice = chooseFromList(2)
    
    print("\n(Select task to Categorize)")
    categoryChoice = chooseFromList(0)
    if(categoryChoice == None):
        return
    else:
        print(taskChoice[0])
        print(categoryChoice[0])

        args = (categoryChoice[1], taskChoice[1])
        try:
            cursor.execute("UPDATE task SET category_id = (%s) WHERE task_id = (%s)", args)
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")

        print("\t\nSuccessfully added Task: '" + taskChoice[0] + "' to Category: [" + categoryChoice[0] + "]")

        connection.commit()


# garth
def viewTaskCalendar():
    print("\tView task per:")
    print("\t• Day (d)")
    print("\t• Month (m)")

    timeFrameCode = askInput("Enter time frame code", tabCount=1)

    if timeFrameCode == "d":
        groupedTasks = getGroupedTasksBy("day")
    elif timeFrameCode == "m":
        groupedTasks = getGroupedTasksBy("month")
    else:
        print("\tInput not recognized\n")
        return

    print("\t---- All tasks ----\n")

    for timeFrame, tasks in groupedTasks.items():
        print(f"\t{timeFrame or '*NO DEADLINE*'}\n")

        for taskInfo in tasks:
            printTask(
                taskInfo["categoryName"],
                taskInfo["title"],
                taskInfo["content"],
                taskInfo["deadline"],
                taskInfo["isDone"],
                tabCount=2,
            )


# garth
def quitApp():
    print("Quitting application\n")
    sys.exit(1)


# garth
actions = {
    "vat": {"name": "View all tasks", "function": viewAllTasks},
    "vtc": {"name": "View task calendar", "function": viewTaskCalendar},
    "ct": {"name": "Create task", "function": createTask},
    "et": {"name": "Edit task", "function": editTask},
    "dt": {"name": "Delete task", "function": deleteTask},
    "mt": {"name": "Mark task as done", "function": markTaskAsDone},
    "cc": {"name": "Create category", "function": createCategory},
    "ec": {"name": "Edit category", "function": editCategory},
    "dc": {"name": "Delete category", "function": deleteCategory},
    "vc": {"name": "View category", "function": viewCategory},
    "attc": {"name": "Add a task to a category", "function": addTaskToCategory},
    "q": {"name": "Quit application", "function": quitApp},
}


# garth
def printActionsList():
    print("Actions: ")
    for actionCode in actions:
        print("•", actions[actionCode]["name"], f"({actionCode})")


# garth
def askInput(prompt, tabCount=0):
    indent = "\t" * tabCount

    inputString = input(f"\n{indent}{prompt}: ")
    print()

    return inputString


# garth
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


# garth
if __name__ == "__main__":
    main()