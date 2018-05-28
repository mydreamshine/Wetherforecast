from pico2d import *
import json
from WeatherAPI import WeatherAPI


def LoadImageFrom(Filepath=None):
    if not Filepath:
        return
    else:
        File = open(Filepath, 'r')

        Dic_imagepath = json.load(File)
        File.close()

        Object_dic_source = dict()

        for name in Dic_imagepath:
            Object_dic_source[name] = load_image(Dic_imagepath[name])

        return Object_dic_source


def LoadFontFrom(Filepath=None):
    if not Filepath:
        return
    else:
        Object_dic_source = dict()
        Object_dic_source[9] = load_font(Filepath, int(9*1.3))
        Object_dic_source[10] = load_font(Filepath, int(10*1.3))
        Object_dic_source[13] = load_font(Filepath, int(13*.13))
        Object_dic_source[18] = load_font(Filepath, int(18*1.3))
        Object_dic_source[21] = load_font(Filepath, int(21*1.3))
        Object_dic_source[26] = load_font(Filepath, int(26*1.3))
        Object_dic_source[36] = load_font(Filepath, int(36*1.3))
        Object_dic_source[55] = load_font(Filepath, int(55*1.3))
        Object_dic_source[62] = load_font(Filepath, int(62*1.3))

        return Object_dic_source


def CreateEmptyWeather():
    Object_dic_source = dict()

    for index in WeatherAPI.Addr.values():
        Object_dic_source[index] = WeatherAPI.WeatherInformation()

    return Object_dic_source


image = None
font = None
Weather = None


def PrePareResource():
    global image, font, Weather
    image = LoadImageFrom("Data\\Bin\\ResourcePath.json")
    font = LoadFontFrom("Data\\Font\\malgun.ttf")
    Weather = CreateEmptyWeather()


def ReleaseResource():
    global image, font, Weather
    if image:
        image.clear()
    if font:
        font.clear()
    if Weather:
        Weather.clear()