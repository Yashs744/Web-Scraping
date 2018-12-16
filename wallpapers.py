# Library
import requests
from bs4 import BeautifulSoup as BS
from fake_useragent import UserAgent
import os

# Get Chrome User Agent
UA = UserAgent()
header = {'User-Agent': UA.chrome}

# Base URL
base_url = "https://wallpaperscraft.com{}"

def getSoup(url):
    r = requests.get(url, headers = header)

    if r.status_code == 200:
        return BS(r.text, 'html5lib')

def getImage(url, folder):
    r = requests.get(url, headers = header)

    if url.endswith(('.jpg', 'jpeg', '.png')):
        if r.status_code == 200:
            image_name = url.split('/')[-1]

            try:
                image_path = os.path.sep.join([f'{folder}', f"{image_name}"])

                with open(image_path, 'wb') as f:
                    f.write(r.content)

                print (f"[X] Image: {image_name} Saved to the disk.")
            except Exception as e:
                print (f'[!] Exception occured {e}')
        else:
            print (f'[!!] Status Code: {r.status_code}')
    else:
        print ('[!] Image Format no supported')

def Images(catalog_url):
    new_url = base_url.format(catalog_url)

    soup = getSoup(new_url)
    last_page = soup.findAll('a', {'class': 'pager__link'})[-1]['href']
    last_page = int(last_page.split('/')[-1].split('page')[-1])

    cat = catalog_url.split('/')[-1].capitalize()
    os.makedirs(cat, exist_ok = True)

    i = 1
    flag = True
    new_url = new_url + "/page{}"

    while flag and i <= last_page:
        links = soup.find_all('a', {'class': 'wallpapers__link'})
        for link in links:
            try:
                image_url = link.get('href')
                image_url = base_url.format(image_url)

                soup = getSoup(image_url)
                original_url = soup.findAll('span', {'class': 'wallpaper-table__cell'})[1].find('a')['href']
                original_url = base_url.format(original_url)

                soup = getSoup(original_url)
                image = soup.find('a', {'class': 'gui-button gui-button_full-height'})['href']

                getImage(image, cat)
            except Exception as e:
                print ("f[!] Error: {e}")
                continue

        next_page = str(input("[--] Next Page? (y/n): "))

        if next_page.lower() == 'y':
            i = i + 1
            soup = getSoup(new_url.format(i))
        else:
            flag = False
            break

def getCatalog():
    soup = getSoup(base_url.format('/'))

    filters = soup.find('div', {'class': 'filters'})
    filters = filters.find('ul', {'class': 'filters__list JS-Filters'})
    catalog = filters.findAll('a', {'class': 'filter__link'})

    catalogs = {}

    for cat in catalog:
        link = cat['href']

        catalogs[link.split('/')[-1]] = link

    return catalogs

if __name__ == "__main__":
    print ("Welcome to WallpapersCraft.\n")

    catalogs = getCatalog()

    print ("Catalog of Categories Available: ")
    for (i, value) in enumerate(catalogs.keys()):
        print (f"{i}. {value.capitalize()}")

    cat = str(input("Enter the Category: "))

    cat_url = catalogs[cat.lower()]
    Images(cat_url)

    print ("\n Thank you. GoodBye!!!")