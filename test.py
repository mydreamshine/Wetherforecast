# tkinter 모듈에 있는 모든 함수를 포함
from tkinter import *


def DollorToWon():
    dollor = float(e1.get())
    e2.insert(0, str(dollor * 1200))


def WonToDollor():
    Won = float(e2.get())
    e1.insert(0, str(Won / 1200))


window = Tk()

l1 = Label(window, text="달러")
l2 = Label(window, text="원")
l1.grid(row=0, column=0)
l2.grid(row=1, column=0)
e1 = Entry(window)
e2 = Entry(window)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
b1 = Button(window, text="달러->원", command=DollorToWon)
b2 = Button(window, text="원->달러", command=WonToDollor)
b1.grid(row=2, column=0)
b2.grid(row=2, column=1)
photo = PhotoImage(file="TestFrame.png")
l3 = Label(window, image=photo)
l3.grid(row=3, column=0)

window.mainloop()


'''
화면에서 위젯의 배치를 담당하는 객체
압축(pack) 배치 관리자
격자(grid) 배치 관리자
절대(place) 배치 관리자
'''