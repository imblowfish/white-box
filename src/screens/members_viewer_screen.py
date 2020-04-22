import tkinter as tk
import tkinter.ttk as ttk

class MembersViewerScreen:
	def show(self, members, command):
		self.root = tk.Tk()
		self.members = ttk.Treeview(self.root)
		include = self.members.insert("", "end", text="Include")
		classes = self.members.insert("", "end", text="Classes")
		variables = self.members.insert("", "end", text="Variables")
		functions = self.members.insert("", "end", text="Functions")
		enums = self.members.insert("", "end", text="Enums")
		for member in members:
			if member.kind == "file":
				self.members.insert(include, "end", text=member.name)
			elif member.kind == "class":
				self.members.insert(classes, "end", text=member.name)
			elif member.kind == "function":
				self.members.insert(functions, "end", text=member.name)
			elif member.kind == "var":
				self.members.insert(variables, "end", text=member.name)
			elif member.kind == "enum":
				self.members.insert(enums, "end", text=member.name)
		self.members.bind("<Button-1>", command)
		self.members.pack()
		self.root.mainloop()