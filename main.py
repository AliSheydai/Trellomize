from rich import console
from rich.table import Table
import os
import json
import re
import uuid
import datetime
from enum import Enum
import bcrypt
from loguru import logger

console = console.Console()
logger.add("app.log", rotation="1 week", level="INFO", format="{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}")


class Model:
    def __init__(self):
        self.id = uuid.uuid4()
        self.users = []


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password


def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)


def passing():
    console.print("Enter any key to continue..", style="black")
    passing = input()


class Account(Model):
    def __init__(self):
        self.id = Model()
        self.user_name = ""
        self.user_data = []
        self.user_info = dict()
        self.user_detail_list = []
        self.logged_in = False
        self.active_user_account = True
        self.user_info["ID"] = str(self.id)
        self.regular_member_projects = []
        self.leader_member_projects = []
        self.projects = []

    def register(self, user_name, password, email):
        self.user_info["gmail"] = email
        self.user_info["Username"] = user_name
        self.user_info["Hash_password_str"] = hash_password(password=password).decode('utf8')
        self.user_info["Is_active"] = False if not self.active_user_account else True
        self.user_info["Regular_member"] = self.regular_member_projects
        self.user_info["Leader_member"] = self.leader_member_projects
        self.user_data = json.load(open("users.json", "r"))

        def is_valid_gmail():
            pattern = r"^[A-Z|a-z][A-Z|a-z|0-9|\.|_|-]*@[\w|\d|_|-]+\.[\w]+$"
            if not re.fullmatch(pattern, email):
                console.print("Invalid gmail ! please enter valid gmail\n", style="bold red")
                return False
            return True

        def is_valid_username():
            if len(str(user_name)) < 3 or len(str(user_name)) > 14:
                console.print("Invalid userName ! please enter userName greater than 5 and less than 14 character\n",
                              style="bold red")
                return False
            elif any(user_name in item.get("Username") for item in self.user_data):
                console.print("Username is already used", style="bold red")
                return False
            return True

        def is_valid_password():
            if len(str(password)) < 5 or len(str(password)) > 18:
                console.print("Enter password greater than 5 and less than 18 character", style="bold red")
                return False
            return True

        if is_valid_username() and is_valid_gmail() and is_valid_password():
            self.user_data.append(self.user_info)
            with open("users.json", "w") as f:
                json.dump(self.user_data, f, indent=4)
            console.print("\nAccount created successfully", style="bold green")
            self.active_user_account = True
            logger.info(f"Account {user_name} was successfully built.")
            return True
        else:
            logger.warning(f"{user_name} account creation failed")
            return False

    def login(self, user_name, password):
        self.user_data = json.load(open("users.json", "r"))
        for item in self.user_data:
            if user_name == item.get("Username"):
                if not item.get("Is_active"):
                    console.print("The user account has been closed by the system administrator."
                                  " You are not allowed to access the account!\n", style="bold red")
                    logger.warning(f"Login failed for user {user_name}")
                    passing()
                    return False

                if verify_password(password=password, hashed_password=item.get("Hash_password_str").encode('utf8')):
                    console.print(f"\nWelcome {user_name}", style="bold green")
                    logger.info(f"User {user_name} logged in")
                    self.logged_in = True
                    return True
                else:
                    console.print("You have entered the wrong password!\n", style="bold red")
                    logger.warning(f"Login failed for user {user_name}")
                    passing()
                    return False

        if not self.logged_in:
            console.print("The username entered is not valid!\n", style="bold red")
            logger.warning(f"Login failed for user {user_name}")
            passing()


class CreateProject(Model):
    def __init__(self, title):
        self.id = str(Model())
        self.project_data = []
        self.project_details = dict()
        self.title = title
        self.members = []
        self.project_details["Project_ID"] = str(self.id)
        self.tasks = []
        self.tasks_data = [
            {"Task ID": task.task_unique_identifier,
             "Title": task.title,
             "Description": task.description,
             "Start Time": str(task.start_time),
             "Start Date": str(task.start_date),
             "End Time": str(task.end_time),
             "End Date": str(task.end_date),
             "Assignees": task.assignees,
             "Priority": str(task.priority)[9:],
             "Status": str(task.status)[7:],
             "Comments": task.comments,
             "History": task.history} for task in self.tasks
        ]

    def save_information(self, leader_id):
        self.project_details["Leader_ID"] = leader_id
        self.project_details["Title"] = self.title
        self.project_details["Members"] = self.members
        self.project_details["Tasks"] = [task.title for task in self.tasks]
        self.project_details["Tasks Data"] = [
            {"Task ID": task.task_unique_identifier,
             "Title": task.title,
             "Description": task.description,
             "Start Time": str(task.start_time),
             "Start Date": str(task.start_date),
             "End Time": str(task.end_time),
             "End Date": str(task.end_date),
             "Assignees": task.assignees,
             "Priority": str(task.priority)[9:],
             "Status": str(task.status)[7:],
             "Comments": task.comments,
             "History": task.history} for task in self.tasks
        ]
        self.project_data = json.load(open("projects.json", "r"))
        for i in range(len(self.project_data)):
            if self.project_data[i]["Title"] == self.title:
                del self.project_data[i]

        self.project_data.append(self.project_details)
        with open("projects.json", "w") as f:
            json.dump(self.project_data, f, indent=4)

    def add_member(self, username):
        self.members.append(username)

    def delete_member(self, username):
        self.members.remove(username)

    def add_task(self, task):
        self.tasks.append(task)


