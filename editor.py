import tkinter as tk
import config as cfg
from syntax import PythonHighlighter

class CodeEditor:
    def __init__(self, root, app_callback=None):
        self.root = root
        self.app_callback = app_callback 
        self.mode = "NORMAL" 
        self.visual_start_idx = None 
        self.current_font_size = cfg.FONT_SIZE

        self.main_frame = tk.Frame(self.root, bg=cfg.BG_MAIN)
        self.main_frame.pack(expand=True, fill="both")

        self.line_canvas = tk.Canvas(self.main_frame, width=40, bg=cfg.BG_LINE_NUM, bd=0, highlightthickness=0)
        self.line_canvas.pack(side="left", fill="y")

        self.text_area = tk.Text(
            self.main_frame, 
            wrap="none", 
            font=(cfg.FONT_FAMILY, self.current_font_size), 
            bg=cfg.BG_MAIN, 
            fg=cfg.FG_MAIN, 
            insertbackground="white",
            bd=0,
            highlightthickness=0
        )
        self.text_area.pack(side="left", expand=True, fill="both")
        self.text_area.focus_set()
        self.text_area.configure(insertwidth=4)

        self.highlighter = PythonHighlighter(self.text_area)

        self.text_area.bind("<KeyPress>", self.handle_keypress)
        self.text_area.bind("<KeyRelease>", self.handle_keyrelease)
        self.text_area.bind("<Escape>", self.go_to_normal_mode)

        self.text_area.bind("<KeyRelease>", self.on_action_update, add="+")
        self.text_area.bind("<Button-1>", self.on_action_update)
        self.text_area.bind("<MouseWheel>", self.on_action_update)

        self.root.bind("<Control-equal>", self.zoom_in)
        self.root.bind("<Control-plus>", self.zoom_in)
        self.root.bind("<Control-minus>", self.zoom_out)

        self.update_title_mode()
        self.redraw_line_numbers()

    def redraw_line_numbers(self):
        self.line_canvas.delete("all")

        i = self.text_area.index("@0,0")
        while True:
            dline = self.text_area.dlineinfo(i)
            if not dline:
                break
            y = dline[1]
            line_num = i.split(".")[0]

            self.line_canvas.create_text(
                35, y, 
                anchor="ne", 
                text=line_num, 
                fill=cfg.FG_LINE_NUM, 
                font=(cfg.FONT_FAMILY, self.current_font_size)
            )
            i = self.text_area.index(f"{i}+1line")

    def on_action_update(self, event=None):
        self.redraw_line_numbers()
        if self.app_callback and hasattr(self.app_callback, "update_status_bar"):
            self.app_callback.update_status_bar()

    def zoom_in(self, event=None):
        if self.current_font_size < 72:
            self.current_font_size += 2
            self.text_area.configure(font=(cfg.FONT_FAMILY, self.current_font_size))
            self.redraw_line_numbers()
        return "break"

    def zoom_out(self, event=None):
        if self.current_font_size > 6:
            self.current_font_size -= 2
            self.text_area.configure(font=(cfg.FONT_FAMILY, self.current_font_size))
            self.redraw_line_numbers()
        return "break"

    def update_title_mode(self):
        title = self.root.title().split(" [")[0]
        self.root.title(f"{title} [{self.mode} MODE]")

    def go_to_normal_mode(self, event=None):
        self.mode = "NORMAL"
        self.visual_start_idx = None
        self.text_area.tag_remove("sel", "1.0", tk.END) 
        self.text_area.configure(insertbackground="white") 
        self.update_title_mode()
        self.on_action_update()
        return "break" 

    def update_visual_selection(self):
        if self.visual_start_idx:
            self.text_area.tag_remove("sel", "1.0", tk.END)
            if self.text_area.compare(self.visual_start_idx, "<=", "insert"):
                self.text_area.tag_add("sel", self.visual_start_idx, "insert")
            else:
                self.text_area.tag_add("sel", "insert", self.visual_start_idx)

    def handle_keypress(self, event):
        if self.mode == "INSERT":
            if event.keysym == "Return":
                curr_line_num = self.text_area.index("insert").split(".")[0]
                line_text = self.text_area.get(f"{curr_line_num}.0", "insert")

                leading_spaces = len(line_text) - len(line_text.lstrip(' '))
                indent = " " * leading_spaces

                if line_text.strip().endswith(":"):
                    indent += "    "

                self.text_area.insert("insert", "\n" + indent)
                self.highlighter.highlight_line(curr_line_num)
                self.root.after(10, self.highlighter.highlight_all)
                self.on_action_update()
                return "break"
            return

        key = event.char
        if event.keysym == "Escape":
            return self.go_to_normal_mode()

        if key in ["h", "l", "j", "k"]:
            if key == "h": 
                self.text_area.mark_set("insert", "insert - 1 chars")
            elif key == "l": 
                self.text_area.mark_set("insert", "insert + 1 chars")
            elif key == "j": 
                self.text_area.mark_set("insert", "insert + 1 lines")
            elif key == "k": 
                self.text_area.mark_set("insert", "insert - 1 lines")

            self.text_area.see("insert")

            if self.mode == "VISUAL":
                self.update_visual_selection()
            self.on_action_update()
            return "break"

        if self.mode == "VISUAL":
            if key == "c": 
                try:
                    selected_text = self.text_area.get("sel.first", "sel.last")
                    self.root.clipboard_clear()
                    self.root.clipboard_append(selected_text)
                except tk.TclError:
                    pass
                self.go_to_normal_mode()
                return "break"
            return "break"

        if self.mode == "NORMAL":
            if key == "i":
                self.mode = "INSERT"
                self.text_area.configure(insertbackground="green") 
                self.update_title_mode()
                self.on_action_update()
                return "break"

            elif key == "v": 
                self.mode = "VISUAL"
                self.visual_start_idx = self.text_area.index("insert") 
                self.update_visual_selection()
                self.update_title_mode()
                self.on_action_update()
                return "break"

            elif key == "p": 
                try:
                    text_to_paste = self.root.clipboard_get()
                    self.text_area.insert("insert", text_to_paste)
                    self.highlighter.highlight_all()
                except tk.TclError:
                    pass
                self.on_action_update()
                return "break"

            elif key == ":":
                if self.app_callback and hasattr(self.app_callback, "focus_command_line"):
                    self.app_callback.focus_command_line()
                return "break"

        if event.keysym not in ["Up", "Down", "Left", "Right", "BackSpace", "Delete"]:
            return "break"

    def handle_keyrelease(self, event):
        if self.mode == "INSERT":
            current_line = self.text_area.index("insert").split(".")[0]
            self.highlighter.highlight_line(current_line)

    def get_text(self):
        return self.text_area.get("1.0", tk.END)
