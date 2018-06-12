import urllib.request
import urllib.parse
import xmltodict
import json
import timeit
from datetime import datetime
from datetime import timedelta
import Load

Addr = dict()
Addr[0] = "시흥"
Addr[1] = "서울"
Addr[2] = "인천"
Addr[3] = "부산"
Addr[4] = "대전"
Addr[5] = "대구"
Addr[6] = "울산"
Addr[7] = "제주"
Addr[8] = "수원"
Addr[9] = "춘천"
Addr[10] = "강릉"
Addr[11] = "광주"
Addr[12] = "청주"
Addr[13] = "안동"
Addr[14] = "전주"
Addr[15] = "포항"
Addr[16] = "창원"
Addr[17] = "여수"
Addr[18] = "홍성"
Addr[19] = "목포"
Addr[20] = "울릉"
Addr[21] = "독도"

AddrXY = dict()
AddrXY["시흥"] = 190, 450
AddrXY["서울"] = 220, 480
AddrXY["인천"] = 150, 450
AddrXY["부산"] = 345, 205
AddrXY["대전"] = 240, 310
AddrXY["대구"] = 300, 260
AddrXY["울산"] = 378, 255
AddrXY["제주"] = 170, 40
AddrXY["수원"] = 200, 393
AddrXY["춘천"] = 265, 490
AddrXY["강릉"] = 330, 475
AddrXY["광주"] = 205, 195
AddrXY["청주"] = 240, 375
AddrXY["안동"] = 310, 350
AddrXY["전주"] = 200, 265
AddrXY["포항"] = 345, 300
AddrXY["창원"] = 305, 195
AddrXY["여수"] = 255, 170
AddrXY["홍성"] = 165, 360
AddrXY["목포"] = 165, 155
AddrXY["울릉"] = 395, 480
AddrXY["독도"] = 423, 395

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


def conversionAddress(Address):
    AddrDic = dict()
    AddrDic["시흥"] = '경기', '정왕동'
    AddrDic["춘천"] = '강원', '석사동'
    AddrDic["강릉"] = '강원', '옥천동'
    AddrDic["수원"] = '경기', '천천동'
    AddrDic["홍성"] = '충남', '홍성읍'
    AddrDic["청주"] = '충북', '복대동'
    AddrDic["안동"] = '경북', '남문동'
    AddrDic["전주"] = '전북', '삼천동'
    AddrDic["포항"] = '경북', '장흥동'
    AddrDic["창원"] = '경남', '반송로'
    AddrDic["여수"] = '전남', '여천동(여수)'
    AddrDic["목포"] = '전남', '부흥동'
    AddrDic["울릉"] = '경북', '태하리'

    if Address in AddrDic:
        return AddrDic[Address]
    else:
        return Address, None


def getDustCurrent(Address):  # 미세먼지를 비롯한 여러 통합대기값 khaiValue는 미래예보정보가 없다.(예보정보가 있기는 하나 위성기상이미지형태임)

    Address, subAddress = conversionAddress(Address)

    url = "http://openapi.airkorea.or.kr/openapi/services/rest/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"
    key = "serviceKey=" + "oTDANY4hsh%2FaYtGulZR1hdreS4rwf6pcEU21%2Bk2x7U8uezVVbJ3valCtUCY3jFLjPW8G2cvbjA%2BzeBsbrhm6pQ%3D%3D" # 성호꺼
    #key = "serviceKey=" + "Iq26py4%2BXq0dUHvM7eXZdaHnh3O8fDOQOTVjMw95Kh94fKJqLYh%2FZH%2BaZ7%2FD%2BojU7RJ6ERZXP8M%2BH%2BnL8a4cbQ%3D%3D" #명준꺼
    numOfRows = "&numOfRows=" + str(200)
    sidoname = "&sidoName=" + urllib.parse.quote_plus(Address)  # 한글은 유니코드로 바꿔줘야 한다.
    ver = "&ver=" + "1.3"
    type = "&_returnType=json"

    api_url = url + key + numOfRows + sidoname + ver + type

    data = urllib.request.urlopen(api_url).read().decode('utf8')
    data_json = json.loads(data)

    data_list = data_json['list']
    # print(data_list)
    try:
        if subAddress:
            for dict in data_list:
                if dict['stationName'] == subAddress:
                    return int(dict['khaiValue']), int(dict['pm10Value'])
        else:
            if len(data_list) > 0:
                return int(data_list[0]['khaiValue']), int(data_list[0]['pm10Value'])
            else:
                return None, None
    except:
        return None, None


