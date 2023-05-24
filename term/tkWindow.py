import requests
import xml.etree.ElementTree as ET
from tkinter import *
from animal import *

width = 1280
height = 720

url = 'https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic'
service_key = "Bst8DsrxQ7RorD2aw2vb4FGO7mfU4MQ7yrH/SYzAN6hYr5OaDJZDV4fYUgUjGtexpTALuChYvNgqV5Uhc8+SgQ=="

class TkWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry(str(width) + "x" + str(height))
        self.window.title("타이틀이름")

        self.categoryFrame = Frame(self.window)
        self.categoryFrame.pack()

        row_count = 0
        self.bgndeRequest = StringVar()
        self.enddeRequest = StringVar()
        Label(self.categoryFrame, text='검색 시작일', font=("Helvetica", 10), width=10).grid(row=row_count, column=0)
        Entry(self.categoryFrame, textvariable=self.bgndeRequest, justify=RIGHT, width=10).grid(row=row_count, column=1)
        Label(self.categoryFrame, text='검색 종료일', font=("Helvetica", 10), width=10).grid(row=row_count, column=2)
        Entry(self.categoryFrame, textvariable=self.enddeRequest, justify=RIGHT, width=10).grid(row=row_count, column=3)
        row_count += 1

        self.upkindRequest = StringVar()
        self.upkindRequest.set('0') # 빈문자열이면 전체 체크되버림
        Radiobutton(self.categoryFrame, text='전체', variable=self.upkindRequest, value='0').grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, text='개', variable=self.upkindRequest, value='417000').grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, text='고양이', variable=self.upkindRequest, value='422400').grid(row=row_count, column=2)
        Radiobutton(self.categoryFrame, text='기타', variable=self.upkindRequest, value='429900').grid(row=row_count, column=3)
        row_count += 1

        self.stateRequest = StringVar()
        self.stateRequest.set('0')
        Radiobutton(self.categoryFrame, text='전체', variable=self.stateRequest, value='0').grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, text='공고중', variable=self.stateRequest, value='notice').grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, text='보호중', variable=self.stateRequest, value='protect').grid(row=row_count, column=2)
        row_count += 1

        Button(self.categoryFrame, text='출력', command=self.printAnimalList).grid(row=row_count, column=0)

        self.mainFrame = Canvas(self.window)
        self.mainFrame.pack()
        self.animalLabelList = []
        self.animalList = []

        self.window.mainloop()

    def getRoot(self):
        self.queryParams = {'serviceKey': service_key}
        self.queryParams['numOfRows'] = '10'
        self.queryParams['pageNo'] = '1'

        # 카테고리 나누기
        if self.bgndeRequest.get():
            self.queryParams['bgnde'] = self.bgndeRequest.get()
        if self.upkindRequest.get() != '0':
            self.queryParams['upkind'] = self.upkindRequest.get()
        if self.stateRequest.get() != '0':
            self.queryParams['state'] = self.stateRequest.get()

        self.response = requests.get(url, params=self.queryParams)
        # 트라이마다 성공할 때 있고 실패할 때 있어서 거르는 작업이나 오류 메세지박스 띄워야 할듯
        self.root = ET.fromstring(self.response.text)
        print(self.response.url) # 디버깅용

    def printAnimalList(self):
        self.getRoot()

        for item in self.animalLabelList: # 무식한 방법의 삭제, 라벨 껍데기는 보관하고 내부만 바꾸는게 나을것, 그래야 격자 배치도 정갈하게 할듯
            item.destroy()
        self.animalLabelList.clear()

        self.animalList.clear()

        row_count = 0
        for item in self.root.iter("item"):
            animal = Animal()
            animal.setData(item)
            self.animalList.append(animal)
            for i, value in enumerate(animal.getData()):
                label = Label(self.mainFrame, width=20, height=1, text=value, font=("Helvetica", 10)) # 현재 무식하게 한 항목마다 라벨 만들고 있음.
                label.grid(row=row_count, column=i)
                # label.place(y=row_count*30, x=i * 300)
                self.animalLabelList.append(label)

            row_count += 1
