import tkinter as tk
import tkinter.ttk as ttk
import codecs

from .tokenizer import Tokenizer

class FileViewerScreen:
	def show(self, file_path, id_table, command):
		self.root = tk.Tk()
		try:
			file = codecs.open(file_path, "r", "utf_8_sig")
		except:
			print(f"FileViewerScreen Error open file {file_path}")
			return
			
		self.text = tk.Text(self.root, font=("Courier New", 9))
		
		self.text.tag_config("default", foreground="black")
		self.text.tag_config("PREPROC", foreground="grey")
		self.text.tag_config("SYMBOL", foreground="orange")
		self.text.tag_config("STRING", foreground="orange")
		self.text.tag_config("COMMENT", foreground="grey")
		self.text.tag_config("MULTILINE COMMENT", foreground="grey")
		self.text.tag_config("FIXED_NUM", foreground="yellow")
		self.text.tag_config("FLOAT_NUM", foreground="yellow")
		self.text.tag_config("KEYWORD", foreground="blue")
		self.text.tag_config("IDENTIFIER", foreground="green")
		self.text.tag_bind("IDENTIFIER", "<Button-1>", lambda e: command(e, "IDENTIFIER"))
		self.text.tag_config("function", foreground="red")
		self.text.tag_bind("function", "<Button-1>", lambda e: command(e, "function"))
		self.text.tag_config("class", foreground="brown")
		self.text.tag_bind("class", "<Button-1>", lambda e: command(e, "class"))
		
		tokenizer = Tokenizer()
		value = ""
		token_type = None
		for line in file:
			i = 0
			while True:
				if i >= len(line):
					break
				else:
					value += line[i]
				res = tokenizer.get_token_type(value)
				if not res:
					if token_type:
						value = value[:-1]
						if tokenizer.is_keyword(value):
							token_type = "KEYWORD"
						if token_type == "IDENTIFIER":
							if id_table.get_kind_by_name(value):
								token_type = id_table.get_kind_by_name(value)
						self.text.insert(tk.END, value, token_type)
						i-=1
					else:
						self.text.insert(tk.END, value, "default")
					value = ""
				token_type = res
				i+=1
			
		self.text.pack()
		self.root.mainloop()

	
	def get_word_under_mouse(self, event, tag):
		index = self.text.index("@%s,%s" % (event.x, event.y))
		tag_indices = list(self.text.tag_ranges(tag))
		for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
			if self.text.compare(start, '<=', index) and self.text.compare(index, '<', end):
				return self.text.get(start, end)
		return None