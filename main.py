from rich import console
from rich.table import Table
import os
import json
import re
import uuid
import datetime
from enum import Enum
import bcrypt

console = console.Console()

class Model:
    def __init__(self):
        self.id = uuid.uuid4()
        self.users = []

    def add_users(self, user):
        self.users.append(user)

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

def passing():
    console.print("Enter any key to continue..", style= "black")
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
        self.user_info["Hash_password_str"] = hash_password(password).decode('utf8')
        # self.Hash_password = hash_password(password)
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
            return True
        else:
            return False

    def login(self, user_name, password):
        self.user_data = json.load(open("users.json", "r"))
        for item in self.user_data:
            if user_name == item.get("Username"):
                if item.get("Is_active") == "No":
                    console.print("The user account has been closed by the system administrator."
                                  " You are not allowed to access the account!\n", style="bold red")
                    return False
                # if hash_password(password) == item.get("Hash_password"):
                if verify_password(password, item.get("Hash_password_str").encode('utf8')):
                    console.print(f"\nWelcome {user_name}",
                                  style="bold green")
                    self.logged_in = True
                    return True
                else:
                    console.print("You have entered the wrong password!\n", style="bold red")
                    return False

        if not self.logged_in:
            console.print("The username entered is not valid!\n", style="bold red")

    def add_project(self, project):
        self.projects.append(project)
            
