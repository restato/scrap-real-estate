# enconding: utf8

import os
import json
from time import sleep
import pandas as pd

import configparser
import src.preprocessing as preprocessing
import src.open_data  as open_data
import src.data_util as data_util
import src.date_util as date_util
from src.logger import init_logger

logger = init_logger('scrapper')

class Scrapper():
    
    def __init__(self, url_type, service_key):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('config.ini')
        self.url_type = url_type
        self.service_key = self.config['SERVICE_KEYS'][service_key]
        self.count = 0

    def run(self):
        logger.info('*' * 20)
        url = self.config['OPEN_DATA_URLS'][self.url_type]
        is_limit = False
        logger.info("START SCRAP %s" % self.url_type)
        logger.info("SERVICE KEY: %s" % self.service_key)
        print(self.url_type, url)
        
        road_codes = data_util.get_rcodes()
        # for rcode in data_util.get_rcodes():
        # for rcode in data_util.get_rcode():
        for rcode in road_codes.index:
            empty_count = 0
            # load rcode meta 
            collection_info = {}
            collection_info_path = './collection_%s_info.json'  % self.url_type
            if os.path.isfile(collection_info_path):
                collection_info = json.load(open(collection_info_path, 'r'))

            for ym in date_util.get_yms(end_ym="198801"): #['202004']: #['199101']: #date_util.get_yms(end_ym="202003"):
                print(ym)
                if str(rcode) in collection_info:
                    if collection_info[str(rcode)] == str(ym): 
                        print("rcode: %s: start ym: %s" % (rcode, collection_info[str(rcode)]))
                        break

                dir_path = self.config['DATA']['ROOT']
                data_util.create_dir(dir_path)
                raw_dir_path = os.path.join(dir_path, 'raw', self.url_type, rcode)
                data_util.create_dir(raw_dir_path)
                raw_file_path = os.path.join(raw_dir_path, ym + '.csv')

                # TODO: Check condition
                # step(1): save raw data
                # add scrap data condition
                is_collected = False 
                is_empty = False
                scrap_type  = data_util.do_scrap(raw_file_path, ym)
                if scrap_type >= 1: # collect
                    result_code, df = self.open_data(url, rcode, ym)
                    sleep(0.10) # sec

                    if result_code == "99":
                        logger.info("STOP SCRAP")
                        is_limit = True
                        break
                    else:
                        if len(df) > 1:
                            df = df.drop_duplicates()
                            self.count += 1
                            if scrap_type == 2: # recollection
                                origin_df = data_util.read(raw_file_path)
                                merged_df = pd.concat([origin_df, df])
                                merged_df = merged_df.drop_duplicates().reset_index()
                                merged_df = merged_df.drop('index', axis=1)
                                data_util.create_dir(raw_dir_path.replace("raw","merged"))
                                data_util.save(merged_df, raw_file_path.replace("raw","merged"))
                            data_util.save(df, raw_file_path)
                            is_collected = True
                        else:
                            is_empty = True

                if is_empty:
                    collection_info[str(rcode)] = str(ym)
                    print("check empty_count: %d" % empty_count)
                    empty_count += 1
                    if empty_count >= 2:
                        break
                    
                if is_limit: # break ymd 
                    break

                if (not is_empty) and (is_collected):
                    # step(2): save preprocessed data
                    # df = data_util.read(raw_file_path) # for debugging
                    preprocessed_dir_path = os.path.join(dir_path, 'preprocessed', self.url_type, rcode)
                    preprocessed_file_path = os.path.join(preprocessed_dir_path, ym+'.csv')
                    data_util.create_dir(preprocessed_dir_path)
                    df = df.dropna()
                    df = preprocessing.join_meta(df, road_codes)
                    if self.url_type == "apt-trade":
                        df = preprocessing.trade(df)
                    elif self.url_type == "apt-rent":
                        df = preprocessing.rent(df)
                    df = preprocessing.convert_column_name(df) 
                    data_util.save(df, preprocessed_file_path)

            json.dump(collection_info, open(collection_info_path, 'w'))
            if is_limit: # break rcode
                break

        msg = "%s TOTAL # OF DATA : %d"  % (self.url_type, self.count) 
        logger.info(msg)
    logger.info("STOP SCRAP")
    logger.info("*" * 20 + "\n")
    logger.info("")


    def open_data(self, url, rcode, ym):
        print(url, rcode, ym)
        response = open_data.get_data(url, rcode, ym, self.service_key)
        status_code = response.status_code
        if status_code == 200:
            root = open_data.parse_xml(response.content)
            result_code, result_msg = open_data.get_result_info(root)
            if result_code == '00':
                df = open_data.xml_to_pdf(root)
                return result_code, df
            else:
                # 99: LIMITED NUMBER OF SERVICE REQUESTS EXCEEDS ERROR 
                logger.info("> %s %s" % (result_code, result_msg))
                print(result_code, result_msg)
                return result_code, None
        else:
            logger.info("response status_code: %s" % (status_code))
            print('response status_code', response.status_code)
            return response.status_code, None