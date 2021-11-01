# enconding: utf8
import argparse
from src.scrapper import Scrapper
from src.logger import init_logger

logger = init_logger('main')

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url_type', help='url_type [apt-trade|apt-rent]', required=True)
    parser.add_argument('--service_key', help='service_key[1|2]', required=True)
    args = parser.parse_args()

    logger.info(args.url_type)
    logger.info(args.service_key)
    scrapper = Scrapper(args.url_type, args.service_key)
    scrapper.run()