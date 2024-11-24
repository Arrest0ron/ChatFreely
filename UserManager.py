import json

def read_json_contents(filename : str):
    try:
        with open(filename, "r") as file:
            try:
                contents = json.load(file)
            except json.JSONDecodeError as err:
                print(f"config.json format error in {err.doc}")
                print(f"Error: {err.msg}")
                print(f"At line: {err.lineno}, coloumn: {err.colno}")
                print(f"Pos: {err.pos}")
                file.seek(0)
                old_contents = file.readlines()
                with open(f"{filename}.old", "w") as old_file:
                    old_file.writelines(old_contents)
                contents = { "Users" : []}
                with open("config.json", "w") as file:
                    json.dump(contents, file, indent=4)
    except FileNotFoundError:
        print("Creating config.json...")
        contents = { "Users" : []}
        with open("config.json", "w") as file:
            json.dump(contents, file, indent=4)
    except Exception:
        print("Unknown exception.")
        raise Exception("The end.")
    return contents

def add_user(User):
    contents = read_json_contents("config.json")
    with open("config.json", "w") as file:
        contents["Users"].append(User)
        json.dump(contents, file, indent=4)
        
def list_users():
    contents = read_json_contents("config.json")
    if contents["Users"]:
        print("Here is the list of all the users (username@host):")
        print("_________________________________________________\n")
        [print(i) for i in [_["username"]+"@"+_["host"] for _ in contents["Users"]]]
        print("_________________________________________________\n")  
    else:
        print("Database is empty\n")
        
def remove_user(username):
    contents = read_json_contents("config.json")
    with open("config.json", "w") as file:
        index = 0
        for i in contents["Users"]:
            if i["username"] == username:
                break
            index+=1
        else:
            print(f"User '{username}' not found")
            json.dump(contents, file, indent=4)
            return
        del contents["Users"][index]
        json.dump(contents, file, indent=4)

def update_user(username):
    contents = read_json_contents("config.json")
    with open("config.json", "r") as file:
        index = 0
        for i in contents["Users"]:
            if i["username"] == username:
                break         
            index +=1
        else:
            print(f"User '{username}' not found. ")     
            return
    while True:
        print("What you would like to change?")
        print("1.username")
        print("2.host")
        print("3.password")
        print("4.database")
        print("5.Save and exit edit menu")
        
        a =input()
        if not a.isdecimal():
            print("Please, enter number from 1 to 5. Try again")
            continue
        a = int(a)
        if (a < 1) or (a > 5):
            print("Incorrect choice. Try again")
            continue
        
        if a == 1:
            new_username = str(input(f"Enter new username (Non-empty) for {username}: "))
            if not new_username:
                print("Username can't be empty. Try again")
                continue
            contents["Users"][index]["username"] = new_username
        if a == 2:
            new_host = str(input(f"Enter new host (default = localhost) for {username}: "))
            if not new_host:
                new_host = "localhost"
            contents["Users"][index]["host"] = new_host
        if a == 3:
            new_password = str(input(f"Enter new password (default = None) for {username}: "))
            contents["Users"][index]["password"] = new_password
        if a == 4:
            new_database = str(input(f"Enter new database (default = None) for {username}: "))
            contents["Users"][index]["database"] = new_database
        if a == 5:
            break
    with open("config.json", "w") as file:
        json.dump(contents, file, indent=4)
  
def get_credentials(username):
    contents = read_json_contents("config.json")
    index = 0
    for i in contents["Users"]:
        if i["username"] == username:
            break
        index +=1
    else:
        print(f"User {username} not found")
        return None
    return contents["Users"][index]       
    
def get_key():
    contents = read_json_contents("API.json")
    return contents["API"]
    
def main(): 
    while (True):
        print(f"Welcome to the UserManager control panel")
        print("----------------------------------------")
        print("1.Add new user credentials")
        print("2.Remove user credentials")
        print("3.List users")
        print("4.Update user")
        print("5.Exit")
        
        a =input()
        if not a.isdecimal():
            print("Please, enter number from 1 to 5. Try again")
            continue
        a = int(a)
        if (a < 1) or (a > 5):
            print("Incorrect choice. Try again")
            continue
        if a == 1:
            print("Please, enter your:")            
            User = {
            "username" : str(input("username (Non empty): ")),
            "host"     : str(input("host     (default = localhost): ")), 
            "password" : str(input("password (default = None): ")),
            "database" : str(input("database (default = None): "))
            }                
            if not User["username"]:
                print("Incorrect username. Try again\n")
                continue
            if not User["host"]:
                User["host"] = "localhost"
            add_user(User)  
        if a == 2:
            remove_user(str(input("username(Non empty): ")))
        if a == 3:
            list_users()
        if a == 4:
            update_user(str(input("username (Non empty): ")))
        if a == 5:
            break
      
if __name__ == "__main__":
    main()
    
    