import requests
import xml.etree.ElementTree as ET
from tkinter import *
from animal import *
from requestValue import *

width = 1280
height = 720

class TkWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry(str(width) + "x" + str(height))
        self.window.title("타이틀이름")

        self.animalLabelList = []
        self.animalList = []

        self.categoryFrame = Frame(self.window)
        self.categoryFrame.pack()

        self.rqValue = ReQuestValue()
        row_count = 0
        Label(self.categoryFrame, text='검색 시작일', font=("Helvetica", 10), width=10).grid(row=row_count, column=0)
        Entry(self.categoryFrame, textvariable=self.rqValue.bgnde, justify=RIGHT, width=10).grid(row=row_count, column=1)
        Label(self.categoryFrame, text='검색 종료일', font=("Helvetica", 10), width=10).grid(row=row_count, column=2)
        Entry(self.categoryFrame, textvariable=self.rqValue.endde, justify=RIGHT, width=10).grid(row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, text='전체', variable=self.rqValue.upkind, value='0').grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, text='개', variable=self.rqValue.upkind, value='417000').grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, text='고양이', variable=self.rqValue.upkind, value='422400').grid(row=row_count, column=2)
        Radiobutton(self.categoryFrame, text='기타', variable=self.rqValue.upkind, value='429900').grid(row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, text='전체', variable=self.rqValue.state, value='0').grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, text='공고중', variable=self.rqValue.state, value='notice').grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, text='보호중', variable=self.rqValue.state, value='protect').grid(row=row_count, column=2)
        row_count += 1

        Button(self.categoryFrame, text='출력', command=self.printAnimalList).grid(row=row_count, column=0)

        self.mainFrame = Canvas(self.window)
        self.mainFrame.pack()
        
        
        self.pageFrame = Frame(self.window)
        self.pageFrame.pack()
        Button(self.pageFrame, text='이전', command=self.prevPage).grid(row=0, column=0)
        Button(self.pageFrame, text='다음', command=self.nextPage).grid(row=0, column=1)


        self.printAnimalList()
        self.window.mainloop()

    def setRoot(self):
        self.rqValue.set()

        self.response = self.rqValue.get()
        if self.response.status_code == 200: # 성공했을때
            self.root = ET.fromstring(self.response.text)
            return True
        return False
    def SetAnimalList(self):
        if not self.setRoot():
            print("읽는데 실패함")
            return
        print("성공")
        self.animalList.clear()
        for item in self.root.iter("item"):
            animal = Animal()
            animal.setData(item)
            self.animalList.append(animal)

    def printAnimalList(self):
        self.SetAnimalList()

        for item in self.animalLabelList: # 무식한 방법의 삭제, 라벨 껍데기는 보관하고 내부만 바꾸는게 나을것, 그래야 격자 배치도 정갈하게 할듯
            item.destroy()
        self.animalLabelList.clear()

        row_count = 0
        for item in self.animalList:
            label = Label(self.mainFrame, height=1, text=item.getSimpleData(), font=("Helvetica", 10))
            label.grid(row=row_count, column=0)
            # 라벨이랑 그리드를 조합하면 왼쪽 정렬이 안되고 중앙정렬이라서 크기가 다르면 들쭐날쭉하게 나옴
            # 지금 출력 방식은 못생기게 나오니까 라벨을 관리하고 안에 각 요소들을 배치하는 클래스를 만들어 쓰든가 해야할듯
            self.animalLabelList.append(label)
            row_count += 1

    def prevPage(self):
        self.rqValue.pageNo = max(1, self.rqValue.pageNo-1)
        self.printAnimalList()
    def nextPage(self):
        self.rqValue.pageNo += 1
        self.printAnimalList()