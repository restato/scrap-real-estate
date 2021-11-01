# -*- encoding: utf8 -*-
import pandas as pd 
import src.date_util as date_util
import glob
import re

"""
구분    소형    중소형  중형    중대형  대형
전용면적    40.0㎡ 미만 40.0㎡ 이상 ~ 
62.81㎡ 미만    62.81㎡ 이상 ~ 
95.86㎡ 미만    95.86㎡ 이상 ~ 
135.0㎡ 미만    135.0㎡ 이상
"""

def join_meta(df, r_df): 
    df['지역코드'] = df['지역코드'].astype(str)
    df = df.set_index('지역코드').join(r_df).reset_index()
    df['시군구'] = df['시'] + ' ' + df['구']
    return df


def common(df):
    #  case 2013 2013    우만동  500 수원광교 양우 내안애 애플 아파트    9   40  11  NaN 607 41115   NaN 1460    NaN NaN
    df['전용면적'] = df['전용면적'].fillna(0)
    df['전용면적'] = round(df['전용면적'].astype(float), 2)
    df['평수'] = round(df['전용면적'].apply(lambda x: x / float(3.30578)), 2)
    # 60m2이하, 60~85m2, 85m2초과 
    labels = ["60m이하", "60-85m2이하", "85m2초과"]
    df['규모'] = pd.cut(df['전용면적'], [0, 65, 85, 99999999],labels = labels) 
    df['층'] = df['층'].fillna(0)
    df['건축년도'] = df['건축년도'].astype(str) 

    df['년'] = df['년'].astype(int) 
    df['월'] = df['월'].astype(int) 
    df['일'] = df['일'].astype(int) 

    df['지역코드'] = df['지역코드'].apply(lambda x: str(x).split('.')[0]) 
    
    df['평당거래액'] = df['거래금액'] / df['평수']
    # df['평당거래액'] = df['평당거래액'].astype(int)

    # 날짜
    df['거래날짜'] = df.apply(date_util.to_datetime, axis=1)
    df['아파트_전처리'] = df['아파트'].apply(lambda x: ' '.join(re.compile('[a-zA-Z가-힣0-9]+').findall(x)))
    if '도로명' in df: # trade
        df['메시지'] = df['시'] + ' ' + df['구'] + ' ' + df['법정동'] + ' ' + df['도로명'] + ' ' + df['아파트_전처리']
    else: # rent
        df['메시지'] = df['시'] + ' ' + df['구'] + ' ' + df['법정동'] + ' ' + df['아파트_전처리']
    df = df.drop('아파트_전처리', axis=1)
    return df


def rent(df): 
    df['보증금액'] = df['보증금액'].apply(lambda x: int(x.replace(',', '')))  
    df['월세금액'] = df['월세금액'].astype(str).apply(lambda x: int(x.replace(',', '')))
    df['거래유형'] = df['월세금액'].apply(lambda x: "월세" if x > 0 else "전세")
    df['거래금액'] = df['보증금액'] + 24 * df['월세금액']
    df = common(df) 
    return df


def trade(df):
    df['거래금액'] = df['거래금액'].apply(lambda x: int(x.replace(',', ''))) 
    df = common(df)
    return df

   
def filtering(frame):
    # 매매
    trade_cols = ['지역코드', '건축년도', '도로명', '도로명건물본번호코드', '도로명건물부번호코드',
       '도로명시군구코드', '도로명일련번호코드', '도로명지상지하코드', '도로명코드', '법정동', '법정동본번코드',
       '법정동부번코드', '법정동시군구코드', '법정동읍면동코드', '법정동지번코드', '아파트', '일련번호',
       '전용면적', '지번', '층', '시', '구']
    
    trade_cols = ['시','구', '메시지', '아파트', '법정동', '건축년도']
    if '도로명' in frame:
        trade_cols.append('도로명')
    frame = frame[trade_cols]
    frame = frame.drop_duplicates()
    return frame

# def get_apt_list(path="/home/irteam/data/apt-trade/41135"):
#     import re 
#     filelist = glob.glob("%s/*.csv" % path) 
#     frames = []
#     for file in filelist: 
#         try:
#             frame = pd.read_csv(file)
#             frame = frame.set_index('지역코드').join(road_code).reset_index()  
#             frame = preprocessing(frame)
#             frame = filtering(frame)
#             frames.append(frame) 
#         except Exception as e:
#             continue
#     return frames


def convert_column_name(pdf):
    column_dict = {
               '지역코드': 'area_code',
               '거래금액': 'transaction_amount',
               '건축년도': 'year_of_construction',
               '년': 'transaction_year',
               '월': 'transaction_month',
               '일': 'transaction_day',
               '도로명': 'road_name',
               '도로명건물본번호코드':'road_name_building_first_code',
               '도로명건물부번호코드': 'road_name_building_second_code',
               '도로명시군구코드': 'road_name_sigungu_code',
               '도로명일련번호코드': 'road_name_serial_number_code',
               '도로명지상지하코드': 'road_name_ground_underground_code',
               '도로명코드': 'road_name_code',
               '법정동': 'legal_dong',
               '법정동본번코드': 'legal_dong_first_code',
               '법정동부번코드': 'legal_dong_second_code',
               '법정동시군구코드': 'legal_sigungu_code',
               '법정동읍면동코드': 'legal_eupmundong_code',
               '법정동지번코드': 'legal_jibun_code',
               '아파트': 'apt_name',
               '일련번호': 'serial_number',
               '전용면적': 'dedicated_area',
               '지번': 'jibun',
               '층': 'floor',
               '시': 'si',
               '구': 'gu',
               '시군구': 'sigungu',
               '평당거래액': 'amount_per_area',
               '평수': 'area',
               '규모': 'dedicated_area_level',
               '거래유형': 'sale_type',
               '메시지': 'description',
               '거래날짜': 'transaction_date'
              }
    # rent
    column_dict.update({'보증금액': 'deposit', '월세금액': 'monthly_rent'})
    pdf = pdf.rename(columns=column_dict)
    return pdf