class CreateTask(Model):
    class Priority(Enum):
        LOW = 1
        MEDIUM = 2
        HIGH = 3
        CRITICAL = 4

    class Status(Enum):
        BACKLOG = 1
        TODO = 2
        DOING = 3
        DONE = 4
        ARCHIVED = 5

    def __init__(self, title, description):
        self.task_unique_identifier = str(Model())
        self.task_data = []
        self.task_properties = dict()
        self.title = title
        self.description = description
        start_time = datetime.datetime.now()
        self.start_time = start_time.time()
        self.start_date = start_time.date()
        end_datetime = start_time + datetime.timedelta(hours=24)
        self.end_time = end_datetime.time()
        self.end_date = end_datetime.date()
        self.assignees = []
        self.priority = CreateTask.Priority.LOW
        self.status = CreateTask.Status.BACKLOG
        self.comments = []
        self.history = []
        self.comment = dict()
        self.comment_text = ""
        self.comment_writer = ""

    def save_info(self, title_project):
        self.task_properties["Task ID"] = self.task_unique_identifier
        self.task_properties["Title"] = self.title
        self.task_properties["Description"] = self.description
        self.task_properties["Start Time"] = str(self.start_time)
        self.task_properties["Start Date"] = str(self.start_date)
        self.task_properties["End Time"] = str(self.end_time)
        self.task_properties["End Date"] = str(self.end_date)
        self.task_properties["Assignees"] = self.assignees
        self.task_properties["Priority"] = str(self.priority)
        self.task_properties["Status"] = str(self.status)
        self.task_properties["Comments"] = self.comments
        self.task_properties["History"] = self.history
        self.task_data = json.load(open(f"{title_project}_tasks.json", "r"))
        self.task_data.append(self.task_properties)
        with open(f"{title_project}_tasks.json", "w") as f:
            json.dump(self.task_data, f, indent=4)

    def write_comment(self, text, username):
        self.comment_text = text
        self.comment_writer = username
        self.comment_date = datetime.datetime.now()
        self.comment["Text"] = self.comment_text
        self.comment["Writer"] = self.comment_writer
        self.comment["Record Date"] = self.comment_date
        self.comments.append(self.comment)

    # def set_status(self, new_status):
    #     if new_status in CreateTask.Status:
    #         self.status = new_status
    #     else:
    #         print(f"Invalid status: {new_status}")

    # def set_priority(self, new_priority):
    #     if new_priority in CreateTask.Priority:
    #         self.status = new_priority
    #     else:
    #         print(f"Invalid priority: {new_priority}")

    def next_status(self):
        current_value = self.status.value
        next_value = (current_value % len(CreateTask.Status)) + 1
        if self.status != self.Status.ARCHIVED:
            self.status = CreateTask.Status(next_value)
            return True
        return False

    def next_priority(self):
        current_value = self.priority.value
        next_value = (current_value % len(CreateTask.Priority)) + 1
        if self.priority != self.Priority.CRITICAL:
            self.priority = CreateTask.Priority(next_value)
            return True
        return False

    def previous_status(self):
        current_value = self.status.value
        previous_value = (current_value - 2) % len(CreateTask.Status) + 1
        if self.status != self.Status.BACKLOG:
            self.status = CreateTask.Status(previous_value)
            return True
        return False

    def previous_priority(self):
        current_value = self.priority.value
        previous_value = (current_value - 2) % len(CreateTask.Priority) + 1
        if self.priority != self.Priority.LOW:
            self.priority = CreateTask.Priority(previous_value)
        return False


def is_your_project(username):
    global info_projects
    info_projects = json.load(open("projects.json", "r"))
    global info_users
    info_users = json.load(open("users.json", "r"))
    global projects
    projects = []
    global users
    users = []

    for user in info_users:
        if user["Username"] == username:
            projects = user["Leader_member"]
        if user["Username"] != username:
            users.append(user["Username"])
    console.print(projects, style="green")
    console.print("Enter title of your project", style="yellow")
    global title
    title = input()

    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next(
                    (item.get("ID") for item in info_users if username == item.get("Username")), None):
                return True
    return False


def delete_project(username):
    # info_users = json.load(open ("users.json", "r"))
    # projects = []
    # for user in info_users:
    #     if user["Username"] == username:
    #         projects = user["Leader_member"]
    # console.print(projects)
    if is_your_project(username=username):
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                console.print(f"Are you sure to delete the {title} project?", style="yellow")
                console.print("1- Yes", style="yellow")
                console.print("2- No", style="yellow")
                choice = str(input())
                if choice == '1':
                    del info_projects[i]
                    with open("projects.json", "w") as f:
                        json.dump(info_projects, f, indent=4)

                    console.print("The project was deleted successfully.", style="green")
                    logger.info(f"{title} project was deleted")
                    for i in range(len(info_users)):
                        if info_users[i].get("Username") == username:
                            info_users[i].get("Leader_member").remove(title)
                            with open("users.json", "w") as f:
                                json.dump(info_users, f, indent=4)
                elif choice == '2':
                    continue
                else:
                    console.print("Invalid key!Please try again.", style="black")
                    passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project.", style="bold red")


