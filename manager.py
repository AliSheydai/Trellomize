import argparse
import json
import sys
import os


def create_admin(username, password):
    admin_file = "admin.json"

    manager_info = dict()
    manager_info["username"] = username
    manager_info["password"] = password

    data = json.load(open(admin_file, "r"))

    for item in data:
        if username == item.get("username"):
            print("Error: The system manager is already built.")
            return
    data.append(manager_info)
    with open(admin_file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Admin '{username}' created successfully!")


def purge_data():
    response = input("Are you sure you want to purge all data? This action cannot be undone. (yes/no): ")

    if response.lower() != "yes":
        print("Data purge aborted.")
        return

    data_file = "manager.json"

    try:
        os.remove(data_file)
        print("All data has been purged successfully.")
    except FileNotFoundError:
        print(f"Error: '{data_file}' not found.")


def main():
    parser = argparse.ArgumentParser(description="Create system administrator information")
    parser.add_argument("command", help="Command to execute")
    parser.add_argument("--username", help="Admin username")
    parser.add_argument("--password", help="Admin password")

    args = parser.parse_args()

    if args.command == "create-admin":
        create_admin(args.username, args.password)
    elif args.command == "purge-data":
        purge_data()


if __name__ == "__main__":
    main()
