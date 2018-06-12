from pico2d import*
import Framework
import Load
import MapWeatherScene
import DetailWeatherScene

name = "SimpleWeatherScene"
city = "서울"
image, font, weather = None, None, None
MouseX, MouseY = 0, 0


def enter():
    global image, font, weather
    font = Load.font
    image = Load.image
    weather = Load.Weather
    weather[city].Update(city)
    pass


def exit():
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global MouseX, MouseY, city
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

            info_tmp = weather[city].getTemperature()
            if not info_tmp:
                info_tmp = '측정정보없음'
            else:
                info_tmp = str(info_tmp) + '˚'
            w, h = font[62].getpixelSize_unicode(info_tmp)
            x2, y2 = get_canvas_width() / 2 + w / 2, get_canvas_height() / 1.3 + h / 2

            info_PM10 = '    미세먼지: '
            if weather[city].getPM10State() == '측정정보없음':
                info_PM10 = '측정정보없음'
            else:
                info_PM10 = info_PM10 + weather[city].getPM10State() + '    '
            w, h = font[26].getpixelSize_unicode(info_PM10)
            x1, y1 = get_canvas_width() / 2 - w / 2, get_canvas_height() / 2.7 - h / 2

            if Load.PointInRect(x1, y1, x2, y2, MouseX, MouseY):
                DetailWeatherScene.city = city
                Framework.change_state(DetailWeatherScene)

            info_Address = weather[city].getAdress()
            if not info_Address:
                info_Address = '측정정보없음'
            else:
                info_Address = ' ' + info_Address + '시  '
            width, height = font[36].getpixelSize_unicode(info_Address)
            CenterPointX, CenterPointY = get_canvas_width() / 2 - width / 2, get_canvas_height() / 4 + height / 2
            x1, y1, x2, y2 = Load.GetCorners(CenterPointX, CenterPointY, width, height)
            if Load.PointInRect(x1, y1, x2, y2, MouseX, MouseY):
                Framework.change_state(MapWeatherScene)

            width2, height2 = font[36].getpixelSize_unicode(info_Address)
            CenterPointX2, CenterPointY2 = get_canvas_width() / 2 - width2 / 2, get_canvas_height() / 4 + height2 / 2
            x11, y11, x22, y22 = Load.GetCorners(CenterPointX2, CenterPointY2, width2, height2)
            if Load.PointInRect(x11, y11, x22, y22, MouseX, MouseY):
                Framework.change_state(MapWeatherScene)

            buttonW, buttonH = image['RefreshButton'].w, image['RefreshButton'].h
            buttonX, buttonY = get_canvas_width() / 2, get_canvas_height() / 10.5
            Buttonx1, Buttony1, Buttonx2, Buttony2 = Load.GetCorners(buttonX, buttonY, buttonW, buttonH)
            if Load.PointInRect(Buttonx1, Buttony1, Buttonx2, Buttony2, MouseX, MouseY):
                weather[city].Update(city, OffsetDay=1)



    pass


def update():
    pass


