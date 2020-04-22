import tkinter as tk
from math import *

# более красивое отображение, с именами и т.д.


class IdTableInfoScreen:
	last_x = None
	last_y = None

	def show_info(self, name, id_table):
		record = id_table.get_record_by_name(name, copy=True)
		if not record:
			print(f"Can't find record {name}")
			return
	
		self.root = tk.Tk()
		self.canvas = tk.Canvas(self.root, width=500, height=500, bg="white")
		self.show_header(record)
		
		if record.parents_id:
			for id in record.parents_id:
				self.show_record( id_table.get_record_by_id(id, copy=True) )
			
		if record.members_id:
			for id in record.members_id:
				self.show_record( id_table.get_record_by_id(id, copy=True) )
		
		self.canvas.pack()
		self.root.mainloop()
		
	def show_header(self, record):
		self.canvas.create_rectangle(5, 5, int(self.canvas["width"]), int(self.canvas["height"])/10)
		self.canvas.create_text(int(self.canvas["width"])/2, int(self.canvas["height"])/10/2, text=record.name)
		self.last_y = int(self.canvas["height"])/10
			
	def show_record(self, record):
		if not self.last_x:
			self.last_x = 5
		text = self.canvas.create_text(self.last_x, 0, text=record.name)
		x1, y1, x2, y2 = self.canvas.bbox(text)
		self.canvas.move(text, fabs(x1)+5, self.last_y+10)
		self.last_y += y2 + 10