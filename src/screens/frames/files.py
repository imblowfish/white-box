import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs
from .base_frame import BaseFrame
from .color.color_scheme import file_content_color_scheme as color_scheme
from .tokenizer.tokenizer import Tokenizer

# отображение текста файла
class FileContentFrame(BaseFrame):
	text = None # виджет отображения текста
	file_path = None # путь до файла
	file_name = None
	def __init__(self, master, file_name, file_path, command, x=0, y=0, width=1, height=1):
		self.file_name = file_name
		self.file_path = file_path
		super().__init__(master, x, y, width, height)
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			def make_lambda(k):
				return lambda e: command(e, k)
			self.text.tag_bind(key, "<Double-Button-1>", make_lambda(key))
		self.text.bind("<Button-3>", lambda e: command(e, "right_b"))
			
	def init_widgets(self):
		self.text = tk.Text(self, wrap=tk.NONE, font=(None, 8))
		self.text.insert(tk.END, self.file_path) 
		self.text.place(relx=0, rely=0, relwidth=1, relheight=1)
	def bind_commands(self):
		pass
	def show(self, id_table):
		try:
			file = codecs.open(self.file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
			return False
		self.text.delete(1.0, tk.END)
		self.highlight(file, id_table)
		file.close()
		return True
	def highlight(self, file, id_table):
		tokenizer = Tokenizer()
		t_value = ""
		t_type = None
		for line in file:
			i = 0
			while i < len(line):
				t_value += line[i]
				now_type = tokenizer.get_token_type(t_value)
				if not now_type or i+1 == len(line):
					if t_type:
						if i+1 < len(line):
							i -= 1
							t_value = t_value[:-1]
						t_type = self.specify(t_value, t_type, tokenizer, id_table)
						self.text.insert(tk.END, t_value, t_type)
					else:
						self.text.insert(tk.END, t_value, "default")
					t_value = ""
				t_type = now_type
				i += 1
	def specify(self, value, type, tokenizer, id_table):
		if tokenizer.is_keyword(value):
			return "keyword"
		if type == "id":
			if id_table.has_record_in_file(self.file_name, value):
				return "id"
			elif id_table.has_record(value):
				return "another_file_id"
			return "unknown_id"	
		return type
	def get_word_under(self, event, tag):
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return self.text.get(start, end)
		return None
	def get_selected(self):
		try:
			return self.text.selection_get()
		except:
			return None
		
# отображение открываемых пользователем файлов
class FilesFrame(BaseFrame):
	notebook = None
	# now_frame = None
	frames = None
	def init_widgets(self):
		self.notebook = ttk.Notebook(self)
		self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.frames = []
	# добавление нового файла в notebook
	def open_file(self, file_name, file_path, command, id_table):
		frame = FileContentFrame(self.notebook, file_name, file_path, command)
		if not frame.show(id_table):
			return
		self.notebook.add(frame, text=file_name)
		self.notebook.select(frame)
		# print(self.notebook.index("current"))
		# self.now_frame = frame
		self.frames.append(frame)
	def get_current(self):
		return self.frames[ self.notebook.index("current") ]