import tkinter as tk

from .frames import (
	HierarchyFrame,
	FilesFrame,
	FileInfoFrame,
	IDInfoFrame,
	DependencyFrame,
	MentionsListFrame,
	DependencyFrame2
)

# класс главного окна
class MainWindow:
	master = None # корень tkinter
	menu_bar = None # меню окна
	files_frame = None # просмотр файлов
	hierarchy_frame = None # иерархия проекта
	file_info_frame = None # информация о файле
	
	#------------------
	def __init__(self):
		self.init_master(800, 600)
		self.init_frames()
	#------------------------------------
	def init_master(self, width, height): # инициализация корня tkinter
		self.master = tk.Tk()
		self.master.title("WhiteBox")
		self.master.geometry(str(width)+"x"+str(height))
	#---------------------
	def init_frames(self): # инициализация фреймов
		# создаем фрейм иерархии проекта
		self.hierarchy_frame = HierarchyFrame(self.master, width=0.2, height=0.5)	
		# фрейм отображения зависимостей файлов между собой
		self.file_dependency_frame = DependencyFrame2(self.master, y=0.5, width=0.2, height=0.5)
		# содежимого файлов
		self.files_frame = FilesFrame(self.master, x=0.2, width=0.6)
		# информации о файле
		self.file_info_frame = FileInfoFrame(self.master, x=0.8, width=0.2)
	#---------------
	def start(self): # начало работы окна
		self.master.mainloop()
	#----------------------
	def show_id_info(self, record, id_table):
		pass
		# print("Show id info")
		# win = tk.Toplevel()
		# win.geometry("500x500")
		# win.title("ID info")
		# id_info_frame = IDInfoFrame(win)
		# id_info_frame.show(record, id_table)
		
		# win = tk.Toplevel()
		# win.geometry("500x500")
		# win.title("Dependencies")
		# dep_frame = DependencyFrame(win)
		# dep_frame.show(record, id_table)
		
		
		# отправляю запись и файлы проекта
		# mentions.show(record)
	def show_mentions(self, record, mentions):
		win = tk.Toplevel()
		win.geometry("500x500")
		win.title("Mentions")
		mentions_frame = MentionsListFrame(win)
		mentions_frame.show(record, mentions)
		
#---MainWindow---