def add_user_project(username):
    # info_users = json.load(open ("users.json", "r"))
    # info_projects = json.load(open ("projects.json", "r"))
    # projects = []
    # users = []

    # for user in info_users:
    #     if user["Username"] == username:
    #         projects = user["Leader_member"]
    #     if user["Username"] != username:
    #         users.append(user["Username"])
    # console.print(projects, style="green")
    if is_your_project(username=username):
        console.print(users, style="green")
        console.print("Please enter the username you want to add to the project", style="yellow")
        add_user_name = str(input())
        is_user_appened = True

        for i in range(len(info_projects)):
            if info_projects[i]["Title"] == title:
                if add_user_name not in info_projects[i]["Members"]:
                    is_user_appened = False
        if any(add_user_name in item.get("Username") for item in info_users) and add_user_name != username:
            if not is_user_appened:
                for i in range(len(info_projects)):
                    if info_projects[i].get("Title") == title:
                        info_projects[i].get("Members").append(add_user_name)
                        with open("projects.json", "w") as f:
                            json.dump(info_projects, f, indent=4)

                        for i in range(len(info_users)):
                            if info_users[i].get("Username") == add_user_name:
                                info_users[i].get("Regular_member").append(title)
                                with open("users.json", "w") as f:
                                    json.dump(info_users, f, indent=4)
                        console.print(f"{add_user_name} added to {title} project", style="green")
                        logger.info(f"{add_user_name} added to {title} project")
            else:
                console.print(f"{username} is already append to {title} ptoject!", style="blue")
                passing()
        else:
            console.print("Invalid username!", style="bold red")
            passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project", style="bold red")
        passing()


def delete_user_project(username):
    members = []
    if is_your_project(username=username):
        for user in info_users:
            if user["Username"] != username and title in user["Regular_member"]:
                members.append(user["Username"])
        console.print(members, style="green")
        console.print("Please enter the username you want to delete from the project", style="yellow")
        delete_user_name = str(input())
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                if delete_user_name in info_projects[i].get("Members"):
                    info_projects[i].get("Members").remove(delete_user_name)
                    for task in info_projects[i]["Tasks Data"]:
                        try:
                            task["Assignees"].remove(delete_user_name)
                        except ValueError:
                            pass
                    with open("projects.json", "w") as f:
                        json.dump(info_projects, f, indent=4)

                    for i in range(len(info_users)):
                        if info_users[i].get("Username") == delete_user_name:
                            info_users[i].get("Regular_member").remove(title)
                            with open("users.json", "w") as f:
                                json.dump(info_users, f, indent=4)
                    console.print(f"{delete_user_name} deleted from {title} project", style="green")
                    logger.info(f"{delete_user_name} deleted from {title} project by {username}")
                else:
                    console.print("Entered username is not valid!", style="bold red")
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project", style="bold red")


def task_definition(username):
    if is_your_project(username=username):
        project = CreateProject(title)
        info_projects = json.load(open("projects.json", "r"))
        console.print("Please enter the title of the task you want to define", style="yellow")
        add_task_title = str(input())
        console.print("Please enter the description of the task", style="yellow")
        add_task_description = str(input())

        task = CreateTask(add_task_title, add_task_description)
        project.add_task(task)
        project.tasks_data = [
            {"Task ID": task.task_unique_identifier,
             "Title": task.title,
             "Description": task.description,
             "Start Time": str(task.start_time),
             "Start Date": str(task.start_date),
             "End Time": str(task.end_time),
             "End Date": str(task.end_date),
             "Assignees": task.assignees,
             "Priority": str(task.priority)[9:],
             "Status": str(task.status)[7:],
             "Comments": task.comments,
             "History": task.history} for task in project.tasks
        ]
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                info_projects[i]["Tasks"].append(project.tasks[0].title)
                info_projects[i].get("Tasks Data").append(project.tasks_data[0])
                break

        with open("projects.json", "w") as f:
            json.dump(info_projects, f, indent=4)

        console.print(f"{add_task_title} task defined in {title} project", style="green")
        logger.info(f"{add_task_title} task defined in {title} project")
        passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()


def task_delete(username):
    valid_task = False
    if is_your_project(username=username):
        tasks = []
        for project in info_projects:
            if project["Title"] == title:
                tasks = project["Tasks"]
        console.print(tasks)
        console.print("Please enter the name of the task you want to delete", style="yellow")
        delete_task = str(input())
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                if delete_task in info_projects[i].get("Tasks"):
                    valid_task = True
                    info_projects[i].get("Tasks").remove(delete_task)
                    console.print(f"{delete_task} task delete from {title} project", style="green")
                    logger.info(f"{delete_task} task delete from {title} project")
                for j in range(len(info_projects[i].get("Tasks Data"))):
                    if info_projects[i].get("Tasks Data")[j]["Title"] == delete_task:
                        del info_projects[i].get("Tasks Data")[j]
                    with open("projects.json", "w") as f:
                        json.dump(info_projects, f, indent=4)
                    break
        if not valid_task:
            console.print("Enterd task is not valid!", style="bold red")
            passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()


