from dataclasses import dataclass, field
from itemloaders.processors import TakeFirst, MapCompose
from scrapy.loader import ItemLoader

import re


@dataclass
class UniversityItem:
    name: str = field(default=None)
    rating: float = field(default=None)
    phone: str = field(default=None)


def parse_rating(x):
    try:
        return float(re.search(r"(\d+\.\d+)", x).group(1))
    except:
        return

def parse_phone(x):
    return x.split(":")[1].strip()


class UniversityItemLoader(ItemLoader):
    default_input_processor = MapCompose(str.strip)
    default_output_processor = TakeFirst()
    default_item_class = UniversityItem

    rating_in = MapCompose(parse_rating)
    phone_in = MapCompose(parse_phone)
