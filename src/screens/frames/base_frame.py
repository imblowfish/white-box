import tkinter as tk

class BaseFrame(tk.Frame):
	"""
		Базовый класс для всех фреймов
	"""
	def __init__(self, master, x=0, y=0, width=1, height=1):
		# вызываем конструктор базового класса
		tk.Frame.__init__(self, master)
		# размещаем фрейм по заданным координатам
		self.place(relx=x, rely=y, relwidth=width, relheight=height)
		# инициализируем виджеты
		self.init_widgets()
		# привязываем команды
		self.bind_commands()
	def init_widgets(self):
		"""
			Инициализация виджетов, реализована в наследниках
		"""
		pass
	def bind_commands(self):
		"""
			Привязка команд, реализована в наследниках
		"""
		pass
	def show(self, *args):
		"""
			Отображение чего-либо на виджетах фрэйма, реализована в наследниках
		"""
		pass