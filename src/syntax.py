import re
import keyword
import builtins
import config as cfg

class PythonHighlighter:
    def __init__(self, text_widget):
        self.txt = text_widget
        self.setup_tags()

    def setup_tags(self):
        self.txt.tag_configure("keyword", foreground=cfg.COLOR_KEYWORD)
        self.txt.tag_configure("builtin", foreground=cfg.COLOR_BUILTIN)
        self.txt.tag_configure("string", foreground=cfg.COLOR_STRING)
        self.txt.tag_configure("comment", foreground=cfg.COLOR_COMMENT)
        self.txt.tag_configure("number", foreground=cfg.COLOR_NUMBER)

    def highlight_line(self, line_num):
        start_idx = f"{line_num}.0"
        end_idx = f"{line_num}.end"

        line_text = self.txt.get(start_idx, end_idx)

        for tag in ["keyword", "builtin", "string", "comment", "number"]:
            self.txt.tag_remove(tag, start_idx, end_idx)

        for match in re.finditer(r'\b\d+\b', line_text):
            self.apply_tag("number", line_num, match.start(), match.end())

        for match in re.finditer(r'\b\w+\b', line_text):
            word = match.group()
            if keyword.iskeyword(word):
                self.apply_tag("keyword", line_num, match.start(), match.end())
            elif word in dir(builtins):
                self.apply_tag("builtin", line_num, match.start(), match.end())

        for match in re.finditer(r'(".*?"|\'.*?\')', line_text):
            self.apply_tag("string", line_num, match.start(), match.end())

        comment_match = re.search(r'#.*$', line_text)
        if comment_match:
            self.apply_tag("comment", line_num, comment_match.start(), comment_match.end())

    def highlight_all(self):
        num_lines = int(self.txt.index("end-1c").split(".")[0])
        for line_num in range(1, num_lines + 1):
            self.highlight_line(line_num)

    def apply_tag(self, tag_name, line_num, start_char, end_char):
        start = f"{line_num}.{start_char}"
        end = f"{line_num}.{end_char}"
        self.txt.tag_add(tag_name, start, end)
