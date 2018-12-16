import requests
import re
from bs4 import BeautifulSoup as BS

def getPiecesUrls(soup):
	urls = list()

	try:
		central = soup.find('div', id = 'central')
		thumbs = central.find('div', id = 'thumbs')
		pieces = thumbs.find_all('div', id = re.compile(r'^piece-'))
		
		for i in range(len(pieces)):
			urls.append(pieces[i].a['href'])
	except Exception as e:
		print (f"Function: getPiecesUrls() | Error: {e}")

	return urls

def getPiecesImgUrl(piece_page_url):

	r = requests.get(piece_page_url)

	if r.status_code != 200:
		print (f'Response Code: {base_r.status_code}')
		return -1

	try:
		piece_soup = BS(r.text, 'html.parser')
		piece_soup = piece_soup.find('div', id = 'central').find('div', id = 'content')

		title = piece_soup.h1.text
		img = piece_soup.find('div', id = 'facet-image')
		img = img.img['src']

		return (title, img)
	except Exception as e:
		print (f"Function: getPiecesImgUrl() | Error: {e}")
		return -1

def getImgURLS(piece_pages_urls):
	img_urls = list()

	for piece_url in piece_pages_urls:
		img_urls.append(getPiecesImgUrl(piece_url))

	return img_urls

def downloadImage(image_title, image_url):
	r = requests.get(image_url)

	if r.status_code != 200:
		print (f'Response Code: {base_r.status_code}')
		return -1

	with open(f"{image_title}.jpg", 'wb') as f:
		f.write(r.content)

	return "sucess"

if __name__ == "__main__":

	# Base URL "http://www.facets.la/"
	base_url = str(input("Facets Website: ")) 

	base_r = requests.get(base_url)

	if base_r.status_code != 200:
		exit(f'Response Code: {base_r.status_code}')

	base_soup = BS(base_r.text, 'html.parser')

	pieces_urls = getPiecesUrls(base_soup)
	imgs_urls = getImgURLS(pieces_urls)

	for title, img_url in imgs_urls:
		print (f"\n Downloading {img_url}...")

		if downloadImage(title, img_url) == -1:
			print (f"\n Downloading Failed \n")
		else:
			print (f"\n Image Downloaded and Saved.")