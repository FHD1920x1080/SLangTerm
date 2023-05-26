from tkinter import *
from animal import *


# 이름이 라벨일뿐 캔버스로 써도 되고..

# 이걸 mainFrame 오른쪽 위에 노트북으로 처리하면 될듯
class ListViewLabel:
    def __init__(self, place, font, row, column):
        self.label = Label(place, font=font, text='', height=1, bg='cyan')

    def setContent(self, string):
        # 아직은 아주 단순하게 처리, Animal 클래스 자체를 받을 수 있게 하면 될 듯
        #
        self.label['text'] = string
        pass


class GridViewLabel:
    pass


# 상세 보기 라벨, 이거 자체에 지도를
class DetaileVeiwLabel:
    pass
