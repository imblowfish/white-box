import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs

from .project_tree import ProjectTree


#
import math
class DependencyFrame2(tk.Frame):
	prev_x = None
	prev_y = None
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
		self.bind("<Configure>", self.resize)
	def resize(self, event):
		wscale = float(event.width)/float(self.canvas["width"])
		hscale = float(event.height)/float(self.canvas["height"])
		self.canvas.configure(width=event.width, height=event.height)
		self.canvas.scale("all", 0, 0, wscale, hscale)
	def init_widgets(self):
		self.canvas = tk.Canvas(self, bg="white")
		self.canvas.bind("<MouseWheel>", self.scale)
		self.canvas.bind("<B1-Motion>", self.move)
		self.canvas.bind("<ButtonRelease-1>", self.reset)
		self.canvas.pack(fill=tk.BOTH)
	def reset(self, event):
		self.prev_x = None
		self.prev_y = None
		print("Release")
	def move(self, event):
		if self.prev_x and self.prev_y:
			delta_x = event.x - self.prev_x
			delta_y = event.y - self.prev_y
			self.canvas.move("all", delta_x, delta_y)
		self.prev_x = event.x
		self.prev_y = event.y
	def scale(self, event):
		wscale, hscale = 0, 0
		center_x, center_y = float(self.canvas["width"])/2, float(self.canvas["height"])/2
		if event.delta < 0:
			wscale=0.5
			hscale=0.5
		else:
			wscale=1.5
			hscale=1.5
		self.canvas.scale("all", center_x, center_y, wscale, hscale)
	def show(self, records, id_table):
		self.canvas.delete("all")
		files = []
		for record in records:
			if record.kind == "file":
				files.append(record.name)
		num_of_files = len(files)
		alpha = (2 * math.pi)/num_of_files
		dt = 3 * math.pi / 2
		center_x = float(self.canvas["width"]) / 2
		center_y = float(self.canvas["height"]) / 2
		for record in records:
			if record.kind != "file":
				continue
			rec_idx = files.index(record.name)
			x1 = center_x + (math.sin(dt - rec_idx * alpha) * 180) / math.pi
			y1 = center_y + (math.cos(dt - rec_idx * alpha) * 180) / math.pi
			self.canvas.create_text(x1, y1, text=record.name, font=(None, 6))
			if not record.parents_id:
				continue
			for id in record.parents_id:
				parent = id_table.get_record_by_id(id)
				if parent.kind != "file":
					continue
				par_idx = files.index(parent.name)
				x2 = center_x + (math.sin(dt - par_idx * alpha) * 180) / math.pi
				y2 = center_y + (math.cos(dt - par_idx * alpha) * 180) / math.pi
				self.canvas.create_line(x2, y2, x1, y1, arrow=tk.LAST)

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
		self.tree_widget.place(relx=0, rely=0, relwidth=1, relheight=1.0)
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
		file.close()
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
# добавить связи
class DependencyTree(tk.Canvas):
	levels = None
	def __init__(self, master, **kwargs):
		tk.Canvas.__init__(self, master, **kwargs)
		self.addtag_all("all")
		self.pack()
		self.levels = []
	def clear(self):
		self.levels = []
	def add_root(self, record):
		self.levels.append([(record.kind, record.name)])
	def add_next_level(self, records):
		level = []
		for record in records:
			level.append((record.kind, record.name))
		self.levels.append(level)
	def show(self):
		depth = len(self.levels)
		step_y = float(self["height"])/depth
		for i in range(depth):
			num_on_layer = len(self.levels[i])
			step_x = float(self["width"]) / (num_on_layer+1)
			for j in range(len(self.levels[i])):
				if i+1 >= depth:
					self.show_node(self.levels[i][j], i, j+1, step_x, step_y, root=True)
				else:
					self.show_node(self.levels[i][j], i, j+1, step_x, step_y)
					
	def show_node(self, node, level, num, step_x, step_y, root=False):
		x1 = num * step_x
		y1 = level * step_y + 20
		x2 = x1 + float(self["width"])/10
		y2 = y1 + float(self["height"])/10
		if root:
			self.draw_kind(node[0], x1, y1, x2, y2, "red")
		else:
			self.draw_kind(node[0], x1, y1, x2, y2)
		self.create_text(x1, y1, text=node[1])
	def draw_kind(self, kind, x1, y1, x2, y2, color="black"):
		if kind == "file":
			self.create_rectangle(x1, y1, x2, y2, outline=color)
		elif kind == "class":
			self.create_oval(x1, y1, x2, y2, outline=color)
		
class DependencyFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
		self.bind("<Configure>", self.resize)
	def init_widgets(self):
		self.dep_tree = DependencyTree(self, bg="white")
	def resize(self, event):
		wscale = float(event.width)/float(self.dep_tree["width"])
		hscale = float(event.height)/float(self.dep_tree["height"])
		self.dep_tree.configure(width=event.width, height=event.height)
		self.dep_tree.scale("all", 0, 0, wscale, hscale)
	def show(self, record, id_table):
		print("Show dependency")
		self.dep_tree.clear()
		self.show_parents(record.parents_id, id_table)
		self.dep_tree.add_root(record)
		self.dep_tree.show()
	def show_parents(self, parents_id, id_table):
		if not parents_id:
			return None
		parents = []
		for id in parents_id:
			parent = id_table.get_record_by_id(id, copy=True)
			if parent:
				parents.append(parent)
			# self.show_parents(parent.parents_id, id_table)
		self.dep_tree.add_next_level(parents)

# ВСЕ,ЧТО ОТНОСИТСЯ К УПОМИНАНИЯМ
class MentionFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.pack()
		self.init_widgets()
	def init_widgets(self):
		pass
	def show(self, file_path, mentions):
		try:
			file = codecs.open(file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {file_path}")
			return False
		label = tk.Label(self, text=file_path)
		label.pack()
		line_num = 0
		for line in file:
			if line_num in mentions:
				text = tk.Text(self,height=1)
				text.insert(tk.END, line)
				text.pack()
			line_num += 1
		file.close()
		return True
		  	
class MentionsListFrame(tk.Frame):
	def __init__(self, master, x=0, y=0, width=1, height=1):
		tk.Frame.__init__(self, master)
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		self.init_widgets()
	def init_widgets(self):
		pass
	def show(self, record, mentions):
		for file_path in mentions:
			frame = MentionFrame(self)
			if not frame.show(file_path, mentions[file_path]):
				messagebox.showerror("MentionsListFrame Error", "Can't show mentions")
				return
		