def getWeatherTomorrow(address, OffsetDay=0, OffsetHour=0):  # 내일 내일 모래 날씨
    url = "http://www.kma.go.kr/wid/queryDFS.jsp?"
    nx, ny = conversionCoordToName(address)
    gridx = "gridx="+ str(nx)
    gridy = "&gridy=" + str(ny)
    api_url = url+gridx+gridy

    T, S, P = None, None, None#온도, 하늘상태 강우량
    data = urllib.request.urlopen(api_url).read().decode('utf8')

    # 동네예보 API에서 일시적인 ERROR가 났을 경우.
    data_dict = xmltodict.parse(data)
    try:
        data_list = data_dict['wid']['body']['data']
        # print(data_list)

        # 업데이트 되는 API 날씨정보는 매일 오전 6시에 업데이트 된다.
        # day값은 24:00가 넘어가면 Day+1, Day+2 밖에 남지 않게 된다.
        # 즉, 00:00 ~ 06:00까지는 day값이 0이 아닌 1이 된다.
        if int(data_list[0]['day']) != 0:
            OffsetDay = min(OffsetDay + 1, 2)

        T, S, P = None, None, None
        for dict in data_list:
            if dict['day'] == str(OffsetDay) and dict['hour'] == str(OffsetHour):
                T, S, P = float(dict['temp']), int(dict['sky']), int(dict['pty'])
                break
    except:
        return None, None, None
    return T, S, P


def getWeatherToday(address): #오늘날씨
    url = "http://newsky2.kma.go.kr/service/SecndSrtpdFrcstInfoService2/ForecastTimeData?"
    key = "serviceKey=" + "oTDANY4hsh%2FaYtGulZR1hdreS4rwf6pcEU21%2Bk2x7U8uezVVbJ3valCtUCY3jFLjPW8G2cvbjA%2BzeBsbrhm6pQ%3D%3D"
    numOfRows = "&numOfRows=" + str(200)
    nx, ny = conversionCoordToName(address)

    # 동네예보API에서는 현재 분(Minute)이 0~30사이일 경우에는 API가 호출되지 않는다.
    # 이럴 경우에는 현재 시각 - 30분을 하여 과거의 측정된 데이터를 가지고 온다.
    CurretnTime = datetime.today()
    if int(CurretnTime.strftime("%M")) < 30:
        CurretnTime -= timedelta(minutes=30)
    base_date = "&base_date=" + CurretnTime.strftime("%Y%m%d")
    base_time = "&base_time=" + CurretnTime.strftime("%H%M")
    nx = "&nx=" + str(nx)
    ny = "&ny=" + str(ny)
    pageNo = "&pageNo=" + "1"
    type = "&_type=json"

    api_url = url + key + numOfRows + base_date + base_time + nx+ny+pageNo+type
    data = urllib.request.urlopen(api_url).read().decode('utf8')

    T, S, P = None, None, None

    # 동네예보 API에서 일시적인 ERROR가 났을 경우.
    data_json = json.loads(data)
    if data_json["response"]["header"]["resultMsg"] == 'SERVICE ACCESS DENIED ERROR.':
        return T, S, P

    data_json = json.loads(data)
    data_list = data_json['response']['body']['items']['item']

    # print(data_list)

    currentHour = CurretnTime.strftime("%H")

    for item in data_list:
        if item['category'] == 'T1H' and currentHour == str(item['baseTime'])[0:2]:
            T = float(item['fcstValue'])
        elif item['category'] == 'SKY' and currentHour == str(item['baseTime'])[0:2]:
            S = int(item['fcstValue'])
        elif item['category'] == 'PTY' and currentHour == str(item['baseTime'])[0:2]:
            P = int(item['fcstValue'])
        if T and S and P:
            break

    return T, S, P


