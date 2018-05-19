# import xml.etree.ElementTree as ET
import urllib.request
import urllib.parse
import json


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

    print(data_json)


getDustinformation("경기")

def getWeatherinformation(address):
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastGrib?"
    key = "serviceKey=" + "oTDANY4hsh%2FaYtGulZR1hdreS4rwf6pcEU21%2Bk2x7U8uezVVbJ3valCtUCY3jFLjPW8G2cvbjA%2BzeBsbrhm6pQ%3D%3D"
    numOfRows = "&numOfRows=" + str(1)
    base_date = "&base_date="+ '20180519'
    base_time = "&base_time="+ '0600'
    nx = "&nx=" + "97"
    ny = "&ny=" + "74"
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

    print(data_json)

getWeatherinformation('부산')

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

    nx, ny = AddrDic[name]