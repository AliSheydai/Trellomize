from rich import console
import os
import json
import re
import uuid
import datetime

console = console.Console()


class Account:
    def __init__(self):
        self.data = []
        self.user_detail_list = []
        self.user_info = dict()
        self.logged_in = False
        self.active_user_account = True

    def register(self, user_name, password, email):
        self.user_info["gmail"] = email
        self.user_info["Username"] = user_name
        self.user_info["Password"] = password
        self.user_info["Is_active"] = "No" if not self.active_user_account else "Yes"
        self.data = json.load(open("users.json", "r"))

        def is_valid_gmail():
            pattern = r"^[A-Z|a-z][A-Z|a-z|0-9|\.|_|-]*@[\w|\d|_|-]+\.[\w]+$"
            if not re.fullmatch(pattern, email):
                console.print("Invalid gmail ! please enter valid gmail\n", style="bold red")
                return False
            return True

        def is_valid_username():
            if len(str(user_name)) < 5 or len(str(user_name)) > 14:
                console.print("Invalid userName ! please enter userName greater than 5 and less than 14 character\n",
                              style="bold red")
                return False
            return True

        def is_valid_password():
            if len(str(password)) < 5 or len(str(password)) > 18:
                console.print("Enter password greater than 5 and less than 18 character", style="bold red")
                return False
            return True

        def is_exist_file():
            if os.path.exists(f"{user_name}.txt"):
                console.print("This username is already exist.\n", style="bold red")
                return False
            return True

        if is_valid_username() and is_valid_gmail() and is_valid_password() and is_exist_file():
            self.data.append(self.user_info)
            with open("users.json", "w") as f:
                json.dump(self.data, f, indent=4)
            console.print("Account created successfully\n", style="bold green")
            self.active_user_account = True

    def login(self, user_name, password):
        self.data = json.load(open("users.json", "r"))
        for item in self.data:
            if user_name == item.get("Username"):
                if item.get("Is_active") == "No":
                    console.print("The user account has been closed by the system administrator."
                                  " You are not allowed to access the account!\n", style="bold red")
                    return
                if password == item.get("Password"):
                    console.print(f"Welcome. Login to user account {user_name} was done successfully.\n",
                                  style="bold green")
                    self.logged_in = True
                else:
                    console.print("You have entered the wrong password!\n", style="bold red")

        if not self.logged_in:
            console.print("The username entered is not valid!\n", style="bold red")


class CreateTask:
    def __init__(self):
        self.task_properties = []
        self.task_unique_identifier = uuid.uuid4()
        self.title = ""
        self.description = ""
        start_time = datetime.datetime.now()
        self.start_time = start_time.time()
        self.start_date = start_time.date()
        end_datetime = start_time + datetime.timedelta(hours=24)
        self.end_time = end_datetime.time()
        self.end_date = end_datetime.date()
        self.assignees = []
        self.priority = "LOW"
        self.status = "BACKLOG"

    def set_title(self, title):
        self.title = title

    def set_description(self, description):
        self.description = description

    def get_title(self):
        return self.title

    def get_description(self):
        return self.description

    def get_start_time(self):
        return self.start_time

    def get_start_date(self):
        return self.start_date

    def get_end_time(self):
        return self.end_time

    def get_end_date(self):
        return self.end_date

    def set_priority(self, priority):
        self.priority = priority

    def set_status(self, status):
        self.status = status

    def add_assignees(self, assignee):
        self.assignees.append(assignee)


def menu():
    while True:
        print("1_ Create account\n"
              "2_ Login to to your account\n"
              "3_ Exit")
        console.print("Enter your select...", style="bold yellow")
        choice = int(input())
        os.system('cls' if os.name == 'nt' else 'clear')
        user = Account()

        if choice == 1:
            console.print("Enter your username..", style="blue")
            username = input()
            console.print("Enter your password..", style="blue")
            password = input()
            console.print("Enter your email..", style="blue")
            email = input()
            user.register(username, password, email)

        elif choice == 2:
            console.print("Enter your username..", style="blue")
            username = input()
            console.print("Enter your password..", style="blue")
            password = input()
            user.login(username, password)
        else:
            break


if __name__ == "__main__":
    menu()