class WeatherInformation:  # 지역에 따른 현재 통합대기상태, 미세먼지농도와 온도, 기상상태, 우천상태를 관리함
    def __init__(self, Address=None):
        self.__address = Address
        self.__day = None
        self.__khaiValue = None
        self.__PM10Value = None
        self.__temperature = None
        self.__skyValue = None
        self.__ptyValue = None
        self.__H24Temperature = list()
        self.__H24SkyValue = list()
        self.__H24PtyValue = list()
        if Address:
            self.Update(Address, OffsetDay=0, OffsetHour=0)

    # 미세먼지를 비롯한 여러 통합대기수치값 khaiValue는 미래예보정보가 없다.(예보정보가 있기는 하나 위성기상이미지형태임)
    def Update(self, Address, OffsetDay=0, OffsetHour=0):

        # 오늘 날짜와 시간 부여(Offset에 따라 증가된 날짜 시간 부여 가능)
        self.__address, self.__day = Address, datetime.today() + timedelta(days=OffsetDay, hours=OffsetHour)

        # 통합대기수치값과 미세먼지농도 부여
        start = timeit.default_timer()
        self.__khaiValue, self.__PM10Value = getDustCurrent(Address)
        print("getDustCurrent() 실행시간:", timeit.default_timer() - start)

        # Offset에 따른 날짜와 시간에 맞추어 온도, 기상상태, 우/설상태 부여
        start = timeit.default_timer()
        if OffsetDay == 0 and OffsetHour == 0:
            self.__temperature, self.__skyValue, self.__ptyValue = getWeatherToday(Address)
            print("getWeatherToday() 실행시간:", timeit.default_timer() - start)
        else:
            self.__temperature, self.__skyValue, self.__ptyValue = getWeatherTomorrow(Address, OffsetDay, self.__day.hour + OffsetHour)

    def Update_24H(self, Address):
        self.__address = Address

        if self.__temperature is None or self.__skyValue is None or self.__ptyValue is None:
            self.__temperature, self.__skyValue, self.__ptyValue = getWeatherToday(Address)

        for i in range(1, 8):
            OffsetToday = self.__day + timedelta(hours=i*3)
            Normalize3H = OffsetToday.hour + (3 - (OffsetToday.hour % 3)) if OffsetToday.hour % 3 != 0 else OffsetToday.hour
            OffsetDay =  OffsetToday.day - self.__day.day
            T, S, P = getWeatherTomorrow(Address, OffsetDay, Normalize3H)
            self.__H24Temperature.append(T)
            self.__H24SkyValue.append(S)
            self.__H24PtyValue.append(P)

    def get24HTemperature(self):
        return self.__H24Temperature

    def get24HSkyValue(self):
        return self.__H24SkyValue

    def get24HPtyValue(self):
        return self.__H24PtyValue

    def getAdress(self):
        return self.__address

    def getDay(self):
        return self.__day

    def getkhaiValue(self):
        return self.__khaiValue

    def getPM10Value(self):
        return self.__PM10Value

    def getTemperature(self):
        return self.__temperature

    def getSkyValue(self):
        return self.__skyValue

    def getPtyValue(self):
        return self.__ptyValue

    def getkhaiState(self):
        if not self.__khaiValue:
            return '측정정보없음'
        elif self.__khaiValue > 250:
            return '매우나쁨'
        elif self.__khaiValue > 100:
            return '나쁨'
        elif self.__khaiValue > 50:
            return '보통'
        elif self.__khaiValue > 0:
            return '좋음'

    def getPM10State(self):
        if not self.__PM10Value:
            return '측정정보없음'
        elif self.__PM10Value > 150:
            return '매우나쁨'
        elif self.__PM10Value > 80:
            return '나쁨'
        elif self.__PM10Value > 30:
            return '보통'
        elif self.__PM10Value > 0:
            return '좋음'

    def getSkyState(self):
        if not self.__skyValue:
            return '측정정보없음'
        elif self.__skyValue == 1:
            return '맑음'
        elif self.__skyValue == 2:
            return '구름조금'
        elif self.__skyValue == 3:
            return '구름많음'
        elif self.__skyValue == 4:
            return '흐림'

    def getPtyState(self):
        if self.__ptyValue is None:
            return '측정정보없음'
        elif self.__ptyValue == 0:
            return '없음'
        elif self.__ptyValue == 1:
            return '비'
        elif self.__ptyValue == 2:
            return '비/눈'
        elif self.__ptyValue == 3:
            return '눈'

    def print(self):
        print('-----------' + self.__address + '-----------')
        print("온도: ", self.__temperature)

        PtyState = self.getPtyState()
        if PtyState == '없음': print('날씨: ', self.getSkyState())
        else: print('날씨: ', PtyState)

        print('미세먼지: ', self.__PM10Value, '(' + self.getPM10State() + ')')
        print('통합대기수치: ', self.__khaiValue, '(' + self.getkhaiState() + ')')

        AMPM = self.__day.strftime("%p")
        AMPM = '오전' if AMPM == 'AM' else '오후'
        print('업데이트 ', self.__day.strftime("%m/%d"), AMPM, self.__day.strftime("%I:%M"))
        print('--------------------------', end='\n\n')


