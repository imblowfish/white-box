import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import codecs
from math import fabs
from .base_frame import BaseFrame

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
		
class IDDependenciesFrame(BaseFrame):
	def init_widgets(self):
		self.dep_tree = DependencyTree(self, bg="white")
	def bind_commands(self):
		self.bind("<Configure>", self.resize)
	def resize(self, event):
		wscale = float(event.width)/float(self.dep_tree["width"])
		hscale = float(event.height)/float(self.dep_tree["height"])
		self.dep_tree.configure(width=event.width, height=event.height)
		self.dep_tree.scale("all", 0, 0, wscale, hscale)
	def show(self, record, id_table):
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

class MentionFrame(BaseFrame):
	def init_widgets(self):
		pass
	def show(self, file_path, mentions):
		try:
			file = codecs.open(file_path, "r", "utf_8_sig")
		except:
			messagebox.showerror("Open file error", f"Can't open file {file_path}")
			return False
		line_num = 0
		for line in file:
			if line_num in mentions:
				text = tk.Text(self,height=1)
				text.insert(tk.END, line)
				text.pack()
			line_num += 1
			print(line_num)
		file.close()
		return True
		  	
class MentionsListFrame(BaseFrame):
	def show(self, record, mentions):
		for file_path in mentions:
			frame = MentionFrame(self)
			if not frame.show(file_path, mentions[file_path]):
				messagebox.showerror("MentionsListFrame Error", "Can't show mentions")
				return

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

class MembersFrame(BaseFrame):
	def init_widgets(self):
		self.canvas = InfoCanvas(self, bg="white")
	def bind_commands(self):
		self.bind("<Configure>", self.resize)
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

class IDInfoFrame(BaseFrame):
	members_frame = None
	dependency_frame = None
	mentions_frame = None
	
	def init_widgets(self):
		self.notebook = ttk.Notebook(self)
		self.notebook.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.members_frame = MembersFrame(self)
		self.dependency_frame = IDDependenciesFrame(self)
		self.mentions_frame = MentionsListFrame(self)
		self.notebook.add(self.members_frame, text="Members")
		self.notebook.add(self.dependency_frame, text="Dependencies")
		self.notebook.add(self.mentions_frame, text="Mentions")
	def show(self, record, id_table, mentions):
		self.members_frame.show(record, id_table)
		self.dependency_frame.show(record, id_table)
		self.mentions_frame.show(record, mentions)