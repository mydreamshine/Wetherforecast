from pico2d import*
import Framework
import Load

name = "MainState"
image = None
MouseX, MouseY = 0, 0
test = None


def enter():
    global image
    image = Load.image

    global test
    test = load_font('Data\\Font\\malgun.TTF', 56)
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
    pass


def update():
    pass


def Scene_draw():
    global image
    global test
    image['Background_Sky'].draw(get_canvas_width()/2, get_canvas_height()/2)
    # test.draw(get_canvas_width()/2, get_canvas_height()/1.5, str(14.5),)


def draw():
    clear_canvas()
    Scene_draw()
    update_canvas()
    delay(0.01)
    pass





