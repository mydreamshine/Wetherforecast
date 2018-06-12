from pico2d import*
import Framework
import Load
import SimpleWeatherScene

name = "DetailWeatherScene"
image, font, weather, weather24H = None, None, None, None
MouseX, MouseY = 0, 0
city = "시흥"

KhaiCurrentX = 0
FrictionFactor = 0.03


def enter():
    global image, font, weather, weather24H, KhaiCurrentX
    KhaiCurrentX = 0
    font = Load.font
    image = Load.image
    weather = Load.Weather
    weather24H = Load.Weather24H
    weather[city].Update(city)
    weather24H.Update(city)
    pass


def exit():
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global MouseX, MouseY
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            Framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            Framework.quit()
        elif event.type == SDL_MOUSEMOTION:
            MouseX, MouseY = event.x, (get_canvas_height() - 1) - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            MouseX, MouseY = event.x, (get_canvas_height() - 1) - event.y
            width, height = image["MainButton_Green"].w, image["MainButton_Green"].h
            a = " 간편대기 "
            w, h = Load.font[18].getpixelSize_unicode(a)
            CenterPointX, CenterPointY = get_canvas_width() / 2, 550 + h / 2
            x1, y1, x2, y2 = Load.GetCorners(CenterPointX, CenterPointY, width, height)
            if Load.PointInRect(x1, y1, x2, y2, MouseX, MouseY):
                Framework.change_state(SimpleWeatherScene)
    pass


def update():
    pass


