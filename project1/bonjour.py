from cryptography.fernet import Fernet

def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    with open("key.key", "rb") as key_file:
        key = key_file.read()
    return key

# Generate a key (run this part once to create the key.key file)
write_key()

# Load the key
master_pwd = input("What is the master password: ")
key = load_key() + master_pwd.encode()
fer = Fernet(key)

def view():
    with open("passwords.txt", "r") as f:
        for line in f.readlines():
            data = line.strip()
            user, passw = data.split("/")
            print(f"User: {user}, Password: {str(fer.decrypt(passw.encode()))}\n",
            fer.decrypt(passw.encode()).decode())

def add():
    name = input("Account name: ")
    pwd = input("Password: ")

    with open("passwords.txt", "a") as f:
        f.write(f"{name}/{fer.encrypt(pwd.encode()).decode()}\n")

while True:
    mode = input("Would you like to add a new password or view existing ones? (add/view), press q to quit: ").lower()
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid input. Please enter 'add' or 'view'.")
