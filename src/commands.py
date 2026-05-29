import sys
import os
import subprocess
from tkinter import messagebox

class CommandHandler:
    def __init__(self, root, editor):
        self.root = root
        self.editor = editor

    def execute(self, raw_input):
        parts = raw_input.strip().split(maxsplit=1)
        if not parts:
            return

        command = parts[0]
        args = parts[1].strip("'\"") if len(parts) > 1 else ""

        if command == "e":
            self.root.quit()

        elif command == "s":
            if not args:
                messagebox.showerror("Error", "Enter the name of the file. Example: s main.py")
                return
            self.save_file(args)

        elif command == "r":
            if not args:
                messagebox.showerror("Error", "Enter a file. Example: r main.py")
                return
            self.run_file(args)
            
        elif command == "rn":
            if not args:
                messagebox.showerror("Error", "Enter the new name of the file. Example: rn new_name.py")
                return
            self.rename_file(args)
            
        else:
            print(f"Command not found: {command}")

    def save_file(self, filename):
        try:
            code = self.editor.get_text()
            with open(filename, "w", encoding="utf-8") as f:
                f.write(code)
            self.root.title(f"MMT CodeEditor - {filename}")
            print(f"File {filename} saved.")
        except Exception as e:
            messagebox.showerror("Save Error", str(e))

    def run_file(self, filename):
        if not os.path.exists(filename):
            messagebox.showerror("Error", f"File {filename} not found.")
            return

        print(f"--- Run {filename} ---")
        try:
            if sys.platform == "win32":
                subprocess.Popen(["cmd", "/c", "python", filename, "&&", "pause"])
            else:
                subprocess.Popen(["python3", filename])
        except Exception as e:
            messagebox.showerror("Run error", str(e))

    def rename_file(self, new_filename):
        app = self.editor.app_callback
        old_filename = app.filename

        if old_filename and os.path.exists(old_filename):
            try:
                os.rename(old_filename, new_filename)
                print(f"File successfully renamed from {old_filename} to {new_filename}")
            except Exception as e:
                messagebox.showerror("Rename Error", str(e))
                return
        else:
            print(f"File did not exist on disk. Name changed in IDE to {new_filename}")

        app.filename = new_filename
        self.root.title(f"MMT CodeEditor - {new_filename}")
        app.update_status_bar()
        self.editor.update_title_mode()
