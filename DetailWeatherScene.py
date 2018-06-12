from pico2d import*
import Framework
import Load
import MapWeatherScene

name = "DetailWeatherScene"
image, font, weather, weather24H = None, None, None, None
MouseX, MouseY = 0, 0
city = "시흥"


def enter():
    global image, font, weather, weather24H
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

    pass


def update():
    pass


def Scene_draw():
    global image, font, weather, weather24H

    # 배경 그리기
    CenterPointX, CenterPointY = get_canvas_width() / 2, get_canvas_height() / 2
    image['Background_White'].draw(CenterPointX, CenterPointY)

    # 통합 대기 정보 그리기
    #####################
    #                   #
    #####################

    # 시간별대기예보 그리기
    weather24H.draw()



def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    pass





