import tkinter as tk
from tkinter import messagebox
import hashlib
import os

# Dummy database for storing user data
# In a real application, this would be a proper database (e.g., SQLite, PostgreSQL)
users_db = {
    # Example user entry:
    # "username": {"password_hash": "...", "password_salt": "..."}
}

class GraphicalPasswordApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Graphical Password Authentication")
        self.root.geometry("600x600")

        self.password_sequence = []
        self.image_path = self.get_image_path()
        self.images = self.load_images()
        
        self.current_user = None

        self.create_main_menu()

    def get_image_path(self):
        # Dynamically get the path to the images directory
        # This makes the code portable
        script_dir = os.path.dirname(os.path.abspath(__file__))
        return os.path.join(script_dir, 'images')

    def load_images(self):
        image_list = []
        for i in range(1, 10):
            try:
                img_file = os.path.join(self.image_path, f"img{i}.png")
                img = tk.PhotoImage(file=img_file)
                image_list.append(img)
            except tk.TclError:
                messagebox.showerror("Error", f"Could not load image: {img_file}. Make sure it exists.")
                return None
        return image_list

    def hash_password(self, sequence):
        # Concatenate the image IDs into a string and hash it
        password_str = "-".join(map(str, sequence))
        return hashlib.sha256(password_str.encode()).hexdigest()

    def create_main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="Welcome!", font=("Helvetica", 24)).pack(pady=20)
        tk.Button(self.root, text="Login", command=self.create_login_ui, width=20, height=2).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.create_register_ui, width=20, height=2).pack(pady=10)

    def create_register_ui(self):
        self.clear_frame()
        tk.Label(self.root, text="New User Registration", font=("Helvetica", 18)).pack(pady=10)
        
        tk.Label(self.root, text="Enter a username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Click 3 images in your desired password sequence:").pack(pady=10)
        self.password_sequence = []
        self.create_image_grid(self.register_sequence)
        
        tk.Button(self.root, text="Confirm", command=self.confirm_registration, width=15).pack(pady=20)

    def create_login_ui(self):
        self.clear_frame()
        tk.Label(self.root, text="User Login", font=("Helvetica", 18)).pack(pady=10)

        tk.Label(self.root, text="Enter your username:").pack(pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Click your 3 password images in the correct order:").pack(pady=10)
        self.password_sequence = []
        self.create_image_grid(self.login_sequence)

        tk.Button(self.root, text="Login", command=self.confirm_login, width=15).pack(pady=20)

    def create_image_grid(self, command_handler):
        image_frame = tk.Frame(self.root)
        image_frame.pack()
        
        for i in range(9):
            btn = tk.Button(image_frame, image=self.images[i], command=lambda i=i: command_handler(i))
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    
    def register_sequence(self, image_id):
        if len(self.password_sequence) < 3:
            self.password_sequence.append(image_id)
            print(f"Registration sequence: {self.password_sequence}")
            if len(self.password_sequence) == 3:
                messagebox.showinfo("Sequence Complete", "Your password sequence has been recorded.")

    def login_sequence(self, image_id):
        self.password_sequence.append(image_id)
        print(f"Login sequence: {self.password_sequence}")
        if len(self.password_sequence) == 3:
            messagebox.showinfo("Sequence Complete", "Checking password...")
            self.confirm_login()

    def confirm_registration(self):
        username = self.username_entry.get()
        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return

        if len(self.password_sequence) != 3:
            messagebox.showerror("Error", "Please select exactly 3 images for your password.")
            return

        if username in users_db:
            messagebox.showerror("Error", "Username already exists. Please choose another.")
            return

        password_hash = self.hash_password(self.password_sequence)
        users_db[username] = {"password_hash": password_hash}
        
        messagebox.showinfo("Success", f"User '{username}' registered successfully!")
        self.create_main_menu()

    def confirm_login(self):
        username = self.username_entry.get()
        if not username or username not in users_db:
            messagebox.showerror("Error", "Invalid username.")
            return

        if len(self.password_sequence) < 3:
            messagebox.showerror("Error", "Please complete the password sequence.")
            return
            
        entered_hash = self.hash_password(self.password_sequence[:3])
        stored_hash = users_db[username]["password_hash"]

        if entered_hash == stored_hash:
            messagebox.showinfo("Success", "Login successful!")
            self.show_success_screen(username)
        else:
            messagebox.showerror("Error", "Incorrect password sequence.")
        
        self.password_sequence = []

    def show_success_screen(self, username):
        self.clear_frame()
        tk.Label(self.root, text=f"Welcome, {username}!", font=("Helvetica", 24)).pack(pady=50)
        tk.Button(self.root, text="Logout", command=self.create_main_menu, width=20, height=2).pack(pady=20)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalPasswordApp(root)
    root.mainloop()