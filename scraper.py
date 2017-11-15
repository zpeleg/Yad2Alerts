import itertools
from typing import List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


class CarAd:
    def __init__(self, model, engine_size, year, price, hand, transmission, location,
                 bump_date, link):
        self.model = model
        self.engine_size = engine_size
        self.year = year
        self.price = price
        self.hand = hand
        self.transmission = transmission
        self.location = location
        self.bump_date = bump_date
        self.link = link

    def __repr__(self):
        return str(self.__dict__)


class YadPage:
    def __init__(self, pageno, link):
        self.pageno = pageno
        self.link = link

    def __repr__(self):
        return "Page no. {}".format(self.pageno)


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
BASE_URL = "http://www.yad2.co.il"
PEUGEOT_URL = "/Cars/Car.php?&ModelID=33&SubModelID=2390"
KIA_URL = "/Cars/Car.php?ModelID=40&SubModelID=1293"

cell_ids = [4,  # Model name
            6,  # Engine size
            8,  # Year
            10,  # Price
            12,  # Hand
            14,  # AT/MT
            16,  # Location
            20,  # Bump date
            21,  # href: rows[0].select('td')[21].a['href']
            ]


def to_ad_object(soup):
    def extract_td(index):
        return soup.select('td')[index].text.strip()

    return CarAd(
        model=extract_td(4),
        engine_size=extract_td(6),
        year=extract_td(8),
        price=extract_td(10),
        hand=extract_td(12),
        transmission=extract_td(14),
        location=extract_td(16),
        bump_date=extract_td(20),
        link=soup.select('td')[21].a['href']
    )


def get_ads_in_page(soup):
    return [to_ad_object(x) for x in soup.select('table.main_table')[0].select('tr.showPopupUnder')]


def get_additional_pages(soup: BeautifulSoup) -> List[YadPage]:
    return [YadPage(int(link.text), link['href']) for link in soup.select("a.showPopupUnder")]


def get_all_ads(url: str) -> List[CarAd]:
    # Create downloader
    downloader = PhantomDownloader()
    downloader.start()
    # Download first page
    first_soup = downloader.download(url)
    # Download the pages
    page_urls = get_additional_pages(first_soup)
    # Download the ads
    ads = [get_ads_in_page(first_soup)]
    page_soups = [debug("Downloading {}".format(u.pageno), downloader.download(u.link)) for u in page_urls]
    downloader.stop()
    ads.extend([get_ads_in_page(s) for s in page_soups])
    ads_flattened = list(itertools.chain.from_iterable(ads))
    return ads_flattened


def debug(msg, itm):
    print(msg)
    return itm


class PhantomDownloader:
    def __init__(self):
        self.driver = None

    def start(self):
        self.driver = webdriver.PhantomJS()

    def stop(self):
        self.driver.quit()

    def download(self, url) -> BeautifulSoup:
        self.driver.get(BASE_URL + url)
        return BeautifulSoup(self.driver.page_source, "html.parser")


def download_with_phantom(url):
    driver = webdriver.PhantomJS()
    driver.get(BASE_URL + url)
    source = driver.page_source
    driver.quit()
    return BeautifulSoup(source, "html.parser")


def main():
    all_ads = get_all_ads(KIA_URL)
    for a in all_ads:
        print(a)


if __name__ == '__main__':
    main()
