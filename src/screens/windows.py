import tkinter as tk

from .frames.hierarchy import HierarchyFrame
from .frames.files import FilesFrame
from .frames.file_info import FileInfoFrame
from .frames.file_dependencies import FileDependenciesFrame
from .frames.log import LogFrame
from .frames.status_bar import StatusBarFrame
from .frames.search_id import SearchIDFrame

# класс главного окна
class MainWindow:
	master = None # корень tkinter
	menu_bar = None # меню окна
	files_frame = None # просмотр файлов
	hierarchy_frame = None # иерархия проекта
	file_info_frame = None # информация о файле

	def __init__(self):
		self.init_master(800, 600)
		self.init_frames()

	def init_master(self, width, height): # инициализация корня tkinter
		self.master = tk.Tk()
		self.master.title("WhiteBox")
		self.master.geometry(str(width)+"x"+str(height))

	def init_frames(self): # инициализация фреймов
		# создаем фрейм иерархии проекта
		self.hierarchy_frame = HierarchyFrame(self.master, width=0.2, height=0.7)	
		# фрейм отображения зависимостей файлов между собой
		self.file_dependency_frame = FileDependenciesFrame(self.master, y=0.7, width=0.2, height=0.3)
		# содежимого файлов
		self.files_frame = FilesFrame(self.master, x=0.2, width=0.6)
		# информации о файле
		self.file_info_frame = FileInfoFrame(self.master, x=0.8, width=0.2, height=0.7)
		self.log_frame = LogFrame(self.master, x=0.8, y=0.7, width=0.2, height=0.27)
		self.status_bar_frame = StatusBarFrame(self.master, x=0.8, y=0.97, width=0.2, height=0.03)

	def start(self): # начало работы окна
		self.master.mainloop()
	
	def log(self, text):
		self.log_frame.insert(text)
		
	def start_statusbar(self):
		self.status_bar_frame.start()
		
	def stop_statusbar(self):
		self.status_bar_frame.stop()
		
	def search_id(self, s_searcher, run_html):
		win = tk.Toplevel()
		win.title("ID searching")
		win.geometry("200x100")
		win.resizable(False, False)
		s_frame = SearchIDFrame(win)
		s_frame.init_searcher(s_searcher)
		s_frame.init_run_html(run_html)
		
		

#---MainWindow---