import requests
from bs4 import BeautifulSoup


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


USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
SAMPLE_URL = "http://www.yad2.co.il/Cars/Car.php?AreaID=&ModelID=33&SubModelID=2390&FromYear=&UntilYear=&Auto=&fromPrice=&untilPrice=&Info="

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


def to_ad_object(x):
    return {"Model": x[4].text.strip()}


def get_rows_in_page(url):
    resp = requests.get(url, headers={'User-Agent': USER_AGENT})
    soup = BeautifulSoup(resp.text)
    return [to_ad_object(x) for x in soup.select('table.main_table')[0].select('tr.showPopupUnder')]


def main():
    get_rows_in_page(
        "http://www.yad2.co.il/Cars/Car.php?AreaID=&ModelID=33&SubModelID=2390&FromYear=&UntilYear=&Auto=&fromPrice=&untilPrice=&Info=")


if __name__ == '__main__':
    main()
