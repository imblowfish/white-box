import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs

from .project_tree import ProjectTree

# отображение иерархии проекта
class HierarchyFrame(tk.Frame):
	tree_widget = None # виджет treeview для отображения иерархии
	
	#-------------------------------------------------------
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.init_widgets()
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
	#----------------------
	def init_widgets(self): # инициализация виджетов
		style = ttk.Style()
		style.configure("Treeview.Heading", font=(None, 7), align=tk.CENTER)
		# создание treeview
		self.tree_widget = ttk.Treeview(self, style="Treeview.Heading")
		# даем ему название
		self.tree_widget.heading("#0", text="Project hierarchy")
		# размещение
		self.tree_widget.place(relx=0, rely=0, relwidth=1, relheight=1)
	#---------------
	def clear(self): # очистка treeview
		if not self.tree_widget:
			return
		for node in self.tree_widget.get_children():
			self.tree_widget.delete(node)
	#-------------------------
	def show(self, hierarchy): # отображение иерархии проекта
		# очищаем treeview
		self.clear()
		# создаем дерево на основе кортежа hierarchy
		tree = ProjectTree()
		tree.create(hierarchy)
		# заносим каждый узел в treeview
		self.add_nodes(tree.root_elements)
	#-------------------------------------
	def add_nodes(self, nodes, parent=""): # добавление нодов в treeview 
		if not nodes:
			return
		for node in nodes:
			next_parent = self.tree_widget.insert(parent, "end", text=node.name, open=True)
			if not node.child_elements:
				continue
			self.add_nodes(node.child_elements, next_parent)
#---HierarchyFrame---


from .color.color_scheme import file_content_color_scheme as color_scheme
# отображение текста файла
class FileContentFrame(tk.Frame):
	text = None # виджет отображения текста
	file_path = None # путь до файла
	
	def __init__(self, master, file_path, command, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.file_path = file_path
		self.init_widgets()
		self.init_tags(command)
	
	def init_widgets(self):
		self.text = tk.Text(self)
		self.text.insert(tk.END, self.file_path) 
		self.text.place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def init_tags(self, command):
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			self.text.tag_bind(key, "<Double-Button-1>", lambda e: command(e, key))
	
	def show_content(self):
		try:
			file = codecs.open(self.file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {self.file_path}")
			return False
		self.text.delete(1.0, tk.END)
		for line in file:
			# отображение содержимого файла с подсветкой синтаксиса
			self.text.insert(tk.END, line)
		return True
		
# отображение открываемых пользователем файлов
class OpenFilesFrame(tk.Frame):
	notebook = None
	
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.init_widgets()
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		
	def init_widgets(self):
		self.notebook = ttk.Notebook(self)
		self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1)
		
	# добавление нового файла в notebook
	def open_file(self, file_name, file_path, command):
		frame = FileContentFrame(self.notebook, file_path, command)
		if not frame.show_content():
			return
		self.notebook.add(frame, text=file_name)

# отображение информации о файле
class FileInfoFrame(tk.Frame):
	info_tree = None # дерево информации о файле
	
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.init_widgets()
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		
	def init_widgets(self):
		style = ttk.Style()
		style.configure("Treeview.Heading", font=(None, 7), align=tk.CENTER)
		self.info_tree = ttk.Treeview(self, style="Treeview.Heading")
		self.info_tree.heading("#0", text="File info")
		self.info_tree.place(relx=0, rely=0, relwidth=1, relheight=1)
			


		

	
		