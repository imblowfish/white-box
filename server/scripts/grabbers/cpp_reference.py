from bs4 import BeautifulSoup
from base_grabber import BaseGrabber
import codecs
import xml.etree.ElementTree as et

class CPPReferenceParser(BaseGrabber):
	doc_dir = "./grabbers/cppreference"
	idents_dir = "reference/en"
	dir = "../database/cpp_reference"
	def parse(self):
		self.parse_index()
		self.parse_idents_list()
		
	def parse_index(self):
		tree = et.parse(f"{self.doc_dir}/cppreference-doxygen-local.tag.xml")
		# получаем список всех файлов
		root = tree.getroot()
		self.paths = []
		for child in root:
			path = child.find("filename")
			if path is not None:
				self.paths.append(path.text)
		
	def parse_idents_list(self):
		for path in self.paths:
			if not path:
				continue
			if path.find(self.doc_dir) >= 0:
				rel_path = f"{path}.html"
			else:
				rel_path = f"{self.doc_dir}/{self.idents_dir}/{path}.html"
			print(rel_path)
			try:
				file = codecs.open(rel_path, "r", "utf8")
			except:
				print(f"Error with parse file {rel_path}")
				continue
			soup = BeautifulSoup(file.read(), "html.parser")
			page = soup.find("div", {"id": "content"})
			idents_list = {}
			name = path.split('/')[-1]
			if not self.save_html(self.dir, name, page):
				print(f"Error with saving {path}")
				continue
		return True
				
			
cpp_p = CPPReferenceParser()
cpp_p.parse()