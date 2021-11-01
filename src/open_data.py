# encoding: utf8
import requests
import xml.etree.ElementTree as ET
import pandas as pd 

'''
def get_data(url, rcode, date):
    # url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcAptTradeDev"
    # url = "http://openapi.molit.go.kr/OpenAPI_ToolInstallPackage/service/rest/RTMSOBJSvc/getRTMSDataSvcOffiRent"
    querystring = {
            "pageNo":"1",
            "startPage":"1",
            "numOfRows":"999999",
            "pageSize":"10",
            "LAWD_CD":""+rcode+ "",
            "DEAL_YMD":""+date+"",
            "type":"json",
            "serviceKey":"vp5RvL5ncgGVGqhnbaNFu5DePN1bHRd+E3DNYN2WdueSS6y9rS1RDLi45r0tqc7BIDJvsEZaUMhYxOk+dcdRdA=="}
    # print querystring
    headers = {
        'cache-control': "no-cache",
        'postman-token': "e8d4c5d9-9287-549d-b5bc-9cdd60e76e1d"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response
'''

def get_data(url, rcode, ym, svc_key):
    print("service_key", svc_key)
    querystring = {
        "pageNo":"1",
        "startPage":"1",
        "numOfRows":"99999",
        "pageSize":"10",
        "LAWD_CD":"" + rcode + "",
        "DEAL_YMD":"" + ym + "",
        "type":"json",
        "serviceKey":"" + svc_key + ""}

    headers = {
        'cache-control': "no-cache",
    }
    print(querystring)
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response


def parse_xml(text):
    root = ET.fromstring(text)
    return root


def xml_to_pdf(root):
    item_list = []
    for child in root.find('body').find('items'):
        elements = child.findall('*')
        data = {}
        for element in elements:
            tag = element.tag.strip()
            text = element.text.strip()
            # print tag, text
            data[tag] = text
        item_list.append(data)
    return pd.DataFrame(item_list)


def get_result_info(root):
    result_code = root.find('header').find('resultCode').text
    result_msg = root.find('header').find('resultMsg').text
    return result_code, result_msg


def get_sample():
    data_as_string = """
    <item><거래금액>    82,500
                </거래금액><건축년도>2008
            </건축년도><년>2015
        </년><도로명>사직로8길
    </도로명><도로명건물본번호코드>00004
    </도로명건물본번호코드><도로명건물부번호코드>00000
    </도로명건물부번호코드><도로명시군구코드>11110
    </도로명시군구코드><도로명일련번호코드>03
    </도로명일련번호코드><도로명지상지하코드>0
    </도로명지상지하코드><도로명코드>4100135
    </도로명코드><법정동> 사직동
    </법정동><법정동본번코드>0009
    </법정동본번코드><법정동부번코드>0000
    </법정동부번코드><법정동시군구코드>11110
    </법정동시군구코드><법정동읍면동코드>11500
    </법정동읍면동코드><법정동지번코드>1
    </법정동지번코드><아파트>광화문풍림스페이스본(9-0)
    </아파트><월>12
    </월><일>1~10
    </일><일련번호>11110-2203
    </일련번호><전용면적>94.51
    </전용면적><지번>9
    </지번><지역코드>11110
    </지역코드><층>11
    </층>
    </item>
    """
    return data_as_string
 
