import requests 
import os
from bs4 import BeautifulSoup as BS

base_url = "http://www.jagodibuja.com/page/{}/"
os.makedirs('Jagodibuja', exist_ok = True)

for i in range(1, 138):
	url = base_url.format(i)

	raw_text = requests.get(url)

	if raw_text.reason == 'OK':
		soup = BS(raw_text.text, 'lxml')

		articles = soup.find_all('article', {'class': 'category-living-with-hipstergirl-and-gamergirl'})

		for article in articles:
			try:
				img_url = article.p.a['href']
				name = img_url.split('/')[-1]

				try:
					r = requests.get(img_url, timeout = 60)

					p = os.path.sep.join(['Jagodibuja', "{}".format(name)])
					f = open(p, "wb")
					f.write(r.content)

					f.close()
				except:
					print("[Error] Skipping Image {}".format(name))

				print ("[INFO] Downloaded: {}".format(p))
			except:
				print ("[Error]")