def task_allocation(username):
    info_projects = json.load(open("projects.json", "r"))
    info_users = json.load(open("users.json", "r"))
    is_exist_project = False
    tasks = []
    members = []
    projects_title = []
    for user in info_users:
        if user["Username"] == username:
            projects_title = user["Leader_member"]
    console.print(projects_title)
    console.print("Enter title of your project", style="yellow")
    title = str(input())

    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next(
                    (item.get("ID") for item in info_users if username == item.get("Username")), None):
                tasks = item.get("Tasks")
                members = item.get("Members")
                if username not in members:
                    members.append(username)

                is_exist_project = True
                break

    if is_exist_project:
        console.print(f"Tasks: {tasks}")
        console.print("Please enter the name of the task to allocate for you", style="yellow")
        allocation_task = str(input())
        if allocation_task in tasks:
            console.print(f"Members: {members}")
            console.print("Enter the name of the person you want to assign the task", style="yellow")
            user_allocation = str(input())

            allocation_task_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_history = dict()
            task_history["Changing User"] = f"{username};({title} project leader)"
            task_history["Changing Date"] = allocation_task_date
            task_history["Action"] = f"{user_allocation} took {allocation_task} task"

            if user_allocation in members:

                for i in range(len(info_projects)):
                    if info_projects[i].get("Title") == title:
                        for j in range(len(info_projects[i].get("Tasks Data"))):
                            if info_projects[i].get("Tasks Data")[j]["Title"] == allocation_task:
                                if user_allocation not in info_projects[i].get("Tasks Data")[j]["Assignees"]:
                                    info_projects[i].get("Tasks Data")[j]["Assignees"].append(user_allocation)
                                    console.print(
                                        f"{user_allocation} assign the {allocation_task} task in {title} project",
                                        style="green")
                                    logger.info(
                                        f"{user_allocation} assign the {allocation_task} task in {title} project")
                                    info_projects[i].get("Tasks Data")[j]["History"].append(task_history)

                                    with open("projects.json", "w") as f:
                                        json.dump(info_projects, f, indent=4)
                                else:
                                    console.print(f"{user_allocation} has already undertaken this task!", style="blue")
                                passing()
                                break
            else:
                console.print(f"{user_allocation} is not a member of {title} project", style="bold red")
                passing()
        else:
            console.print(f"{allocation_task} task is not valid!", style="bold red")
            passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()


def delete_task_allocation(username):
    info_projects = json.load(open("projects.json", "r"))
    info_users = json.load(open("users.json", "r"))
    is_exist_project = False
    tasks = []
    members = []
    projects_title = []
    for user in info_users:
        if user["Username"] == username:
            projects_title = user["Leader_member"]
    console.print(projects_title)
    console.print("Enter title of your project", style="yellow")
    title = input()

    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next(
                    (item.get("ID") for item in info_users if username == item.get("Username")), None):
                tasks = item.get("Tasks")
                members = item.get("Members")
                if username not in members:
                    members.append(username)

                is_exist_project = True
                break

    if is_exist_project:
        console.print(f"Tasks: {tasks}")
        console.print("Please enter the name of the task you want to delete allocation", style="yellow")
        delete_allocation_task = str(input())
        if delete_allocation_task in tasks:
            console.print(f"Members: {members}")
            console.print("Enter the name of the person you want to picking up the task", style="yellow")
            user_delete = str(input())

            allocation_task_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            task_history = dict()
            task_history["Changing User"] = f"{username};({title} project leader)"
            task_history["Changing Date"] = allocation_task_date
            task_history["Action"] = f"{user_delete} left {delete_allocation_task} task"

            if user_delete in members:
                for i in range(len(info_projects)):
                    if info_projects[i].get("Title") == title:
                        for j in range(len(info_projects[i].get("Tasks Data"))):
                            if info_projects[i].get("Tasks Data")[j]["Title"] == delete_allocation_task:
                                if user_delete in info_projects[i].get("Tasks Data")[j]["Assignees"]:
                                    info_projects[i].get("Tasks Data")[j]["Assignees"].remove(user_delete)
                                    info_projects[i].get("Tasks Data")[j]["History"].append(task_history)
                                    console.print(
                                        f"{user_delete} delete from the {delete_allocation_task} task in {title} project",
                                        style="green")
                                    logger.info(
                                        f"{user_delete} delete from the {delete_allocation_task} task in {title} project")

                                    with open("projects.json", "w") as f:
                                        json.dump(info_projects, f, indent=4)
                                else:
                                    console.print(f"{user_delete} not undertaken this task!", style="bold red")
                                passing()
                                break
            else:
                console.print(f"{user_delete} is not a member of {title} project", style="bold red")
                passing()
        else:
            console.print(f"{delete_allocation_task} task is not valid!", style="bold red")
            passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()


def task_change_page():
    table = Table(title="Task Change Page")
    table.add_column("Option", style="blue", justify="center")
    table.add_column("Description")
    table.add_row("[yellow]1[/yellow]", "[blue]Change Title Task[/blue]")
    table.add_row("[yellow]2[/yellow]", "[blue]Change Description Task[/blue]")
    table.add_row("[yellow]3[/yellow]", "[blue]Change Status Task[/blue]")
    table.add_row("[yellow]4[/yellow]", "[blue]Change Priority Task[/blue]")
    table.add_row("[yellow]0[/yellow]", "[red]Back To Task Page[/red]")
    console.print(table)


def task_property_table():
    tasks_data = []
    for i in range(len(info_projects)):
        if title == info_projects[i].get("Title"):
            tasks_data = info_projects[i].get("Tasks Data")
            break

    table = Table(title="Task Status Overview")
    table.add_column("Title", style="cyan")
    table.add_column("Description", style="green")
    table.add_column("Start Date", style="yellow")
    table.add_column("End Date", style="blue")
    table.add_column("Assignees", style="blue")
    table.add_column("Priority", style="cyan")
    table.add_column("Status", style="cyan")
    table.add_column("Comments", style="green")
    table.add_column("History", style="green")

    status_order = {
        "Status.BACKLOG": 5,
        "Status.TODO": 4,
        "Status.DOING": 3,
        "Status.DONE": 2,
        "Status.ARCHIVED": 1,
    }

    sorted_tasks = sorted(tasks_data, key=lambda x: status_order.get(x["Status"], 0))

    for task in sorted_tasks:
        table.add_row(
            str(task["Title"]),
            task["Description"],
            task["Start Date"],
            task["End Date"],
            str(task["Assignees"]),
            str(task["Priority"]),
            str(task["Status"]),
            str(task["Comments"]),
            str(task["History"])
        )
    console.print(table)


