from pico2d import *
import json


def LoadFileFrom(Filepath=None):
    if not Filepath:
        return
    else:
        File = open(Filepath, 'r')

        Dic_imagepath = json.load(File)
        File.close()

        Object_list_source = {}

        test = load_image("TestFrame.png")

        for name in Dic_imagepath:
            Object_list_source[name] = load_image(Dic_imagepath[name])

        return Object_list_source


image = LoadFileFrom("Data\\Bin\\ResourcePath.json")
