import sys
import os
import tkinter as tk
from tkinter import PhotoImage
import config as cfg
from editor import CodeEditor
from commands import CommandHandler

class MainApp:
    def __init__(self):
        self.root = tk.Tk() 
        self.root.title("MMT CodeEditor")
        self.root.geometry("800x600")
        
        if sys.platform == "win32":
            import ctypes
            myappid = "mmt.codeeditor.python.v1"
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
            
            if os.path.exists("icon.ico"):
                try:
                    self.root.iconbitmap("icon.ico")
                except Exception as e:
                    print(f"Failed to load .ico icon: {e}")
        else:
            if os.path.exists("icon.png"):
                try:
                    self.icon_img = PhotoImage(file="icon.png")
                    self.root.iconphoto(False, self.icon_img)
                except Exception as e:
                    print(f"Failed to load .png icon: {e}")

        self.filename = "New File"
        self.editor = CodeEditor(self.root, app_callback=self)

        divider = tk.Frame(self.root, height=2, bg="#333333")
        divider.pack(fill="x")

        self.cmd_handler = CommandHandler(self.root, self.editor)

        self.history = []
        self.history_index = -1

        if len(sys.argv) > 1:
            self.filename = sys.argv[1]
            if os.path.exists(self.filename):
                try:
                    with open(self.filename, "r", encoding="utf-8") as f:
                        self.editor.text_area.insert("1.0", f.read())
                    self.root.title(f"MMT CodeEditor - {self.filename}")
                    self.editor.highlighter.highlight_all()
                except Exception as e:
                    print(f"Error while reading the file: {e}")
            else:
                self.root.title(f"MMT CodeEditor - {self.filename} (New file)")
           
        self.editor.update_title_mode()

        self.cmd_frame = tk.Frame(self.root, bg=cfg.BG_BOTTOM)
        self.cmd_frame.pack(fill="x")

        self.prompt_label = tk.Label(
            self.cmd_frame, 
            text="-", 
            font=(cfg.FONT_FAMILY, cfg.FONT_SIZE, "bold"), 
            bg=cfg.BG_BOTTOM, 
            fg=cfg.FG_PROMPT
        )
        self.prompt_label.pack(side="left", padx=5)

        self.cmd_input = tk.Entry(
            self.cmd_frame, 
            font=(cfg.FONT_FAMILY, cfg.FONT_SIZE), 
            bg=cfg.BG_BOTTOM, 
            fg=cfg.FG_MAIN, 
            insertbackground="white", 
            bd=0
        )
        self.cmd_input.pack(side="left", fill="x", expand=True, ipady=5)

        self.status_bar = tk.Label(
            self.root, 
            text="Ln 1, Col 0 | UTF-8", 
            font=(cfg.FONT_FAMILY, 10), 
            bg=cfg.BG_BOTTOM, 
            fg=cfg.FG_STATUS, 
            anchor="e", 
            padx=10,
            pady=3
        )
        self.status_bar.pack(side="bottom", fill="x")

        self.cmd_input.bind("<Return>", self.on_enter)
        self.cmd_input.bind("<Escape>", self.return_to_editor)
        self.cmd_input.bind("<Up>", self.history_up)
        self.cmd_input.bind("<Down>", self.history_down)

        self.update_status_bar()

    def update_status_bar(self):
        try:
            cursor_pos = self.editor.text_area.index("insert")
            line, col = cursor_pos.split(".")
            self.status_bar.configure(text=f"File: {self.filename}  |  Ln {line}, Col {col}  |  UTF-8")
        except Exception:
            pass

    def focus_command_line(self):
        self.cmd_input.focus_set()
        self.history_index = len(self.history)

    def return_to_editor(self, event=None):
        self.cmd_input.delete(0, tk.END)
        self.editor.text_area.focus_set()
        self.editor.go_to_normal_mode()

    def on_enter(self, event):
        cmd_text = self.cmd_input.get().strip()
        
        if cmd_text:
            if not self.history or self.history[-1] != cmd_text:
                self.history.append(cmd_text)
            
            parts = cmd_text.split(maxsplit=1)
            if parts[0] == "s" and len(parts) > 1:
                self.filename = parts[1].strip("'\"")
        
        self.cmd_handler.execute(cmd_text)
        self.return_to_editor()

    def history_up(self, event):
        if not self.history: return "break"
        if self.history_index > 0:
            self.history_index -= 1
            self.cmd_input.delete(0, tk.END)
            self.cmd_input.insert(0, self.history[self.history_index])
        elif self.history_index == 0:
            self.cmd_input.delete(0, tk.END)
            self.cmd_input.insert(0, self.history[0])
        return "break"

    def history_down(self, event):
        if not self.history: return "break"
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.cmd_input.delete(0, tk.END)
            self.cmd_input.insert(0, self.history[self.history_index])
        else:
            self.history_index = len(self.history)
            self.cmd_input.delete(0, tk.END)
        return "break"

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