def Change_task_info(username):
    info_projects = json.load(open("projects.json", "r"))
    is_leader = is_your_project(username=username)
    is_assignee = False
    valid_task = False
    tasks = []

    if any(title == item.get("Title") for item in info_projects):
        if any(username in item.get("Members") for item in info_projects) or is_leader:
            task_property_table()
            console.print("Enter the title of target task:", style="yellow")
            target_task = str(input())
            for i in range(len(info_projects)):
                if title == info_projects[i].get("Title"):
                    tasks = info_projects[i].get("Tasks")
                    for j in range(len(info_projects[i]["Tasks Data"])):
                        if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                            valid_task = True
                            if username in info_projects[i]["Tasks Data"][j]["Assignees"]:
                                is_assignee = True
                                break
            if valid_task:
                console.print("Do you want to change this task?", style="yellow")
                console.print("1- Yes", style="yellow")
                console.print("2- No", style="yellow")
                choice = str(input())
                if choice == '1':
                    if is_assignee or is_leader:
                        task_change_page()
                        console.print("Enter your select:", style="yellow")
                        choice = str(input())
                        if choice == '1':
                            if target_task in tasks:
                                console.print("Enter the new task title:", style="yellow")
                                new_task_title = str(input())
                                change_title_date = datetime.datetime.now()
                                task_history = dict()
                                task_history["Changing User"] = username
                                task_history["Changing Date"] = change_title_date.strftime("%Y-%m-%d %H:%M:%S")
                                task_history["Action"] = "change title"
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                info_projects[i]["Tasks Data"][j]["Title"] = new_task_title
                                                info_projects[i]["Tasks"] = [new_task_title if x == target_task else x
                                                                             for x in info_projects[i]["Tasks"]]
                                                info_projects[i]["Tasks Data"][j]["History"].append(task_history)
                                                break
                                with open("projects.json", "w") as f:
                                    json.dump(info_projects, f, indent=4)
                                console.print("The task name was successfully renamed", style="green")
                                logger.info(f"The task name was successfully renamed")

                                passing()
                            else:
                                console.print("Invalid task!", style="bold red")
                                passing()
                        elif choice == '2':
                            if target_task in tasks:
                                console.print("Enter the new task description:", style="yellow")
                                new_task_description = str(input())
                                change_title_date = datetime.datetime.now()
                                task_history = dict()
                                task_history["Changing User"] = username
                                task_history["Changing Date"] = change_title_date.strftime("%Y-%m-%d %H:%M:%S")
                                task_history["Action"] = "change description"
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                info_projects[i]["Tasks Data"][j]["Description"] = new_task_description
                                                info_projects[i]["Tasks Data"][j]["History"].append(task_history)
                                                break
                                with open("projects.json", "w") as f:
                                    json.dump(info_projects, f, indent=4)
                                console.print("The task description was successfully changed.", style="green")
                                logger.info(f"The task description was successfully changed")
                                passing()
                            else:
                                console.print("Invalid task!", style="bold red")
                                passing()

                        elif choice == '3':
                            if target_task in tasks:
                                console.print("1- Increase task status", style="yellow")
                                console.print("2- Reduce task status", style="yellow")
                                select = str(input())

                                is_changed = True
                                change_title_date = datetime.datetime.now()
                                task_history = dict()
                                task_history["Changing User"] = username
                                task_history["Changing Date"] = change_title_date.strftime("%Y-%m-%d %H:%M:%S")
                                if select == '1':
                                    task_history["Action"] = "increase status"
                                elif select == '2':
                                    task_history["Action"] = "reduce status"
                                else:
                                    is_changed = False

                                task_description = ""
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                task_description = info_projects[i]["Tasks Data"][j]["Description"]
                                                current_status = info_projects[i]["Tasks Data"][j]["Status"]
                                                if is_changed:
                                                    info_projects[i]["Tasks Data"][j]["History"].append(task_history)
                                                break
                                task = CreateTask(target_task, task_description)
                                status_enum = CreateTask.Status[current_status]
                                task.status = status_enum
                                if select == '1':
                                    can_is_next = task.next_status()
                                elif select == '2':
                                    can_is_previous = task.previous_status()
                                else:
                                    console.print("Invalid choice!", style="black")
                                    passing()
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                info_projects[i]["Tasks Data"][j]["Status"] = str(task.status)[7:]
                                                break
                                if select == '1':
                                    if can_is_next:
                                        console.print("Increase task status was done successfully.", style="green")
                                        logger.info(f"Increase task status was done successfully")
                                        passing()
                                    else:
                                        console.print("Status is out of range!", style="blue")
                                        passing()

                                elif select == '2':
                                    if can_is_previous:
                                        console.print("Reduce task status was done successfully.", style="green")
                                        logger.info(f"Reduce task status was done successfully")
                                        passing()
                                    else:
                                        console.print("Status is out of range!", style="blue")
                                        passing()

                                with open("projects.json", "w") as f:
                                    json.dump(info_projects, f, indent=4)
                            else:
                                console.print("Invalid task!", style="bold red")
                                passing()
                        elif choice == '4':
                            if target_task in tasks:
                                console.print("1- Increase task priority", style="yellow")
                                console.print("2- Reduce task priority", style="yellow")
                                select = str(input())

                                is_changed = True
                                change_title_date = datetime.datetime.now()
                                task_history = dict()
                                task_history["Changing User"] = username
                                task_history["Changing Date"] = change_title_date.strftime("%Y-%m-%d %H:%M:%S")
                                if select == '1':
                                    task_history["Action"] = "increase priority"
                                elif select == '2':
                                    task_history["Action"] = "reduce priority"
                                else:
                                    is_changed = False

                                task_description = ""
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                task_description = info_projects[i]["Tasks Data"][j]["Description"]
                                                current_priority = info_projects[i]["Tasks Data"][j]["Priority"]
                                                if is_changed:
                                                    info_projects[i]["Tasks Data"][j]["History"].append(task_history)
                                                break
                                task = CreateTask(target_task, task_description)
                                priority_enum = CreateTask.Priority[current_priority]
                                task.priority = priority_enum
                                if select == '1':
                                    can_is_next = task.next_priority()
                                elif select == '2':
                                    can_is_previous = task.previous_priority()
                                else:
                                    console.print("Invalid choice!", style="black")
                                    passing()
                                for i in range(len(info_projects)):
                                    if title == info_projects[i].get("Title"):
                                        for j in range(len(info_projects[i]["Tasks Data"])):
                                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                                info_projects[i]["Tasks Data"][j]["Priority"] = str(task.priority)[9:]
                                                break
                                if select == '1':
                                    if can_is_next:
                                        console.print("Increase task priority was done successfully.", style="green")
                                        logger.info(f"Increase task priority was done successfully")
                                        passing()
                                    else:
                                        console.print("Status is out of range!", style="blue")
                                        passing()
                                elif select == '2':
                                    if can_is_previous:
                                        console.print("Reduce task priority was done successfully.", style="green")
                                        logger.info(f"Reduce task priority was done successfully")
                                        passing()
                                    else:
                                        console.print("Status is out of range!", style="blue")
                                        passing()

                                with open("projects.json", "w") as f:
                                    json.dump(info_projects, f, indent=4)
                            else:
                                console.print("Invalid task!", style="bold red")
                                passing()
                        elif choice == '0':
                            pass
                        else:
                            console.print("Invalid choice!", style="black")
                            passing()
                    else:
                        console.print(
                            f"You are not a assignee of {title} project.\nYou can not change the {target_task} task property",
                            style="bold red")
                        passing()
                elif choice == '2':
                    pass
                else:
                    console.print("Invalid key!Please try again.", style="black")
                    passing()
            else:
                console.print("Invalid task!", style="bold red")
                passing()
        else:
            console.print(f"You are not a member of {title} project.", style="bold red")
            passing()
    else:
        console.print("Invalid project!", style="bold red")
        passing()


