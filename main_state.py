from pico2d import*
import Framework
import Load


name = "MainState"
image = Load.image
MouseX, MouseY = 0, 0


def enter():
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
        elif event.type == SDL_WINDOW_MOUSE_FOCUS:
            MouseX, MouseY = event.x, event.y
    pass


def update():
    pass


def draw():
    image["Background_Sky"].draw(image["Background_Sky"].w/2, image["Background_Sky"].h/2)
    pass





