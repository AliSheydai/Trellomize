# import rich
import os
import json
import re


class Account:
    def __init__(self):
        self.data = []
        self.user_detail_list = []
        self.user_info = dict()
        self.logged_in = False

    def register(self, email, user_name, password):
        self.user_info["gmail"] = email
        self.user_info["Username"] = user_name
        self.user_info["Password"] = password
        self.data = json.load(open("users.json", "r"))

        def is_valid_gmail():
            pattern = r"^[A-Z|a-z][A-Z|a-z|0-9|\.|_|-]*@[\w|\d|_|-]+\.[\w]+$"
            if not re.fullmatch(pattern, email):
                print("Invalid gmail ! please enter valid gmail")
                return False
            return True

        def is_valid_username():
            if len(str(user_name)) < 5 or len(str(user_name)) > 14:
                print("Invalid userName ! please enter userName greater than 5 and less than 14 character")
                return False
            return True

        def is_valid_password():
            if len(str(password)) < 5 or len(str(password)) > 18:
                print("Enter password greater than 5 and less than 18 character")
                return False
            return True

        def is_exist_file():
            if os.path.exists(f"{user_name}.txt"):
                print("This username is already exist.")
                return False
            return True

        if is_valid_username() and is_valid_gmail() and is_valid_password() and is_exist_file():
            self.data.append(self.user_info)
            with open("users.json", "w") as f:
                json.dump(self.data, f, indent=4)
            print("Account created successfully")

    def login(self, user_name, password):
        if os.path.exists(f"{user_name}.txt"):
            with open(f"{user_name}.txt", "r") as f:
                details = f.read()
                self.user_detail_list = details.split("\n")
                if str(user_name) in str(self.user_detail_list):
                    if str(password) in str(self.user_detail_list):
                        self.logged_in = True
                if self.logged_in:
                    print(f"{user_name} logged in")
                else:
                    print("The username or password entered is invalid.")
        else:
            print("There is no file with this username.")