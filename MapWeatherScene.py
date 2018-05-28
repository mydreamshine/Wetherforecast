from pico2d import*
import Framework
import Load
from datetime import datetime
import SimpleWeatherScene

name = "MapWeatherScene"
image, font, weather, weatherSub = None, None, None, None
MouseX, MouseY = 0, 0

EnterTime = None
StackTime = 0


def enter():
    global image, font, weather, weatherSub, EnterTime, StackTime
    font = Load.font
    image = Load.image
    weather = Load.Weather
    weatherSub = Load.WeatherSub
    EnterTime = datetime.now()

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
            CenterPointX, CenterPointY = get_canvas_width()/2, 565
            x1, y1, x2, y2 = Load.GetCorners(CenterPointX, CenterPointY, width, height)
            if Load.PointInRect(x1, y1, x2, y2, MouseX,MouseY):
                Framework.change_state(SimpleWeatherScene)




    pass


def update():
    global StackTime, EnterTime
    t = datetime.now() - EnterTime
    StackTime += t.seconds
    Load.UpdateWeatherSubWithTick(StackTime)


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
    update_canvas()
    pass





