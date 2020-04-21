import tkinter as tk
import tkinter.ttk as ttk
import codecs

class SourceContentViewer:
	def __init__(self, parent, path):
		# пока что просто текст, затем добавить проверку на тип токена и подсветку
		try:
			file = codecs.open(path, "r", "utf_8_sig")
		except:
			print(f"SourceViewer error with open file {path}")
			return
		text = tk.Text(parent)
		for line in file:
			text.insert(1.0, line)
		text.pack()
		print(f"View file {path}")
	
class SourceMembersViewer:
	# self.members = None
	def __init__(self, parent, members):
		self.members = ttk.Treeview(parent)
		# self.members.column("#0", text="123")
		# self.members["columns"] = ("one", "two")
		# self.members.heading("one", text="1")
		# self.members.heading("two", text="2")
		
		# добавление переменных
		vars = self.members.insert("", "end", text="Variables")
		# добавление функций
		funcs = self.members.insert("", "end", text="Functions")
		# добавление классов
		classes = self.members.insert("", "end", text="Classes")
		for member in members:
			if member.kind == "file":
				continue
			if member.kind == "class":
				self.members.insert(classes, "end", text=member.name)
			elif member.kind == "function":
				self.members.insert(funcs, "end", text=member.name)
			elif member.kind == "var":
				self.members.insert(vars, "end", text=member.name)
				
		# self.members.heading("#0", text="1")
		# self.members.heading("one", text="2")
		# вывод всех членов файла в таблицу
		
		self.members.pack()