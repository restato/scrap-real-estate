# encoding: utf8
import os
import pandas as pd
import src.date_util as date_util


# # return only areacodes
# def get_rcodes():
#     f_in = open('../data/road_code.csv', 'r')
#     lines = [x[:-1].split(',') for x in f_in.readlines()]
#     rcodes = [x[0] for x in lines]
#     rcodes = list(set(rcodes))
#     return rcodes


# return pandas dataframe
def get_rcodes():
    road_code = pd.read_csv('./data/road_code.csv',names=["지역코드", "0", "1","도로명","시","구"], dtype=str)
    road_code = road_code.set_index('지역코드')[['시','구']]
    road_code = road_code.drop_duplicates()
    road_code = road_code[(road_code['시'] == '서울특별시') | (road_code['시'] == '경기도') ]
    # road_code = road_code[(road_code['시'] == '경기도') ]
    return road_code #.head(3).tail(1) #.head(3)


# for sample
def get_rcode():
    return ['41135']


def check_file_exist(filepath):
    if os.path.isfile(filepath):
        return True
    return False


def is_empty(filepath):
    f_in = open(filepath, 'r')
    lines = [line[:-1] for line in f_in.readlines()]
    if lines == ['']:
        return True
    return False


'''
2달 전까지는 무조건 데이터를 재수집하도록
예) 202004월에는 202004, 202003은 무조건 수집
'''

def do_scrap(filepath, ym):
    if check_file_exist(filepath):
        # 파일이 있으면 
        # 파일이 있어도 두달 전까지는 무조건 재수집
        # print("수집날짜:", ym, "현재날짜:", date_util.get_ym_now())
        if int(ym) >= int(date_util.get_ym_now()):
            print("re-collection", ym) 
            # send_msg_to_slack("re-collect: %s" % ym) 
            return 2 # re-collect
        else:
            # 최근이 아닌데 데이터가 있을경우 원래 데이터가 없는것으로 간주
            # 예) 1999년 데이터가 있지만 비어있다면 원래 데이터 없는것
            print("already collect: %s" % ym)
            return False
    else:
        # 파일이 없으면 스크랩 
        print(filepath, 'is not exist %s' % ym)
        return 1 # collect 


def create_dir(dir_path):
    # print(dir_path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        # print("Directory " , dir_path,  " Created ")
    # else:    
        # print("Directory " , dir_path ,  " already exists")


def save(df, filepath):
    df.to_csv(filepath, index=False)


def read(filepath):
    return pd.read_csv(filepath)
