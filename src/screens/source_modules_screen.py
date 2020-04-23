class SourceModule:
	name = None
	blocks = None
	def __init__(self, name):
		self.name = name
		self.blocks = []
	def add_block(self, text):
		self.blocks.append(text)

# в принципе пофиг, все равно будут создаваться в новом окне

class SourceModulesScreen:
	modules = None
	def __init__(self):
		self.modules = []
	def add_in_module(self, text):
		pass
		# new_mode = True
		# if new_mode:
			# self.modules.append(SourceModule("new_module"))
			# self.modules[-1].add_block(text)
		# else:
			# поиск по модулям и добавление в существующий
		# print(modules)