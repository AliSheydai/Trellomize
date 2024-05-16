import argparse
import json
import sys


def create_admin(user_name, password):
    admin_file = "admin.json"

    manager_info = dict()
    manager_info["Username"] = user_name
    manager_info["password"] = password

    data = json.load(open(admin_file, "r"))

    for item in data:
        if user_name == item.get("username"):
            print("Error: The system manager is already built.")
            return
    data.append(manager_info)
    with open(admin_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Admin '{user_name}' created successfully!")


def main():
    parser = argparse.ArgumentParser(description="Create system administrator information")
    parser.add_argument("create-admin", help="Create an admin")
    parser.add_argument("--username", help="Admin username")
    parser.add_argument("--password", help="Admin password")

    args = parser.parse_args(sys.argv[1:])

    create_admin(args.username, args.password)


if __name__ == "__main__":
    main()