def show_task_tables(username):
    info_projects = json.load(open("projects.json", "r"))
    flag = is_your_project(username=username)
    tasks_data = []
    backlog_tasks = []
    to_do_tasks = []
    doing_tasks = []
    done_tasks = []
    archived_tasks = []
    for i in range(len(info_projects)):
        if title == info_projects[i].get("Title"):
            tasks_data = info_projects[i].get("Tasks Data")
            break
    for task in tasks_data:
        if task["Status"] == "BACKLOG":
            backlog_tasks.append(task["Title"])
        elif task["Status"] == "TODO":
            to_do_tasks.append(task["Title"])
        elif task["Status"] == "DOING":
            doing_tasks.append(task["Title"])
        elif task["Status"] == "DONE":
            done_tasks.append(task["Title"])
        elif task["Status"] == "ARCHIVED":
            archived_tasks.append(task["Title"])

    if any(title == item.get("Title") for item in info_projects):
        if any(username in item.get("Members") for item in info_projects) or flag:

            table = Table(title="Task Status Overview")
            table.add_column("BACKLOG", style="green")
            table.add_column("TODO", style="cyan")
            table.add_column("DOING", style="yellow")
            table.add_column("DONE", style="blue")
            table.add_column("ARCHIVED", style="red")

            max_length = max(len(backlog_tasks), len(to_do_tasks), len(doing_tasks), len(done_tasks),
                             len(archived_tasks))

            for i in range(max_length):
                table.add_row(
                    backlog_tasks[i] if i < len(backlog_tasks) else "",
                    to_do_tasks[i] if i < len(to_do_tasks) else "",
                    doing_tasks[i] if i < len(doing_tasks) else "",
                    done_tasks[i] if i < len(done_tasks) else "",
                    archived_tasks[i] if i < len(archived_tasks) else "",
                )
            console.print(table)
            passing()
        else:
            console.print(f"You are not a member of {title} project", style="bold red")
            passing()
    else:
        console.print("Invalid project!", style="bold red")
        passing()


