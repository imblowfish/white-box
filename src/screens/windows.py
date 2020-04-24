import tkinter as tk

from .frames import (
	HierarchyFrame,
	OpenFilesFrame,
	FileInfoFrame
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
		self.hierarchy_frame = HierarchyFrame(self.master, width=0.2)
		# содежимого файлов
		self.files_frame = OpenFilesFrame(self.master, x=0.2, width=0.6)
		# информации о файле
		self.file_info_frame = FileInfoFrame(self.master, x=0.8, width=0.2)
	#---------------
	def start(self): # начало работы окна
		self.master.mainloop()
#---MainWindow---