class CreateProject(Model):
    def __init__(self, title):
        self.id = str(Model())
        self.project_data = []
        self.project_details = dict()
        self.title = title
        self.members = []
        self.project_details["Project_ID"] = str(self.id)
        self.tasks = []
        self.tasks_data = []

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
             "Priority": str(task.priority),
             "Status": str(task.status),
             "Comments": task.comments,} for task in self.tasks
        ]
        self.project_data = json.load(open("projects.json", "r"))
        for i in range(len(self.project_data)):
            if self.project_data[i]["Project_ID"] == self.id:
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
        # self.data = []
        # self.data2 = []
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
        self.comment = dict()
        self.comment_text = ""
        self.comment_writer = ""
        # self.exist_file = False
        # if not self.exist_file:
        #     with open(f"{title_project}_tasks.json", "w") as f:
        #             json.dump([], f, indent=4)
        #             self.exist_file = True

    def save_info(self, title_project):
        # self.data1 = json.load(open("projects.json", "r"))
        # # self.data2 = []
        # for item in self.data1:
        #     if item.get("Title") == title_project:
        #         self.data2 = item.get("Tasks Data")

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
        # if os.path.isfile(f"{title_project}_tasks.json"):
        self.task_data = json.load(open(f"{title_project}_tasks.json", "r"))
        self.task_data.append(self.task_properties)
        with open(f"{title_project}_tasks.json", "w") as f:
            json.dump(self.task_data, f, indent=4)
        # else:
        #     with open(f"{title_project}_tasks.json", "w") as f:
        #         json.dump([], f, indent=4)
        # self.data2.append(self.task_properties)
        # for item in self.data1:
        #     if item.get("Title") == title_project:
        #         item["Tasks Data"] = self.data2
        #     break
        # with open("projects.json", "w") as f:
        #             json.dump(self.data1, f, indent=4)

    def write_comment(self, text, username):
        self.comment_text = text
        self.comment_writer = username
        self.comment_date = datetime.datetime.now()
        self.comment["Text"] = self.comment_text
        self.comment["Writer"] = self.comment_writer
        self.comment["Record Date"] = self.comment_date
        self.comments.append(self.comment)

    def set_status(self, new_status):
        if new_status in CreateTask.Status:
            self.status = new_status
        else:
            print(f"Invalid status: {new_status}")

    def set_priority(self, new_priority):
        if new_priority in CreateTask.Priority:
            self.status = new_priority
        else:
            print(f"Invalid priority: {new_priority}")

    def next_status(self):
        current_value = self.status.value
        next_value = (current_value % len(CreateTask.Status)) + 1
        self.status = CreateTask.Status(next_value)

    def next_priority(self):
        current_value = self.priority.value
        next_value= (current_value % len(CreateTask.Priority)) + 1
        self.priority = CreateTask.Priority(next_value)

    def task_allocation(self, username):
        is_exist_project = False
        tasks = []
        members = []
        console.print("Enter title of your project", style="yellow")
        title = input()
        info_projects = json.load(open ("projects.json", "r"))
        info_users = json.load(open ("users.json", "r"))
        
        for item in info_projects:
            if title == item.get("Title"):
                if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                    tasks = item.get("Tasks")
                    members = item.get("Members")
                    is_exist_project = True
                    break
                    
        if is_exist_project:
            console.print(f"Tasks: {tasks}")   
            console.print("Please enter the name of the task you want to allocation", style= "yellow")
            allocation_task = str(input())
            if allocation_task in tasks:
                console.print(f"Members: {members}") 
                console.print("Enter the name of the person you want to assign the task", style="yellow")
                user_alloc = str(input())
                if user_alloc in members:
                    self.assignees.append(user_alloc)
                else:
                    console.print("User is not valid!", style="bold red")
            else: 
                console.print(f"{allocation_task} task is not valid!", style="bold red")

    # def task_definition(self, username, user_obj):
    #     is_exist_project = False
    #     console.print("Enter title of your project", style="yellow")
    #     title = str(input())
    #     info_projects = json.load(open ("projects.json", "r"))
    #     info_users = json.load(open ("users.json", "r"))
        
    #     for item in info_projects:
    #         if title == item.get("Title"):
    #             if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
    #                 is_exist_project = True
                    
    #     if is_exist_project:
    #         console.print("Please enter the title of the task you want to define", style= "yellow")
    #         add_task_title = str(input())
    #         self.title = add_task_title
    #         console.print("Please enter the description of the task", style= "yellow")
    #         add_task_description = str(input())
    #         self.description = add_task_description
    #         for i in range(len(info_projects)):
    #             if info_projects[i].get("Title") == title:
    #                 info_projects[i].get("Tasks").append(add_task_title)
    #                 console.print(f"{add_task_title} task defined in {title} project", style="green")
                    
    #                 # task = CreateTask(add_task_title, add_task_description)
    #                 for project in user_obj.projects:
    #                     if project.title == title:
    #                         project.add_task(self)
    #                         leader_id = next((item.get("ID") for item in info_users if username == item.get("Username")), None)
    #                         project.save_information(leader_id)
    #                 # with open("projects.json", "w") as f:
    #                 #     json.dump(info_projects, f, indent=4)
    #                 passing()
    #                 break
    # def delete_task_allocation(self, username):
    #     is_exist_project = False
    #     tasks = []
    #     members = []
    #     console.print("Enter title of your project", style="yellow")
    #     title = input()
    #     info_projects = json.load(open ("projects.json", "r"))
    #     info_users = json.load(open ("users.json", "r"))
        
    #     for item in info_projects:
    #         if title == item.get("Title"):
    #             if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
    #                 tasks = item.get("Tasks")
    #                 members = item.get("Members")
    #                 is_exist_project = True
    #                 break
                    
    #     if is_exist_project:
    #         console.print(f"Tasks: {tasks}")   
    #         console.print("Please enter the name of the task you want to delete allocation", style= "yellow")
    #         delete_allocation_task = str(input())
    #         if delete_allocation_task in tasks:
    #             console.print(f"Members: {members}") 
    #             console.print("Enter the name of the person you want to picking up the task", style="yellow")
    #             user_delete = str(input())
    #             if user_delete in members:
    #                 self.assignees.append(user_delete)
    #             else:
    #                 console.print("User is not valid!", style="bold red")
    #         else: 
    #             console.print(f"{delete_allocation_task} task is not valid!", style="bold red")


def delete_project(username):
    is_exist_project = False
    console.print("Enter title of your project", style="yellow")
    title = input()
    info_projects = json.load(open ("projects.json", "r"))
    info_users = json.load(open ("users.json", "r"))
    
    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                is_exist_project = True
                
    if is_exist_project:
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                del info_projects[i]
                with open("projects.json", "w") as f:
                    json.dump(info_projects, f, indent=4)   

                console.print("The project was deleted successfully.", style= "green")
                for i in range(len(info_users)):
                        if info_users[i].get("Username") == username:
                            info_users[i].get("Leader_member").remove(title)
                            with open("users.json", "w") as f:
                                json.dump(info_users, f, indent=4)
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project.", style="bold red")


