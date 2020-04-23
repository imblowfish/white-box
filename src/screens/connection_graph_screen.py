import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.collections import PathCollection


class ConnectionGraphScreen:
	nodes = None
	def show_project_connections(self, records, id_table):
		self.fig, ax = plt.subplots()
		self.fig.canvas.mpl_connect("button_press_event", self.onpick)
		graph = nx.DiGraph()
		for record in records:
			if record.kind != "file":
				continue
			if record.parents_id:
				for id in record.parents_id:
					parent_record = id_table.get_record_by_id(id, True)
					if parent_record.kind != "file":
						continue
					graph.add_edge(parent_record.name, record.name)		
		self.nodes = graph.nodes
		options = {
			'node_color': 'blue',
			'node_size': 400,
			"node_alpha": 0,
			'line_color': 'grey',
			'linewidths': 0,
			'width': 1.0,
			"with_labels": True,
			"font_size": 7
		}
		nx.draw_shell(graph, **options)
		plt.show()
		
	def show_record_connections(self, name, id_table):
		record = id_table.get_record_by_name(name)
		if not record:
			return
		# показываем зависимости записи от других
		if not record.parents_id:
			return
		graph = nx.DiGraph()
		self.show_parent(graph, record, id_table)
		# self.nodes = graph.nodes
		options = {
			'node_color': 'blue',
			'node_size': 400,
			"node_alpha": 0,
			'line_color': 'grey',
			'linewidths': 0,
			'width': 1.0,
			"with_labels": True,
			"font_size": 7
		}
		nx.draw(graph, **options)
		plt.show()
			
	def show_parent(self, graph, record, id_table):
		if not record.parents_id:
			return
		for id in record.parents_id:
			parent_record = id_table.get_record_by_id(id)
			# print(record.name, parent_record.name)
			graph.add_edge(parent_record.name, record.name)
		
	def onpick(self, event):
		print("click")
		(x, y) = (event.xdata, event.ydata)
		for i in self.nodes:
			node = pos[i]