def Scene_draw():
    global image, font, weather

    # 배경 그리기
    info_sky = weather[city].getSkyState()
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 2
    if info_sky == '측정정보없음' or info_sky == '맑음' or info_sky == '구름 조금':
        if 6 < int(weather[city].getDay().strftime("%H")) < 18:
            image['Background_Sky'].draw(CenterPointX, CenterPointY)
        else:
            image['Background_Blue'].draw(CenterPointX, CenterPointY)
    else:
        image['Background_Black'].draw(CenterPointX, CenterPointY)

    # 현재 온도 그리기
    info_tmp = weather[city].getTemperature()
    if not info_tmp:
        info_tmp = '측정정보없음'
    else:
        info_tmp = str(info_tmp) + '˚'

    w, h = font[62].getpixelSize_unicode(info_tmp)
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 1.3 + h / 2
    font[62].draw_unicode(get_canvas_width() / 2 - w / 2, get_canvas_height() / 1.3 + h / 2, info_tmp, (255, 255, 255))

    X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, w, h)
    if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
        draw_rectangle(X1, Y1, X2, Y2)

    # 기상 정보 이미지 출력
    info_pty = weather[city].getPtyState()
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 1.7
    if info_pty == '측정정보없음' or info_pty == '없음':
        if info_sky == '구름많음' or info_sky == '흐림':
            image['Cloud'].draw(CenterPointX, CenterPointY)
            X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['Cloud'].w, image['Cloud'].h)
            if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
                draw_rectangle(X1, Y1, X2, Y2)
        elif 6 < int(weather[city].getDay().strftime("%H")) < 18:
            image['Sun'].draw(CenterPointX, CenterPointY)
            X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['Sun'].w, image['Sun'].h)
            if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
                draw_rectangle(X1, Y1, X2, Y2)
        else:
            image['Moon'].draw(CenterPointX, CenterPointY)
            X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['Moon'].w, image['Moon'].h)
            if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
                draw_rectangle(X1, Y1, X2, Y2)
    else:
        if info_pty == '비' or info_pty == '비/눈':
            image['Rain'].draw(CenterPointX, CenterPointY)
            X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['Rain'].w, image['Rain'].h)
            if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
                draw_rectangle(X1, Y1, X2, Y2)
        else:
            image['Snow'].draw(CenterPointX, CenterPointY)
            X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['Snow'].w, image['Snow'].h)
            if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
                draw_rectangle(X1, Y1, X2, Y2)

    # 미세먼지 정보 출력
    info_PM10 = '    미세먼지: '
    if weather[city].getPM10State() == '측정정보없음':
        info_PM10 = '측정정보없음'
    else:
        info_PM10 = info_PM10 + weather[city].getPM10State() + '    '
    w, h = font[26].getpixelSize_unicode(info_PM10)
    CenterPointX, CenterPointY = get_canvas_width()/2 - w/2, get_canvas_height()/2.7 + h/2
    font[26].draw_unicode(CenterPointX, CenterPointY, info_PM10, (255, 255, 255))
    X1, Y1, X2, Y2 = Load.GetCorners(get_canvas_width()/2, CenterPointY, w, h)
    if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
        draw_rectangle(X1, Y1, X2, Y2)

    # 위치 정보 출력
    info_Address = weather[city].getAdress()
    if not info_Address:
        info_Address = '측정정보없음'
    else:
        info_Address = ' ' + info_Address + '시  '
    w, h = font[36].getpixelSize_unicode(info_Address)
    CenterPointX, CenterPointY = get_canvas_width() / 2 - w / 2, get_canvas_height() / 4 + h / 2
    font[36].draw_unicode(CenterPointX, CenterPointY, info_Address, (255, 255, 255))
    X1, Y1, X2, Y2 = Load.GetCorners(get_canvas_width() / 2, CenterPointY, w, h)
    if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
        draw_rectangle(X1, Y1, X2, Y2)

    # 날짜 정보 출력
    info_Day = weather[city].getDay()
    AMPM = '오전' if info_Day.strftime("%p") == 'AM' else '오후'
    str_update = '업데이트 ' + info_Day.strftime("%m/%d") + ' ' + AMPM + ' ' + info_Day.strftime("%I:%M")
    w, h = font[21].getpixelSize_unicode(str_update)
    font[21].draw_unicode(get_canvas_width() / 2 - w / 2, get_canvas_height() / 5.8 + h / 2, str_update, (255, 255, 255))

    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 10.5
    image['RefreshButton'].draw(CenterPointX, CenterPointY)
    X1, Y1, X2, Y2 = Load.GetCorners(CenterPointX, CenterPointY, image['RefreshButton'].w, image['RefreshButton'].h)
    if Load.PointInRect(X1, Y1, X2, Y2, MouseX, MouseY):
        draw_rectangle(X1, Y1, X2, Y2)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    pass





