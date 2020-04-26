import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs

from .project_tree import ProjectTree
# ВСЕ, ЧТО ОТНОСИТСЯ К ФРЕЙМУ ИЕРАРХИИ
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
		# отображение графа зависимости файлов проекта	
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

# ВСЕ, ЧТО ОТНОСИТСЯ К ФРЕЙМУ ОТОБРАЖЕНИЯ СОДЕРЖИМОГО ФАЙЛА
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
		self.text = tk.Text(self, wrap=tk.NONE)
		self.text.insert(tk.END, self.file_path) 
		self.text.place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def init_tags(self, command):
		for key in color_scheme:
			self.text.tag_config(key, foreground=color_scheme[key])
			self.text.tag_bind(key, "<Button-1>", lambda e: command(e, key))
	
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
class FilesFrame(tk.Frame):
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
		self.notebook.select(frame)

# ВСЕ, ЧТО ОТНОСИТСЯ К ФРЕЙМУ ОТОБРАЖЕНИЯ ЧЛЕНОВ ФАЙЛА
# отображение информации о файле
class FileInfoFrame(tk.Frame):
	info_tree = None # дерево информации о файле
	kinds = {
		"Includes": "file", 
		"Included by": "file", 
		"Variables": "variable", 
		"Enums": "enum", 
		"Functions": "function", 
		"Classes": "class"
	}
	includes = None
	included_by = None
	vars = None
	classes = None
	funcs = None
	enums = None
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.init_widgets()
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		
	def clear(self):
		if not self.info_tree:
			return
		for node in self.info_tree.get_children():
			self.info_tree.delete(node)
		
	def init_widgets(self):
		style = ttk.Style()
		style.configure("Treeview.Heading", font=(None, 7), align=tk.CENTER)
		self.info_tree = ttk.Treeview(self, style="Treeview.Heading")
		self.info_tree.heading("#0", text="File info")
		self.info_tree.place(relx=0, rely=0, relwidth=1, relheight=1)
	
	def init_nodes(self):
		self.includes = self.info_tree.insert("", "end", text="Includes", open=True)
		self.included_by = self.info_tree.insert("", "end", text="Included by", open=True)
		self.vars = self.info_tree.insert("", "end", text="Variables", open=True)
		self.enums = self.info_tree.insert("", "end", text="Enums", open=True)
		self.funcs = self.info_tree.insert("", "end", text="Functions", open=True)
		self.classes = self.info_tree.insert("", "end", text="Classes", open=True)
		
	def get_item_info(self, x, y):
		item = self.info_tree.identify("item", x, y)
		name = self.info_tree.item(item, "text")
		parent = self.info_tree.item(self.info_tree.parent(item), "text")
		if len(parent) == 0:
			return None
		return(name, self.kinds[parent])
	
	def show(self, record, id_table):
		self.clear()
		self.init_nodes()
		self.add_parents(record.parents_id, id_table)
		self.add_members(record.members_id, id_table)
		# где-то здесь отображение графа зависимостей файла до корня
	
	def add_parents(self, parents_id, id_table):
		if not parents_id:
			return
		for id in parents_id:
			parent = id_table.get_record_by_id(id)
			# родителями файла могут быть только другие файлы
			self.info_tree.insert(self.includes, "end", text=parent.name, open=True)
		
	def add_members(self, members_id, id_table):
		if not members_id:
			return
		for id in members_id:
			member = id_table.get_record_by_id(id)
			if member.kind == "file":
				self.info_tree.insert(self.included_by, "end", text=member.name, open=True)
			elif member.kind == "variable":
				self.info_tree.insert(self.vars, "end", text=member.name, open=True)
			elif member.kind == "function":
				self.info_tree.insert(self.funcs, "end", text=member.name, open=True)
			elif member.kind == "enum":
				self.info_tree.insert(self.enums, "end", text=member.name, open=True)
			elif member.kind == "class":
				self.info_tree.insert(self.classes, "end", text=member.name, open=True)
				

# ВСЕ, ЧТО ОТНОСИТСЯ К ФРЕЙМУ ОТОБРАЖЕНИЯ ИНФОРМАЦИИ ОБ ИДЕНТИФИКАТОРЕ
# отображать граф зависимостей и treeview информации о классе

from math import fabs

class InfoCanvas(tk.Canvas):
	padding = 5
	up_limit = None
	down_limit = None
	def __init__(self, master, **kwargs):
		tk.Canvas.__init__(self, master, **kwargs)
		self.up_limit = 0
		self.down_limit = 0
		self.addtag_all("all")
		self.bind("<MouseWheel>", self.scroll)
		self.pack()
		# self.tag_bind("all", "<Enter>", self.on_enter)
	# def on_enter(self, event):
		# item = event.widget.find_closest(event.x, event.y)
		# self.itemconfig(item, fill="yellow")
	def scroll(self, event):
		bbox = self.bbox("all")
		if event.delta < 0 and bbox[3] + event.delta < self.down_limit:
			return
		elif event.delta > 0 and bbox[1] + event.delta > self.up_limit:
			return
		self.move("all", 0, event.delta)
	def draw_header(self, record):
		width = int(self["width"])
		height = int(self["height"])
		name = self.create_text(width/2, height/20, text=record.kind+' '+record.name, )
		self.create_rectangle(self.padding, self.padding, width - self.padding, height/10)
		self.up_limit = int(self["height"])/10
		self.down_limit = int(self["height"]) - int(self["height"])/10
	def show_member(self, member):
		bbox = self.bbox("all")
		text = self.create_text(self.padding + bbox[0], bbox[3], text=str(member), anchor="nw")
		bbox = self.bbox(text)
		if bbox[0] < 0:
			self.move(text, fabs(bbox[0]), 0)
		
class IDInfoFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
		self.bind("<Configure>", self.resize)
	def init_widgets(self):
		self.canvas = InfoCanvas(self, bg="white")
	def resize(self, event):
		wscale = float(event.width)/float(self.canvas["width"])
		hscale = float(event.height)/float(self.canvas["height"])
		self.canvas.configure(width=event.width, height=event.height)
		self.canvas.scale("all", 0, 0, wscale, hscale)
	def show(self, record, id_table):
		self.canvas.draw_header(record)
		if not record.members_id:
			return
		for id in record.members_id:
			member = id_table.get_record_by_id(id, copy=True)
			self.canvas.show_member(member)

# ВСЕ,ЧТО ОТНОСИТСЯ К ФРЕЙМУ ОТОБРАЖЕНИЯ ЗАВИСИМОСТЕЙ ОБЪЕКТА

class DependencyGraph(tk.Canvas):
	edges = None
	def __init__(self, master, **kwargs):
		tk.Canvas.__init__(self, master, **kwargs)
		self.addtag_all("all")
		self.pack()
		self.edges = []

class DependencyFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
		self.bind("<Configure>", self.resize)
	def init_widgets(self):
		self.graph = DependencyGraph(self, bg="white")
	def resize(self, event):
		wscale = float(event.width)/float(self.graph["width"])
		hscale = float(event.height)/float(self.graph["height"])
		self.graph.configure(width=event.width, height=event.height)
		self.graph.scale("all", 0, 0, wscale, hscale)
	def show(self, record, id_table):
		print("Show dependency")

	
		