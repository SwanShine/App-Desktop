import tkinter as tk
from getpass import getpass

class GraphicalLogin:
    def __init__(self, master):
        self.master = master
        self.master.geometry("300x100")
        self.master.title("Login")
        self.master.config(bg="purple")

        self.username_label = tk.Label(master, text="Usuário:", bg="purple", fg="white")
        self.username_label.place(relx=0.05, rely=0.3)

        self.username_entry = tk.Entry(master, width=20, bd=2, bg="white")
        self.username_entry.place(relx=0.3, rely=0.3)

        self.password_label = tk.Label(master, text="Senha:", bg="purple", fg="white")
        self.password_label.place(relx=0.05, rely=0.5)

        self.password_entry = tk.Entry(master, width=20, bd=2, bg="white", show="*")
        self.password_entry.place(relx=0.3, rely=0.5)

        self.login_button = tk.Button(master, text="Login", command=self.validate_credentials)
        self.login_button.place(relx=0.4, rely=0.7)

    def validate_credentials(self):
        username = self.username_entry.get()
        password = getpass("Enter password: ")

        if username == "your_username" and password == "your_password":
            print("Login successful")
        else:
            print("Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    login_system = GraphicalLogin(root)
    root.mainloop()