def Scene_draw():
    global image, font, weather, weather24H, KhaiCurrentX, FrictionFactor

    # 배경 그리기
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 2
    image['Background_White'].draw(CenterPointX, CenterPointY)


    KhaiValue = weather[city].getkhaiValue()
    KhaiState = weather[city].getkhaiState()

    s = str(KhaiValue)
    # 통합 대기 정보 그리기
    a = " 간편대기 "
    w, h = Load.font[18].getpixelSize_unicode(a)
    CenterPointX, CenterPointY = get_canvas_width() / 2, 550 + h / 2
    if int(s) < 50:
        image['MainButton_Blue'].draw(CenterPointX, CenterPointY)
        Load.font[18].draw_unicode(CenterPointX - w / 2, CenterPointY, a, (77, 173, 255))
    if 50 < int(s) and int(s) <= 100:
        image['MainButton_Green'].draw(CenterPointX, CenterPointY)
        Load.font[18].draw_unicode(CenterPointX - w / 2, CenterPointY, a, (0, 197, 24))
    if 100 < int(s) and int(s) <= 250:
        image['MainButton_Caution'].draw(CenterPointX, CenterPointY)
        Load.font[18].draw_unicode(CenterPointX - w / 2, CenterPointY, a, (253, 161, 99))
    if 250 < int(s):
        image['MainButton_Bad'].draw(CenterPointX, CenterPointY)
        Load.font[18].draw_unicode(CenterPointX - w / 2, CenterPointY, a, (255, 93, 93))

    w, h = Load.font[55].getpixelSize_unicode(s)
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height()*(3/4)
    if int(s) < 50:
        Load.font[55].draw_unicode(CenterPointX - w / 2, CenterPointY, s, (77, 173, 255))
    if 50< int(s) and int(s)<=100:
        Load.font[55].draw_unicode(CenterPointX - w / 2, CenterPointY, s, (0, 197, 24))
    if 100< int(s) and int(s)<=250:
        Load.font[55].draw_unicode(CenterPointX - w / 2, CenterPointY, s, (253, 161, 99))
    if 250< int(s):
        Load.font[55].draw_unicode(CenterPointX - w / 2, CenterPointY, s, (255, 93, 93))


    w, h = Load.font[21].getpixelSize_unicode(KhaiState)
    CenterPointX, CenterPointY = get_canvas_width() / 2-(get_canvas_width() / 4), get_canvas_height() * (3 / 5)
    if KhaiState == "좋음":
        Load.font[21].draw_unicode(CenterPointX - w / 2 - 35, CenterPointY, KhaiState, (77, 173, 255))
    if KhaiState == "보통":
        Load.font[21].draw_unicode(CenterPointX - w / 2 - 35, CenterPointY, KhaiState, (0, 197, 24))
    if KhaiState == "나쁨":
        Load.font[21].draw_unicode(CenterPointX - w / 2 - 35, CenterPointY, KhaiState, (253, 161, 99))
    if KhaiState == "매우나쁨 ":
        Load.font[21].draw_unicode(CenterPointX - w / 2 - 35, CenterPointY, KhaiState, (255, 93, 93))


    if KhaiState == "측정정보없음":
        m = "측정정보없음"
        Load.font[21].draw_unicode(CenterPointX + 65, CenterPointY, m, (124, 124, 124))
    if KhaiState == '보통':
        image['DustState_Normal'].draw(CenterPointX+35, CenterPointY)
        m = " 민감군 주의하세요     "
        Load.font[21].draw_unicode(CenterPointX +65, CenterPointY, m, (0, 197, 24))
    if KhaiState == '좋음':
        image['DustState_Good'].draw(CenterPointX+35, CenterPointY)
        m = " 민감군 걱정마세요     "
        Load.font[21].draw_unicode(CenterPointX +65, CenterPointY, m, (77, 173, 255))
    if KhaiState == '나쁨':
        image['DustState_Caution'].draw(CenterPointX+35, CenterPointY)
        m = " 마스크 착용하세요     "
        Load.font[21].draw_unicode(CenterPointX +65, CenterPointY, m, (253, 161, 99))
    if KhaiState == '매우나쁨 ':
        image['DustState_Bad'].draw(CenterPointX+45, CenterPointY)
        m = " 외출을 삼가하세요     "
        Load.font[21].draw_unicode(CenterPointX +70, CenterPointY, m, (255, 93,93 ))

    Color = (77, 173, 255)
    CenterPointX, CenterPointY = 65, get_canvas_height() / 2 -20
    image['Line_DustGood'].draw(CenterPointX, CenterPointY)
    if(KhaiValue<50):
        CenterPointX = CenterPointX-image['Line_DustGood'].w/2 + KhaiValue*image['Line_DustGood'].w/50
        KhaiCurrentX += (CenterPointX - KhaiCurrentX) * FrictionFactor
        image['DustValue_Good'].draw(KhaiCurrentX, CenterPointY+25)
        w, h = Load.font[18].getpixelSize_unicode(str(KhaiValue))
        Load.font[18].draw_unicode(KhaiCurrentX - w / 2, CenterPointY + h / 2 +20, str(KhaiValue), (77, 173, 255))

    CenterPointX, CenterPointY = 175, get_canvas_height() / 2-20
    image['Line_DustNormal'].draw(CenterPointX, CenterPointY)
    if (50 <= KhaiValue and KhaiValue < 100):
        CenterPointX = CenterPointX - image['Line_DustNormal'].w / 2 + (KhaiValue-50) * image['Line_DustNormal'].w / 50
        KhaiCurrentX += (CenterPointX - KhaiCurrentX) * FrictionFactor
        image['DustValue_Normal'].draw(KhaiCurrentX, CenterPointY+25)
        w, h = Load.font[18].getpixelSize_unicode(str(KhaiValue))
        Load.font[18].draw_unicode(KhaiCurrentX - w / 2, CenterPointY + h / 2 + 20, str(KhaiValue), (0, 197, 24))

    CenterPointX, CenterPointY = 285, get_canvas_height() / 2-20
    image['Line_DustCaution'].draw(CenterPointX, CenterPointY)
    if (100 <= KhaiValue and KhaiValue < 250):
        CenterPointX = CenterPointX - image['Line_DustCaution'].w / 2 + (KhaiValue-100) * image['Line_DustCaution'].w / 150
        KhaiCurrentX += (CenterPointX - KhaiCurrentX) * FrictionFactor
        image['DustValue_Caution'].draw(KhaiCurrentX, CenterPointY + 25)
        w, h = Load.font[18].getpixelSize_unicode(str(KhaiValue))
        Load.font[18].draw_unicode(KhaiCurrentX - w / 2, CenterPointY + h / 2 +20, str(KhaiValue), (253, 161, 99))

    CenterPointX, CenterPointY = 395, get_canvas_height() / 2-20
    image['Line_DustBad'].draw(CenterPointX, CenterPointY)
    if (250 <= KhaiValue):
        CenterPointX = CenterPointX - image['Line_DustBad'].w / 2 + (KhaiValue-250) * image['Line_DustBad'].w / 250
        KhaiCurrentX += (CenterPointX - KhaiCurrentX) * FrictionFactor
        image['DustValue_Bad'].draw(KhaiCurrentX, CenterPointY+25)
        w, h = Load.font[18].getpixelSize_unicode(str(KhaiValue))
        Load.font[18].draw_unicode(KhaiCurrentX - w / 2, CenterPointY + h / 2 +20, str(KhaiValue), (255, 93,93 ))

    Load.font[10].draw_unicode(15, CenterPointY + h / 2 - 30, '좋음', (0, 0, 0))
    Load.font[10].draw_unicode(15, CenterPointY + h / 2 - 45, ' ~50 ', (0, 0, 0))

    Load.font[10].draw_unicode(125, CenterPointY + h / 2 - 30, '보통', (0, 0, 0))
    Load.font[10].draw_unicode(125, CenterPointY + h / 2 - 45, ' ~100 ', (0, 0, 0))

    Load.font[10].draw_unicode(235, CenterPointY + h / 2 - 30, '나쁨', (0, 0, 0))
    Load.font[10].draw_unicode(235, CenterPointY + h / 2 - 45, ' ~250 ', (0, 0, 0))

    Load.font[10].draw_unicode(340, CenterPointY + h / 2 - 30, ' 매우나쁨 ', (0, 0, 0))
    Load.font[10].draw_unicode(340, CenterPointY + h / 2 - 45, ' ~500 ', (0, 0, 0))

    # 시간별대기예보 그리기
    weather24H.draw()


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    pass
