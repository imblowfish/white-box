import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
import math
from PIL import Image, ImageTk
from .base_frame import BaseFrame

class FileDependenciesFrame(BaseFrame):
	prev_x = None
	prev_y = None
	radius = 2
	
	text_color = "black"
	line_color = "#b8b6b6"
	without_childs_color = "red"
	zoom_icon_path = "./conf/zoom_icon.png"
	
	def init_widgets(self):
		self.bind("<Configure>", self.resize)
		self.canvas = tk.Canvas(self, bg="white")
		image = Image.open(self.zoom_icon_path)
		icon = ImageTk.PhotoImage(image)
		self.zoom_btn = tk.Button(self, text="Maximize", image=icon, width = 16)
		self.zoom_btn.image = icon
		self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
		self.zoom_btn.pack(fill=tk.X, side=tk.TOP)
		self.canvas.pack(fill=tk.BOTH)
		self.font = tkFont.Font(family=None, size=8, weight="bold")
		
	def bind_commands(self):
		self.bind("<Configure>", self.resize)
		self.canvas.bind("<MouseWheel>", self.scale)
		self.canvas.bind("<B1-Motion>", self.move)
		self.canvas.bind("<ButtonRelease-1>", self.reset)
	
	def resize(self, event):
		wscale = float(event.width)/float(self.canvas["width"])
		hscale = float(event.height)/float(self.canvas["height"])
		self.canvas.configure(width=event.width, height=event.height)
		self.canvas.scale("all", 0, 0, wscale, hscale)	
		
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
		
	def move(self, event):
		if self.prev_x and self.prev_y:
			delta_x = event.x - self.prev_x
			delta_y = event.y - self.prev_y
			self.canvas.move("all", delta_x, delta_y)
		self.prev_x = event.x
		self.prev_y = event.y
	
	def reset(self, event):
		self.prev_x = None
		self.prev_y = None
	
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
			x1 = center_x + (self.radius * math.sin(dt - rec_idx * alpha) * 180) / math.pi
			y1 = center_y + (self.radius * math.cos(dt - rec_idx * alpha) * 180) / math.pi
			if not record.members_id:
				text = self.canvas.create_text(x1, y1, text=record.name, font=self.font, fill=self.without_childs_color)
			else:
				has_member = False
				for id in record.members_id:
					member = id_table.get_record_by_id(id)
					if member.kind == "file":
						has_member = True
						break
				if has_member:
					text = self.canvas.create_text(x1, y1, text=record.name, font=self.font, fill=self.text_color)
				else:
					text = self.canvas.create_text(x1, y1, text=record.name, font=self.font, fill=self.without_childs_color)
			if not record.parents_id:
				continue
			for id in record.parents_id:
				parent = id_table.get_record_by_id(id)
				if parent.kind != "file":
					continue
				par_idx = files.index(parent.name)
				x2 = center_x + (self.radius * math.sin(dt - par_idx * alpha) * 180) / math.pi
				y2 = center_y + (self.radius * math.cos(dt - par_idx * alpha) * 180) / math.pi
				self.canvas.create_line(x2, y2, x1, y1, dash=(4,2), arrow=tk.LAST, fill=self.line_color, arrowshape=(10, 10, 4), smooth=True)
			self.canvas.tag_raise(text)