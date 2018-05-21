from pico2d import *
import json


def LoadImageFrom(Filepath=None):
    if not Filepath:
        return
    else:
        File = open(Filepath, 'r')

        Dic_imagepath = json.load(File)
        File.close()

        Object_list_source = {}

        for name in Dic_imagepath:
            Object_list_source[name] = load_image(Dic_imagepath[name])

        return Object_list_source


image = None


def ReleaseResource():
    global image
    if image:
        image.clear()
