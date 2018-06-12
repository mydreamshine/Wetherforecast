from pico2d import*
import Framework
import Load
from datetime import datetime
import SimpleWeatherScene
from WeatherAPI import WeatherAPI

name = "MapWeatherScene"
image, font, weather, weatherSub = None, None, None, None
MouseX, MouseY = 0, 0

FadeAlpha = 0.0
ChangeScene = None
EnterScene = True

ChangeCity = None

EnterTime = None
StackTime = 0


def enter():
    global image, font, weather, weatherSub, EnterTime, StackTime
    global FadeAlpha, ChangeScene, EnterScene, ChangeCity
    font = Load.font
    image = Load.image
    weather = Load.Weather
    weatherSub = Load.WeatherSub
    EnterTime = datetime.now()

    FadeAlpha = 1.0
    ChangeScene = None
    EnterScene = True
    ChangeCity = None

    t = datetime.now() - EnterTime
    StackTime += t.seconds
    Load.UpdateWeatherSubWithTick(StackTime,True)

    pass


def exit():
    pass


def pause():
    pass


def resume():
    pass


def handle_events():
    global MouseX, MouseY, ChangeCity, ChangeScene
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
            CenterPointX, CenterPointY = get_canvas_width()/2, 565
            x1, y1, x2, y2 = Load.GetCorners(CenterPointX, CenterPointY, width, height)
            if Load.PointInRect(x1, y1, x2, y2, MouseX,MouseY):
                ChangeScene = SimpleWeatherScene.name

            w, h = image["Background_RegionLayout"].w,image["Background_RegionLayout"].h
            for weather_info in Load.WeatherSub.values():
                x11, y11, x22, y22 = Load.GetCorners(weather_info.x, weather_info.y, w, h)
                if Load.PointInRect(x11, y11, x22, y22, MouseX, MouseY):
                    ChangeCity = weather_info.city
                    ChangeScene = SimpleWeatherScene.name
    pass


def update():
    global StackTime, EnterTime
    t = datetime.now() - EnterTime
    StackTime += t.seconds
    Load.UpdateWeatherSubWithTick(StackTime)


def Scene_Fade_draw():
    global image, FadeAlpha, ChangeScene, EnterScene, ChangeCity

    if EnterScene or ChangeScene is not None:
        if EnterScene:
            FadeAlpha -= 0.1
            if FadeAlpha < 0.0: FadeAlpha = 0.0
        elif ChangeScene is not None:
            FadeAlpha += 0.1
            if FadeAlpha > 1.0: FadeAlpha = 1.0
        image['Fade_Layout'].opacify(FadeAlpha)
        image['Fade_Layout'].draw(get_canvas_width()/2, get_canvas_height()/2)

    if ChangeScene is not None and FadeAlpha is 1.0:
        if ChangeScene == SimpleWeatherScene.name:
            if ChangeCity is not None:
                SimpleWeatherScene.city = ChangeCity
            Framework.change_state(SimpleWeatherScene)
    elif EnterScene and FadeAlpha is 0.0: EnterScene = False
    pass


def Scene_draw():
    global image, weatherSub
    image["Background_Map_Korea"].draw(get_canvas_width() / 2, get_canvas_height() / 2)
    a = " 간편대기 "
    w, h = Load.font[18].getpixelSize_unicode(a)
    Load.font[18].draw_unicode(get_canvas_width() / 2 - w / 2, 550 + h / 2, a, (124, 124, 124))
    # print(MouseX,MouseY)
    for weatherInfo in weatherSub.values():
        weatherInfo.draw()
    image["MainButton_Green"].draw(get_canvas_width()/2, 565)


def draw():
    clear_canvas()
    Scene_draw()
    Scene_Fade_draw()
    update_canvas()
    pass





