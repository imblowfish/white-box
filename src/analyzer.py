from parsing import (
	doxygen_worker_main as dw,
	source_worker_main as sw
)

class AnalysisManager:
	def __init__(self):
		print("AnalysisManager is created")
	def parse_project(self, project_directory):
		print(f"Start parse project {project_directory}")