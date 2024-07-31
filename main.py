import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, font , colorchooser

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor++")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, wrap='word')
        self.text_area.pack(expand=1, fill='both')

        self.font_family = "Arial"
        self.font_size = 12
        self.update_font()

        self.create_menu()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File ", menu=file_menu)
        file_menu.add_command(label="New             (Ctrl+N)", command=self.new_file)
        file_menu.add_command(label="Open            (Cntrl O)", command=self.open_file)
        file_menu.add_command(label="Save            (Cntrl S)", command=self.save_file)
        file_menu.add_command(label="Save As         (Control-Shift-S)", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit            (Cntrl Q)", command=self.exit_editor)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Cut            (Cntrl X)", command=self.cut_text)
        edit_menu.add_command(label="Copy           (Cntrl C)", command=self.copy_text)
        edit_menu.add_command(label="Paste          (Cntrl V)", command=self.paste_text)
        edit_menu.add_command(label="Find           (Cntrl F)", command=self.find_text)
        edit_menu.add_command(label="Replace        (Cntrl R)", command=self.replace_text)
        edit_menu.add_command(label="Highlight      (Cntrl H)", command=self.highlight_text)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In        (Cntrl +)", command=self.zoom_in)
        view_menu.add_command(label="Zoom Out       (Cntrl Minus)", command=self.zoom_out)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font", command=self.choose_font)
        format_menu.add_command(label="Size", command=self.choose_size)

        about_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="About", menu=about_menu)
        about_menu.add_command(label="About Developer", command=self.show_about)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
            self.current_file = file_path
            self.root.title(f"Text Editor ++ - {file_path}")

    def bind_shortcuts(self):
        self.root.bind_all('<Control-n>', lambda event: self.new_file())
        self.root.bind_all('<Control-o>', lambda event: self.open_file())
        self.root.bind_all('<Control-s>', lambda event: self.save_file())
        self.root.bind_all('<Control-Shift-S>', lambda event: self.save_as_file())
        self.root.bind_all('<Control-q>', lambda event: self.exit_editor())
        self.root.bind_all('<Control-x>', lambda event: self.cut_text())
        self.root.bind_all('<Control-c>', lambda event: self.copy_text())
        self.root.bind_all('<Control-v>', lambda event: self.paste_text())
        self.root.bind_all('<Control-f>', lambda event: self.find_text())
        self.root.bind_all('<Control-r>', lambda event: self.replace_text())
        self.root.bind_all('<Control-h>', lambda event: self.highlight_text())
        self.root.bind_all('<Control-+>', lambda event: self.zoom_in())
        self.root.bind_all('<Control-minus>', lambda event: self.zoom_out())


    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.root.title("Text Editor ++")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            messagebox.showinfo("Save", "File Saved Successfully")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                content = self.text_area.get(1.0, tk.END)
                file.write(content)
            self.current_file = file_path
            self.root.title(f"Text Editor ++ - {file_path}")
            messagebox.showinfo("Save As", "File Saved Successfully")

    def exit_editor(self):
        self.root.quit()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find")
        find_dialog.geometry("300x100")

        tk.Label(find_dialog, text="Find:").grid(row=0, column=0, padx=10, pady=10)
        find_entry = tk.Entry(find_dialog, width=20)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        def find():
            word = find_entry.get()
            self.text_area.tag_remove('found', '1.0', tk.END)
            if word:
                start_pos = '1.0'
                while True:
                    start_pos = self.text_area.search(word, start_pos, stopindex=tk.END)
                    if not start_pos:
                        break
                    end_pos = f"{start_pos}+{len(word)}c"
                    self.text_area.tag_add('found', start_pos, end_pos)
                    start_pos = end_pos
                self.text_area.tag_config('found', foreground='red')

        tk.Button(find_dialog, text="Find", command=find).grid(row=1, column=0, columnspan=2, pady=10)

    def replace_text(self):
        replace_dialog = tk.Toplevel(self.root)
        replace_dialog.title("Replace")
        replace_dialog.geometry("300x150")

        tk.Label(replace_dialog, text="Find:").grid(row=0, column=0, padx=10, pady=10)
        find_entry = tk.Entry(replace_dialog, width=20)
        find_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(replace_dialog, text="Replace:").grid(row=1, column=0, padx=10, pady=10)
        replace_entry = tk.Entry(replace_dialog, width=20)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        def replace():
            word = find_entry.get()
            replace_word = replace_entry.get()
            content = self.text_area.get('1.0', tk.END)
            new_content = content.replace(word, replace_word)
            self.text_area.delete('1.0', tk.END)
            self.text_area.insert('1.0', new_content)

        tk.Button(replace_dialog, text="Replace", command=replace).grid(row=2, column=0, columnspan=2, pady=10)

    def zoom_in(self):
        self.font_size += 2
        self.update_font()

    def zoom_out(self):
        if self.font_size > 2:
            self.font_size -= 2
            self.update_font()

    def highlight_text(self):
        color = colorchooser.askcolor()[1]
        if color:
            try:
                start_index = self.text_area.index(tk.SEL_FIRST)
                end_index = self.text_area.index(tk.SEL_LAST)
                self.text_area.tag_add("highlight", start_index, end_index)
                self.text_area.tag_config("highlight", background=color)
            except tk.TclError:
                messagebox.showerror("Error", "No text selected")



    def choose_font(self):
        fonts = list(font.families())
        font_dialog = tk.Toplevel(self.root)
        font_dialog.title("Choose Font")
        font_dialog.geometry("300x250")

        tk.Label(font_dialog, text="Font:").pack(pady=10)
        font_listbox = tk.Listbox(font_dialog)
        font_listbox.pack(expand=1, fill='both')
        for f in fonts:
            font_listbox.insert(tk.END, f)

        def set_font():
            self.font_family = font_listbox.get(tk.ACTIVE)
            self.update_font()
            font_dialog.destroy()

        tk.Button(font_dialog, text="Select", command=set_font).pack(pady=10)

    def choose_size(self):
        size_dialog = tk.Toplevel(self.root)
        size_dialog.title("Choose Size")
        size_dialog.geometry("300x100")

        tk.Label(size_dialog, text="Size:").pack(pady=10)
        size_entry = tk.Entry(size_dialog)
        size_entry.pack(pady=10)
        size_entry.insert(0, str(self.font_size))

        def set_size():
            self.font_size = int(size_entry.get())
            self.update_font()
            size_dialog.destroy()

        tk.Button(size_dialog, text="Select", command=set_size).pack(pady=10)

    def update_font(self):
        new_font = (self.font_family, self.font_size)
        self.text_area.config(font=new_font)

    def show_about(self):
        messagebox.showinfo("About Developer", "This  Text Editor was developed by [PRAFUL SINGH NEGI].")

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
