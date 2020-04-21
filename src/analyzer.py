from parsing import (
	doxygen_worker_main as dox_w,
	source_worker_main as s_w,
	
)

class Analyzer:
	def __init__(self):
		pass
	def parse_project(self, project_directory):
		print(f"Start parse project {project_directory}")