import xml.etree.ElementTree as ET
from tkinter import font
from customLabel import *
from requestValue import *
from utils import *

width = 1280
height = 720
# 텍스트 배율 가져오기
class TkWindow:
    def __init__(self):
        self.window = Tk()
        self.window.geometry(str(width) + "x" + str(height))
        self.window.title("타이틀이름")
        scaling_factor = get_windows_text_scaling()#윈도우 텍스트 배율 받아옴
        font1 = font.Font(size=int(12.0/scaling_factor), family='Helvetica')

        self.ListViewLabels = []
        self.animals = []
        self.totalCount = 0 # len(self.animals)과는 다름, 페이지와 상관없이 검색한 전체 개수
        self.numOfPage = 16 # 한페이지에 표시할 수
        self.curPage = 1
        self.lastPage = 1
        self.rqValue = RequestValue(self.numOfPage) # 페이지의 10배만큼 읽음. 100개

        self.categoryFrame = Frame(self.window)
        self.categoryFrame.pack()

        row_count = 0
        Label(self.categoryFrame, font=font1, text='검색 시작일', width=10).grid(row=row_count, column=0)
        Entry(self.categoryFrame, font=font1, textvariable=self.rqValue.bgnde, justify=RIGHT, width=10).grid(row=row_count, column=1)
        Label(self.categoryFrame, font=font1, text='검색 종료일', width=10).grid(row=row_count, column=2)
        Entry(self.categoryFrame, font=font1, textvariable=self.rqValue.endde, justify=RIGHT, width=10).grid(row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, font=font1, text='전체', variable=self.rqValue.upkind, value='0', command=self.disablePrevNext).grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, font=font1, text='개', variable=self.rqValue.upkind, value='417000', command=self.disablePrevNext).grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, font=font1, text='고양이', variable=self.rqValue.upkind, value='422400', command=self.disablePrevNext).grid(row=row_count, column=2)
        Radiobutton(self.categoryFrame, font=font1, text='기타', variable=self.rqValue.upkind, value='429900', command=self.disablePrevNext).grid(row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, font=font1, text='전체', variable=self.rqValue.state, value='0', command=self.disablePrevNext).grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, font=font1, text='공고중', variable=self.rqValue.state, value='notice', command=self.disablePrevNext).grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, font=font1, text='보호중', variable=self.rqValue.state, value='protect', command=self.disablePrevNext).grid(row=row_count, column=2)
        row_count += 1

        self.setAndPrintButton = Button(self.categoryFrame, font=font1, text='출력', command=self.setAndPrint)
        self.setAndPrintButton.grid(row=row_count, column=0)

        self.mainFrame = Canvas(self.window)
        self.mainFrame.pack()
        
        
        self.pageFrame = Frame(self.window)
        self.pageFrame.pack()
        self.prevButton = Button(self.pageFrame, font=font1, text='이전', command=self.prevPage)
        self.prevButton.grid(row=0, column=0)
        self.pageLabel = Label(self.pageFrame, font=font1, text=str(self.curPage), width=8)
        self.pageLabel.grid(row=0, column=1)
        self.nextButton = Button(self.pageFrame, font=font1, text='다음', command=self.nextPage)
        self.nextButton.grid(row=0, column=2)

        for i in range(self.numOfPage):
            label = Label(self.mainFrame, font=font1, text='', height=1)
            self.ListViewLabels.append(ListViewLabel(self.mainFrame, font1, i, 0))

        #self.setAndPrint() 이걸 하면 초기에 값이 나오는데 프로그램 실행이 느려짐
        self.window.mainloop()

    def setRoot(self):
        self.rqValue.set()
        self.response = self.rqValue.getValue()
        print(self.response.url)
        if self.response.status_code == 200: # 성공했을때
            self.root = ET.fromstring(self.response.text) # 루트 세팅!
            for item in self.root.iter("body"): # body는 하나라서 반복은 한번만 함. 반복문 안쓰는법을 모름 ㅋ
                self.totalCount = int(item.findtext("totalCount")) # 총 개수를 받아옴
                self.lastPage = (self.totalCount + self.numOfPage - 1) // self.numOfPage # 마지막 페이지 정의
            return True
        return False # 실패

    def setanimals(self):
        if not self.setRoot():
            print("읽는데 실패함")
            return
        self.animals.clear()
        for item in self.root.iter("item"):
            self.animals.append(Animal(item))

    def setAndPrint(self):
        self.setanimals()
        self.curPage = 1
        self.pageLabel['text'] = str(self.curPage)
        self.prevButton['state'] = 'normal'
        self.nextButton['state'] = 'normal'
        self.printListView()

    def disablePrevNext(self):
        self.prevButton['state'] = 'disable'
        self.nextButton['state'] = 'disable'

    def printListView(self):
        i = 0 # 라벨 인덱스
        curPageFirstIndex = (self.curPage - 1) % 10 * self.numOfPage
        curPageCount = min(self.numOfPage, len(self.animals)-curPageFirstIndex)
        #print(curPageFirstIndex, curPageCount, len(self.animals))
        while i < curPageCount:
            self.ListViewLabels[i].setContent(self.animals[curPageFirstIndex + i].getSimpleData())
            i += 1
        while i < self.numOfPage: # 페이지의 라벨 수보다 동물이 적으면 공백
            self.ListViewLabels[i].setContent('')
            i += 1

    def prevPage(self):
        if self.curPage <= 1:
            print("첫 페이지 입니다.")
            return
        self.curPage -= 1
        if self.curPage % 10 == 0: # 11->10, 21->20, 31->30
            self.rqValue.pageNo -= 1
            self.setanimals()
        self.pageLabel['text'] = str(self.curPage)
        self.printListView()
    def nextPage(self):
        if self.curPage >= self.lastPage:
            print("마지막 페이지 입니다.")
            return
        self.curPage += 1
        if self.curPage % 10 == 1: # 10->11, 20->21, 30->31
            self.rqValue.pageNo += 1
            self.setanimals()
        self.pageLabel['text'] = str(self.curPage)
        self.printListView()