def add_user_project(username):
    is_exist_project = False
    console.print("Enter title of your project", style="yellow")
    title = input()
    info_projects = json.load(open ("projects.json", "r"))
    info_users = json.load(open ("users.json", "r"))
    
    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                is_exist_project = True
                
    if is_exist_project:
        console.print("Please enter the username you want to add to the project", style= "yellow")
        add_user_name = str(input())
        info_users = json.load(open ("users.json", "r"))
        if any(add_user_name in item.get("Username") for item in info_users):
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
                    console.print(f"{add_user_name} added to {title} project", style= "green")
        else:
            console.print("Entered username is not valid!", style="bold red")
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project", style="bold red")

def delete_user_project(username):
    is_exist_project = False
    console.print("Enter title of your project", style="yellow")
    title = input()
    info_projects = json.load(open ("projects.json", "r"))
    info_users = json.load(open ("users.json", "r"))
    
    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                is_exist_project = True
                
    if is_exist_project:
        console.print("Please enter the username you want to add to the project", style= "yellow")
        delete_user_name = str(input())
        info_users = json.load(open ("users.json", "r"))
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                if delete_user_name in info_projects[i].get("Members"):
                    info_projects[i].get("Members").remove(delete_user_name)
                    with open("projects.json", "w") as f:
                        json.dump(info_projects, f, indent=4)   

                    for i in range(len(info_users)):
                        if info_users[i].get("Username") == delete_user_name:
                            info_users[i].get("Regular_member").remove(title)
                            with open("users.json", "w") as f:
                                json.dump(info_users, f, indent=4)
                    console.print(f"{delete_user_name} deleted from {title} project", style= "green")
                else:
                    console.print("Entered username is not valid!", style="bold red")
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project", style="bold red")

def create_main_menu():
    table = Table(title="Main menu")
    table.add_column("Option", style="blue", justify="center")
    table.add_column("Description")
    table.add_row("[yellow]1[/yellow]", "[magenta]Create Account[/magenta]")
    table.add_row("[yellow]2[/yellow]", "[magenta]Login[/magenta]")
    table.add_row("[yellow]3[/yellow]", "[red]Exit[/red]")
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
    table.add_row("[yellow]4[/yellow]", "[blue]Task Field Definition[/blue]")
    table.add_row("[yellow]0[/yellow]", "[red]Back To Account Page[/red]")
    console.print(table)

def task_definition(username, user_obj):
    is_exist_project = False
    console.print("Enter title of your project", style="yellow")
    title = str(input())
    info_projects = json.load(open ("projects.json", "r"))
    info_users = json.load(open ("users.json", "r"))
    
    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                is_exist_project = True
                
    if is_exist_project:
        console.print("Please enter the title of the task you want to define", style= "yellow")
        add_task_title = str(input())
        console.print("Please enter the description of the task", style= "yellow")
        add_task_description = str(input())
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                info_projects[i].get("Tasks").append(add_task_title)
                console.print(f"{add_task_title} task defined in {title} project", style="green")
                
                task = CreateTask(add_task_title, add_task_description)
                for project in user_obj.projects:
                    if project.title == title:
                        project.add_task(task)
                        leader_id = next((item.get("ID") for item in info_users if username == item.get("Username")), None)
                        project.save_information(leader_id)

                passing()
                break
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()

def task_delete(username):
    is_exist_project = False
    console.print("Enter title of your project", style="yellow")
    title = input()
    info_projects = json.load(open ("projects.json", "r"))
    info_users = json.load(open ("users.json", "r"))
    
    for item in info_projects:
        if title == item.get("Title"):
            if item.get("Leader_ID") == next((item.get("ID") for item in info_users if username == item.get("Username")), None):
                is_exist_project = True
                
    if is_exist_project:
        console.print("Please enter the name of the task you want to delete", style= "yellow")
        delete_task = str(input())
        for i in range(len(info_projects)):
            if info_projects[i].get("Title") == title:
                if delete_task in info_projects[i].get("Tasks"):
                    info_projects[i].get("Tasks").remove(delete_task)
                    console.print(f"{delete_task} task delete from {title} project", style="green")
                    for j in range(len(info_projects[i].get("Tasks Data"))):
                        if info_projects[i].get("Tasks Data")[j]["Title"] == delete_task:
                            del info_projects[i].get("Tasks Data")[j]
                    with open("projects.json", "w") as f:
                        json.dump(info_projects, f, indent=4)
                    passing()
                    break
                else:
                    console.print("Enterd task is not valid!", style="bold red")
                    passing()
    else:
        console.print("This project is not valid!\nOr you are not the leader of this project!", style="bold red")
        passing()
    

