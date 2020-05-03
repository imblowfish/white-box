from bs4 import BeautifulSoup
from base_grabber import BaseGrabber

class SDLWikiParser(BaseGrabber):
	begin_url = "https://wiki.libsdl.org"
	search_url = "https://wiki.libsdl.org/CategoryAPI"
	dir = "../database/sdl_wiki"
	def parse_idents_list(self):
		self.page = self.get_page(self.search_url)
		if not self.page:
			return
		soup = BeautifulSoup(self.page.content, "html.parser")
		divs = soup.find_all("div", {"class":"searchresults"})
		idents_list = {}
		for div in divs:
			for a in div.find_all("a"):
				name = a.text
				href = a["href"]
				idents_list[name] = self.begin_url+href
		if not self.save_json(self.dir+"/idents.json", idents_list):
			return
		return idents_list
		
	def parse_page(self, ident_name, url):
		page = self.get_page(url)
		if not page:
			return False
		soup = BeautifulSoup(page.content, "html.parser")
		page = soup.find("div", {"id": "page"})
		if not self.save_html(self.dir, ident_name, page):
			return False
		return True

# import sys
# def do_command():
	# if len(sys.argv) < 2:
		# print("Too few arguments")
		# return
sdl_p = SDLWikiParser()
sdl_p.parse()
# ident_page = sdl_p.has_ident("SDL_HINT_AROMETER_AS_JOYSTICK")
# if ident_page:
	# print("Can show page")
# else:
	# print("Can't show page")
