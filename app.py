import sys
from database import cursor


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


def viewCategory():
    pass


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
