from tkinter import *
from tkinter import font
from animal import *
import tkWindow


# 이름이 라벨일뿐 캔버스로 써도 되고..
# 이걸 mainFrame 오른쪽 위에 노트북으로 처리하면 될듯
class ListViewLabel:
    def __init__(self, master, font, width=20, height=20, x=0, y=0, ):
        self.canvas = Canvas(master, relief="groove", borderwidth=5, bg='cornsilk1', width=width-50, height=height)# 스크롤바 두께만큼 작게함
        master.create_window(x, y, anchor="nw", window=self.canvas)

        # self.image = None
        self.kindCd = Label(self.canvas, font=font, text='', height=1, bg='cyan')
        self.canvas.create_window(10, 10, anchor="nw", window=self.kindCd)
        self.age = Label(self.canvas, font=font, text='', height=1, bg='cyan')
        self.canvas.create_window(10, 40, anchor="nw", window=self.age)
        self.careNm = Label(self.canvas, font=font, text='', height=1, bg='cyan')
        self.canvas.create_window(10, 70, anchor="nw", window=self.careNm)
        self.careAddr = Label(self.canvas, font=font, text='', height=1, bg='cyan')
        self.canvas.create_window(10, 100, anchor="nw", window=self.careAddr)

    def setContent(self, animal):
        if animal is None:
            self.kindCd['text'] = ''
            self.age['text'] = ''
            self.careNm['text'] = ''
            self.careAddr['text'] = ''
            return

        self.kindCd['text'] = animal.kindCd
        self.age['text'] = animal.age
        self.careNm['text'] = animal.careNm
        self.careAddr['text'] = animal.careAddr


class GridViewLabel:
    pass


# 상세 보기 라벨, 이거 자체에 지도를
class DetaileVeiwLabel:
    pass