class WeatherInformationSub:

    def __init__(self, city, x, y):
        self.city = city
        self.x, self.y = x, y
        self.Active = False

    def Update(self):
        Load.Weather[self.city].Update(self.city)
        self.Active = True

    def draw(self):
        # 기상 정보 배경이미지 출력
        Load.image['Background_RegionLayout'].draw(self.x, self.y)

        # 기상 정보 이미지 출력
        info_pty = Load.Weather[self.city].getPtyState()
        info_sky = Load.Weather[self.city].getSkyState()
        if info_pty == '측정정보없음' or info_pty == '없음':
            if info_pty == info_sky == '측정정보없음':
                Load.image['Sun_small'].draw(self.x - 3, self.y + 4)
            elif info_sky == '구름많음' or info_sky == '흐림':
                Load.image['Cloud_small'].draw(self.x-3, self.y+4)
            elif 6 < int(Load.Weather[self.city].getDay().strftime("%H")) < 18:
                Load.image['Sun_small'].draw(self.x-3, self.y+4)
            else:
                Load.image['Moon_small'].draw(self.x-3, self.y+4)
        else:
            if info_pty == '비' or info_pty == '비/눈':
                Load.image['Rain_small'].draw(self.x-3, self.y+4)
            else:
                Load.image['Snow_small'].draw(self.x-3, self.y+4)

        # 도시 이름 그리기
        w, h = Load.font[9].getpixelSize_unicode(self.city)
        interval_height = Load.image['Background_RegionLayout'].h/2
        Load.font[9].draw_unicode(self.x-w/2-1, self.y+interval_height+h/2 , self.city, (0, 0, 0))

        # 현재 온도 그리기
        t = Load.Weather[self.city].getTemperature()
        if t is None: t = 0
        w, h = Load.font[10].getpixelSize(str(t))
        Load.font[10].draw(self.x-w/2-1, self.y-interval_height+h/2+4, str(t), (255, 0, 0))


class Weather24HInformation:

    def __init__(self, city, x, y, width, height):
        self.city = city
        self.x, self.y = x, y
        self.width, self.height = width, height

    def Update(self, city):
        self.city = city
        Load.Weather[self.city].Update_24H(self.city)

    def draw(self):
        pass