def task_comment(username):
    info_projects = json.load(open("projects.json", "r"))
    flag = is_your_project(username=username)
    tasks = []
    for i in range(len(info_projects)):
        if title == info_projects[i].get("Title"):
            tasks = info_projects[i].get("Tasks")

    if any(title == item.get("Title") for item in info_projects):
        if any(username in item.get("Members") for item in info_projects) or flag:
            console.print(tasks)
            console.print("Enter the title of target task:", style="yellow")
            target_task = str(input())
            if target_task in tasks:
                console.print("Enter the comment text:", style="yellow")
                comment_text = str(input())
                comment = dict()
                create_task_date = datetime.datetime.now()
                comment["Text"] = comment_text
                comment["Writer"] = username
                comment["Date"] = create_task_date.strftime("%Y-%m-%d %H:%M:%S")

                for i in range(len(info_projects)):
                    if title == info_projects[i].get("Title"):
                        for j in range(len(info_projects[i]["Tasks Data"])):
                            if info_projects[i]["Tasks Data"][j]["Title"] == target_task:
                                info_projects[i]["Tasks Data"][j].get("Comments").append(comment)
                                break
                with open("projects.json", "w") as f:
                    json.dump(info_projects, f, indent=4)
                    console.print("Create comment was done successfully", style="green")
                    logger.info(f"Create comment by {username} was done successfully")
                    passing()
            else:
                console.print("Invalid task!", style="bold red")
                passing()
        else:
            console.print(f"You are not a member of {title} project", style="bold red")
            passing()
    else:
        console.print("Invalid project!", style="bold red")
        passing()


def admin_login():
    console.print("Enter your username:", style="yellow")
    admin_username = str(input())
    console.print("Enter your password:", style="yellow")
    admin_password = str(input())
    info_admin = json.load(open("admin.json", "r"))
    valid_admin = False
    for i in range(len(info_admin)):
        if info_admin[i]["Username"] == admin_username:
            if info_admin[i]["Password"] == admin_password:
                valid_admin = True
    if valid_admin:
        logger.info(f"Admin {admin_username} logged in")
        while True:
            console.print(f"\n    Welcom {admin_username}\n", style="green")
            console.print("1- Open Account", style="yellow")
            console.print("2- Close Account", style="yellow")
            console.print("0- Exit", style="red")
            select = str(input())
            info_users = json.load(open("users.json", "r"))
            users = []
            for user in info_users:
                users.append(user["Username"])
            is_user_exist = False
            if select == '1':
                console.print(users)
                console.print("Enter username of user:", style="yellow")
                user_username = str(input())
                for i in range(len(info_users)):
                    if info_users[i]["Username"] == user_username:
                        is_user_exist = True
                        if info_users[i]["Is_active"] == True:
                            console.print(f"{user_username} account is already active.", style="blue")
                            passing()
                        else:
                            info_users[i]["Is_active"] = True
                            console.print(f"{user_username} account opend successfully.", style="green")
                            logger.info(f"{user_username} account opend successfully by {admin_username}")
                            passing()
                if not is_user_exist:
                    console.print("User is not exist!", style="bold red")
                with open("users.json", "w") as f:
                    json.dump(info_users, f, indent=4)
            elif select == '2':
                console.print(users)
                console.print("Enter username of user:", style="yellow")
                user_username = str(input())
                for i in range(len(info_users)):
                    if info_users[i]["Username"] == user_username:
                        is_user_exist = True
                        if info_users[i]["Is_active"] == False:
                            console.print(f"{user_username} account is already inactive.", style="blue")
                            passing()
                        else:
                            info_users[i]["Is_active"] = False
                            console.print(f"{user_username} account closed successfully.", style="green")
                            logger.info(f"{user_username} account closed successfully by {admin_username}")
                            passing()
                if not is_user_exist:
                    console.print("User is not exist!", style="bold red")
                with open("users.json", "w") as f:
                    json.dump(info_users, f, indent=4)
            elif select == '0':
                logger.info(f"Admin {admin_username} logged out")
                break
            else:
                console.print("Invalid choice! Please try again.", style="black")
                passing()
    else:
        console.print("Invalid admin!", style="bold red")
        logger.warning(f"Login failed for admin {admin_username}")
        passing()


def create_main_menu():
    table = Table(title="Main menu")
    table.add_column("Option", style="blue", justify="center")
    table.add_column("Description")
    table.add_row("[yellow]1[/yellow]", "[magenta]Create Account[/magenta]")
    table.add_row("[yellow]2[/yellow]", "[magenta]User Login[/magenta]")
    table.add_row("[yellow]3[/yellow]", "[magenta]Admin Login[/magenta]")
    table.add_row("[yellow]0[/yellow]", "[red]Exit[/red]")
    console.print(table)


def account_page():
    table = Table(title="Account Page")
    table.add_column("Option", style="blue", justify="center")
    table.add_column("Description")
    table.add_row("[yellow]1[/yellow]", "[magenta]Create New Project[/magenta]")
    table.add_row("[yellow]2[/yellow]", "[magenta]Add user in project[/magenta]")
    table.add_row("[yellow]3[/yellow]", "[magenta]delete user in project[/magenta]")
    table.add_row("[yellow]4[/yellow]", "[magenta]delete project[/magenta]")
    table.add_row("[yellow]5[/yellow]", "[magenta]List of projects in which you are the leader[/magenta]")
    table.add_row("[yellow]6[/yellow]", "[magenta]List of projects in which you are a regular member[/magenta]")
    table.add_row("[yellow]7[/yellow]", "[magenta]Task[/magenta]")
    table.add_row("[yellow]0[/yellow]", "[red]Logout[/red]")
    console.print(table)