def menu():
    model = Model()
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
            if user.register(username, password, email):
                model.add_users(user)


        elif choice == '2':
            console.print("Enter your username..", style="blue")
            username = str(input())
            console.print("Enter your password..", style="blue")
            password = input()
            user.login(username, password)
            while user.logged_in:
                account_page()
                console.print("Enter your select...", style="bold yellow")
                choice = input()
                os.system('cls' if os.name == 'nt' else 'clear')

                if choice == '1':
                    console.print("Please choose a title for your project", style="bold yellow")
                    title_project = input()
                    info_users = json.load(open ("users.json", "r"))
                    info_projects = json.load(open ("projects.json", "r"))
                    if not any(title_project == item.get("Title") for item in info_projects):
                        for i in range(len(info_users)):
                            if info_users[i].get("Username") == username:
                                info_users[i].get("Leader_member").append(title_project)
                                with open("users.json", "w") as f:
                                    json.dump(info_users, f, indent=4)
                        
                        project = CreateProject(title_project)
                        for user in model.users:
                            if user.user_name == username:
                                user.add_project(project)
                        console.print("The construction of the project was completed successfully", style= "bold green")

                        while True:
                            console.print("Please enter the title of the task you want to define", style= "yellow")
                            add_task_title = str(input())
                            console.print("Please enter the description of the task", style= "yellow")
                            add_task_description = str(input())
                            task = CreateTask(add_task_title, add_task_description)
                            project.add_task(task)
                            info_users = json.load(open ("users.json", "r"))
                            leader_id = next((item.get("ID") for item in info_users if username == item.get("Username")), None)
                            project.save_information(leader_id)
                            console.print("\nIf you want to end the definition of the task, enter the 0 key", style="black")
                            console.print("If you want to define a new task, enter a any key (except 0)",style="black")
                            console.print("Enter your choice...", style="yellow")
                            choice = str(input())
                            if choice == '0':
                                console.print("The construction of the project was completed successfully", style= "green")
                                break
                            else:
                                continue
                    else:
                        console.print(f"Project {title_project} has already been created.", style="bold red")
                        passing()
                        os.system('cls' if os.name == 'nt' else 'clear')

                elif choice == '2':
                    add_user_project(username)

                elif choice == '3':
                    delete_user_project(username)

                elif choice == '4':
                    delete_project(username)
                    
                elif choice == '5':
                   info_users = json.load(open ("users.json", "r"))
                   for i in range(len(info_users)):
                    if info_users[i].get("Username") == username:
                                console.print("List of projects in which you are the leader: ", style="blue")
                                if info_users[i].get("Leader_member"):
                                    console.print(info_users[i].get("Leader_member"))
                                    break
                                else:
                                    console.print("Nothing found!", style="black")
                                    break
            
                elif choice == '6':
                   info_users = json.load(open ("users.json", "r"))
                   for i in range(len(info_users)):
                    if info_users[i].get("Username") == username:
                                console.print("List of projects in which you are a regular member: ", style="blue")
                                if info_users[i].get("Regular_member"):
                                    console.print(info_users[i].get("Regular_member"))
                                    break
                                else:
                                    console.print("Nothing found!", style="black")
                                    break
                
                elif choice == '7':
                    while True:
                        os.system('cls' if os.name == 'nt' else 'clear')
                        task_page()
                        console.print("Enter your select...", style="bold yellow")
                        choice = input()

                        if choice == '1':
                            task_definition(username, user)

                        elif choice == '2':
                            task_delete(username)
                    
                        elif choice == '0':
                            os.system('cls' if os.name == 'nt' else 'clear')
                            break
                        else:
                            console.print("Invalid choice.Please try again.", style="bold red")
                            passing()
                            continue
                elif choice == '0':
                    break
                else:
                    console.print("Invalid choice.Please try again.", style="bold red")
                    continue

        elif choice == '3':
            break
        else:
            console.print("Invalid choice.Please try again", style="bold red")
            continue


if __name__ == "__main__":
    menu()

