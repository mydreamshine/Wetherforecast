# import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import xmltodict
import json
from datetime import datetime


def conversionCoordToName(name):
    AddrDic = dict()
    AddrDic["부산"] = 98, 76
    AddrDic["서울"] = 60, 127
    AddrDic["인천"] = 55, 124
    AddrDic["시흥"] = 57, 123
    AddrDic["춘천"] = 73, 134
    AddrDic["강릉"] = 92, 131
    AddrDic["수원"] = 60, 121
    AddrDic["홍성"] = 55, 106
    AddrDic["청주"] = 69, 106
    AddrDic["대전"] = 67, 100
    AddrDic["안동"] = 91, 106
    AddrDic["전주"] = 63, 89
    AddrDic["대구"] = 89, 90
    AddrDic["포항"] = 102, 94
    AddrDic["울산"] = 102, 84
    AddrDic["창원"] = 90, 77
    AddrDic["여수"] = 73, 66
    AddrDic["광주"] = 58, 74
    AddrDic["목포"] = 50, 67
    AddrDic["제주"] = 52, 38
    AddrDic["울릉"] = 127, 127
    AddrDic["독도"] = 144, 123

    return AddrDic[name]


def getDustinformation(Address):
    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"
    key = "serviceKey=" + "Iq26py4%2BXq0dUHvM7eXZdaHnh3O8fDOQOTVjMw95Kh94fKJqLYh%2FZH%2BaZ7%2FD%2BojU7RJ6ERZXP8M%2BH%2BnL8a4cbQ%3D%3D"
    numOfRows = "&numOfRows=" + str(1)
    sidoname = "&sidoName=" + urllib.parse.quote_plus(Address)  # 한글은 유니코드로 바꿔줘야 한다.
    ver = "&ver=" + "1.3"
    type = "&_returnType=json"

    api_url = url + key + numOfRows + sidoname + ver + type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    numOfRows = "&numOfRows=" + str(data_json["totalCount"])

    api_url = url + key + numOfRows + sidoname + ver + type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)

    #print(data_json)


def getWeatherTomorrow(address):#내일 내일 모래 날씨
    url = "http://www.kma.go.kr/wid/queryDFS.jsp?"
    nx, ny = conversionCoordToName(address)
    gridx = "gridx="+ str(nx)
    gridy = "&gridy=" + str(ny)
    api_url = url+gridx+gridy
    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_dict = xmltodict.parse(data)
    data_list = data_dict['wid']['body']['data']
    print(data_list)
    return data_list

getWeatherTomorrow('부산')

def getWeatherToday(address): #오늘날씨
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?"
    key = "serviceKey=" + "oTDANY4hsh%2FaYtGulZR1hdreS4rwf6pcEU21%2Bk2x7U8uezVVbJ3valCtUCY3jFLjPW8G2cvbjA%2BzeBsbrhm6pQ%3D%3D"
    numOfRows = "&numOfRows=" + str(1)
    nx, ny = conversionCoordToName(address)
    base_date = "&base_date="+ '20180520'
    base_time = "&base_time="+ '2000'
    nx = "&nx=" + str(nx)
    ny = "&ny=" + str(ny)
    pageNo = "&pageNo=" + "1"
    type = "&_type=json"

    api_url = url + key + numOfRows + base_date + base_time + nx+ny+pageNo+type

    data = urllib.request.urlopen(api_url).read().decode('utf8')

    data_json = json.loads(data)
    data_json = data_json["response"]["body"]
    numOfRows = "&numOfRows=" + str(data_json["totalCount"])

    api_url = url + key + numOfRows + base_date + base_time + nx+ny+pageNo+type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)
    data_list = data_json['response']['body']['items']['item']

    currentHour = datetime.today().hour

    T, S, P = None, None, None
    for item in data_list:
        if item['category'] == 'T1H' and str(currentHour) == str(item['fcstTime'])[0:2]:
            T = item['fcstValue']
        elif item['category'] == 'SKY' and str(currentHour) == str(item['fcstTime'])[0:2]:
            S = item['fcstValue']
        elif item['category'] == 'PTY' and str(currentHour) == str(item['fcstTime'])[0:2]:
            P = item['fcstValue']
        if T and S:
            break

    # print(data_json)
    return T, S, P


class DustInformation:
    def __init__(self, Address=None):
        self.address = Address
        self.hour = None
        self.DustValue = None


class WetherInformation:
    def __init__(self):
        self.address = None
        self.day = None
        self.hour = None
        self.temperature = None
        self.skyState = None
        self.ptyState = None

    def Update(self, Address, OffsetDay=0, OffsetHour=0):
        self.address = Address
        if OffsetDay == 0 and OffsetHour == 0:
            self.temperature, self.skyState, self.ptyState = getWeatherToday(Address)
        else:
            wetherinfo_List = getWeatherTomorrow(Address)
            for dict in wetherinfo_List:
                for item in dict.items():
                    self.temperature, self.skyState, self.ptyState = item['temp'], item['sky'], item['pty']
