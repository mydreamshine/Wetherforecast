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