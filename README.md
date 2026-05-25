# MMT version 0.01 CodeEditor

MMT is a lighweight, modal text editor designed for developers. Currently, MMT fully supports **Python**, with plans to add **C support** in the future.

---

##  Editor Modes

MMT operates using three distinct modes:

* **NORMAL MODE** (`Esc`) — Used for navigation and executing commands.
* **INSERT MODE** (`i`) — Used for writing and editing code.
* **VISUAL MODE** (`v`) — Used for selecting and copying text.

---

##  Navigation (NORMAL MODE)

To move the cursor around your code, switch to **NORMAL MODE** and use the following keys:

* `k` — Move cursor **up**
* `j` — Move cursor **down**
* `h` — Move cursor **left**
* `l` — Move cursor **right**

---

##  Copy & Paste (VISUAL MODE)

1.  Position your cursor where you want to start copying.
2.  Press `v` to enter **VISUAL MODE**.
3.  Use `k`, `j`, `h`, `l` to expand your text selection.
4.  Press `c` to **copy** the selected text. The editor will automatically return to **NORMAL MODE**.
5.  Move to your desired location and press `p` to **paste** (Paste works only in **NORMAL MODE**).

---

##  Commands (NORMAL MODE + `:`)

To execute system commands, switch to **NORMAL MODE**, type `:` (colon), enter your command, and press `Enter`:

| `:e` | **Exit** the editor
| `:s <filename>` | **Save** the file
| `:r <filename>` | **Run** the Python file
| `:rn <newfilename>` | **Rename** the current file
