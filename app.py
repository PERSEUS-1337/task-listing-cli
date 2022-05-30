import sys
from database import cursor
from database import mariadb


def printTask(categoryName, title, content, deadline, isDone):
    print(f"\t[{categoryName}]") if categoryName else print("\t[UNCATEGORIZED]")

    if isDone:
        print("\t(FINISHED)" + title)
    else:
        print("\t" + title)

    if content:
        print("\t-", content)

    if deadline:
        print("\tDeadline:", deadline)

    print()

# def printCategory(categoryName, title, content, deadline, isDone):
#     print(f"\t[{categoryName}]") if categoryName else print("\t[UNCATEGORIZED]")

#     if isDone:
#         print("\t(FINISHED)" + title)
#     else:
#         print("\t" + title)

#     if content:
#         print("\t-", content)

#     if deadline:
#         print("\tDeadline:", deadline)

#     print()


def createTask():
    pass


def editTask():
    pass


def deleteTask():
    pass


def viewAllTasks():
    print("\t---- All tasks ----\n")

    cursor.execute(
        "SELECT category_id, title, content, deadline, is_done FROM task ORDER BY is_done, title"
    )
    tasks = cursor.fetchall()

    for categoryId, title, content, deadline, isDone in tasks:
        cursor.execute("SELECT name FROM category WHERE category_id = ?", (categoryId,))
        category = cursor.fetchone()

        categoryName = category and category[0]

        printTask(categoryName, title, content, deadline, isDone)


def markTaskAsDone():
    pass


def createCategory():
    pass


def editCategory():
    pass


def deleteCategory():
    pass


def listCategory():
    try:
        cursor.execute(
            "SELECT name, category_id FROM category ORDER BY name"
            # "SELECT name, category_id, description FROM category ORDER BY name"
        )
        categories = cursor.fetchall()
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")

    index = 0
    for name in categories:
        print(f"[{index}] {name[0]}")
        index += 1

    selected = int(input("Enter the index of the chosen category: "))

    return categories[selected]


def viewCategory():
    print("\t---- All categories ----\n")
    categoryChoice = listCategory()
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