def task_page():
    table = Table(title="Task Page")
    table.add_column("Option", style="blue", justify="center")
    table.add_column("Description")
    table.add_row("[yellow]1[/yellow]", "[blue]Task Definition[/blue]")
    table.add_row("[yellow]2[/yellow]", "[blue]Task Delete[/blue]")
    table.add_row("[yellow]3[/yellow]", "[blue]Task Allocation[/blue]")
    table.add_row("[yellow]4[/yellow]", "[blue]Task Delete Allocation[/blue]")
    table.add_row("[yellow]5[/yellow]", "[blue]Make Changes In Tasks[/blue]")
    table.add_row("[yellow]6[/yellow]", "[blue]Show Project Tasks Tables[/blue]")
    table.add_row("[yellow]7[/yellow]", "[blue]Task comment Definition[/blue]")
    table.add_row("[yellow]0[/yellow]", "[red]Back To Account Page[/red]")
    console.print(table)


def menu():
    while True:
        create_main_menu()
        user = Account()

        console.print("Enter your select...", style="bold yellow")
        choice = input()
        os.system('cls' if os.name == 'nt' else 'clear')

        if choice == '1':
            console.print("Enter your username..", style="blue")
            username = input()
            console.print("Enter your password..", style="blue")
            password = input()
            console.print("Enter your email..", style="blue")
            email = input()
            user.register(user_name=username, password=password, email=email)

        elif choice == '2':
            console.print("Enter your username..", style="blue")
            username = str(input())
            console.print("Enter your password..", style="blue")
            password = input()
            user.login(user_name=username, password=password)

            while user.logged_in:
                account_page()
                console.print("Enter your select...", style="bold yellow")
                choice = input()
                os.system('cls' if os.name == 'nt' else 'clear')

                if choice == '1':
                    console.print("Please choose a title for your project", style="bold yellow")
                    title = input()
                    info_users = json.load(open("users.json", "r"))
                    info_projects = json.load(open("projects.json", "r"))
                    if not any(title == item.get("Title") for item in info_projects):
                        for i in range(len(info_users)):
                            if info_users[i].get("Username") == username:
                                info_users[i].get("Leader_member").append(title)
                                with open("users.json", "w") as f:
                                    json.dump(info_users, f, indent=4)

                        project = CreateProject(title)
                        # console.print("The construction of the project was completed successfully", style= "bold green")
                        logger.info(f"The construction of the {title} project was created")

                        while True:
                            console.print("Please enter the title of the task you want to define", style="yellow")
                            add_task_title = str(input())
                            console.print("Please enter the description of the task", style="yellow")
                            add_task_description = str(input())
                            task = CreateTask(add_task_title, add_task_description)
                            project.add_task(task=task)
                            info_users = json.load(open("users.json", "r"))
                            leader_id = next(
                                (item.get("ID") for item in info_users if username == item.get("Username")), None)
                            project.save_information(leader_id=leader_id)
                            console.print(f"{add_task_title} task defined in {title} project", style="green")
                            logger.info(f"{add_task_title} task defined in {title} project", style="green")
                            console.print("\nIf you want to end the definition of the task, enter the 0 key",
                                          style="black")
                            console.print("If you want to define a new task, enter a any key (except 0)", style="black")
                            console.print("Enter your choice...", style="yellow")
                            choice = str(input())
                            if choice == '0':
                                console.print("The construction of the project was completed successfully",
                                              style="green")
                                break
                            else:
                                continue
                    else:
                        console.print(f"Project {title} has already been created.", style="bold red")
                        passing()
                        os.system('cls' if os.name == 'nt' else 'clear')

                elif choice == '2':
                    add_user_project(username=username)

                elif choice == '3':
                    delete_user_project(username=username)

                elif choice == '4':
                    delete_project(username=username)

                elif choice == '5':
                    info_users = json.load(open("users.json", "r"))
                    for i in range(len(info_users)):
                        if info_users[i].get("Username") == username:
                            console.print("List of projects in which you are the leader: ", style="blue")
                            if info_users[i].get("Leader_member"):
                                console.print(info_users[i].get("Leader_member"))
                                passing()
                                break
                            else:
                                console.print("Nothing found!", style="black")
                                passing()
                                break

                elif choice == '6':
                    info_users = json.load(open("users.json", "r"))
                    for i in range(len(info_users)):
                        if info_users[i].get("Username") == username:
                            console.print("List of projects in which you are a regular member: ", style="blue")
                            if info_users[i].get("Regular_member"):
                                console.print(info_users[i].get("Regular_member"))
                                passing()
                                break
                            else:
                                console.print("Nothing found!", style="black")
                                passing()
                                break

                elif choice == '7':
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        task_page()
                        console.print("Enter your select...", style="bold yellow")
                        choice = input()

                        if choice == '1':
                            task_definition(username=username)

                        elif choice == '2':
                            task_delete(username=username)

                        elif choice == '3':
                            task_allocation(username=username)

                        elif choice == '4':
                            delete_task_allocation(username=username)

                        elif choice == '5':
                            Change_task_info(username=username)

                        elif choice == '6':
                            show_task_tables(username=username)

                        elif choice == '7':
                            task_comment(username=username)
                        elif choice == '0':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break
                        else:
                            console.print("Invalid choice.Please try again.", style="black")
                            passing()
                            continue
                elif choice == '0':
                    logger.info(f"User {username} logged out")
                    break
                else:
                    console.print("Invalid choice.Please try again.", style="black")
                    continue

        elif choice == '3':
            admin_login()
        elif choice == '0':
            break
        else:
            console.print("Invalid choice.Please try again", style="black")
            continue


if __name__ == "__main__":
    menu()
