import xml.etree.ElementTree as ET
import tkinter.ttk
from tkinter import font
from customLabel import *
from requestValue import *
from utils import *

width = 1280
height = 720
font12 = None


# 텍스트 배율 가져오기
class TkWindow:
    def __init__(self):
        global font12
        self.window = Tk()
        scaling_factor = get_windows_text_scaling()  # 윈도우 텍스트 배율 받아옴
        font12 = font.Font(size=int(12.0 / scaling_factor), family='Helvetica')  # font설정은 Tk()생성자 이후에만 할 수 있음. 불편...
        self.window.geometry(str(width) + "x" + str(height) + "+100+100")
        self.window.title("타이틀이름")
        self.window.configure(bg='light salmon')

        self.ListViewLabels = []
        self.animals = []
        self.root = None
        self.totalCount = 0  # len(self.animals)과는 다름, 페이지와 상관없이 검색한 전체 개수
        self.numOfPage = 16  # 한페이지에 표시할 수
        self.curPage = 1
        self.lastPage = 1
        self.rqValue = RequestValue(self.numOfPage)  # 페이지의 10배만큼 읽음. 100개

        self.TabBar = tkinter.ttk.Notebook(self.window)
        self.TabBar.pack(side="top", expand=True, fill="both")

        self.inquiryFrame = Frame(self.window, bg='light salmon')
        self.TabBar.add(self.inquiryFrame, text="조회")
        self.setCategoriFrame(self.inquiryFrame)
        self.setMainFrame(self.inquiryFrame)  # selectViewMode Notebook 추가 예정
        self.setPageFrame(self.inquiryFrame)

        # 상세보기 탭에 들어갈 프레임 껍데기 만들어줘야함

        self.interestsFrame = Frame(self.window)
        self.TabBar.add(self.interestsFrame, text="관심목록")

        self.setAndPrint()  # 이걸 init에서 해줘야 초기에 값이 나오는데 프로그램 실행이 느려짐
        self.window.mainloop()

    def setRoot(self):
        self.rqValue.set()
        self.response = self.rqValue.getValue()
        print(self.response.url)
        if self.response.status_code == 200:  # 성공했을때
            self.root = ET.fromstring(self.response.text)  # 루트 세팅!
            for item in self.root.iter("body"):  # body는 하나라서 반복은 한번만 함. 반복문 안쓰는법을 모름 ㅋ
                self.totalCount = int(item.findtext("totalCount"))  # 총 개수를 받아옴
                self.lastPage = (self.totalCount + self.numOfPage - 1) // self.numOfPage  # 마지막 페이지 정의
            return True
        return False  # 실패

    def setanimals(self):
        if not self.setRoot():
            print("읽는데 실패함")
            return
        self.animals.clear()
        for item in self.root.iter("item"):
            self.animals.append(Animal(item))

    def setAndPrint(self):
        self.rqValue.pageNo = 1  # 출력을 이용하면 조건을 변경하지 않았어도 첫페이지로
        self.curPage = 1
        self.setanimals()
        self.pageLabel['text'] = str(self.curPage)
        self.prevButton['state'] = 'normal'
        self.nextButton['state'] = 'normal'
        self.printListView()

    def disablePrevNext(self):
        self.prevButton['state'] = 'disable'
        self.nextButton['state'] = 'disable'

    def printListView(self):
        i = 0  # 라벨 인덱스
        curPageFirstIndex = (self.curPage - 1) % 10 * self.numOfPage
        curPageCount = min(self.numOfPage, len(self.animals) - curPageFirstIndex)
        # print(curPageFirstIndex, curPageCount, len(self.animals))
        while i < curPageCount:
            self.ListViewLabels[i].setContent(self.animals[curPageFirstIndex + i])
            i += 1
        while i < self.numOfPage:  # 페이지의 라벨 수보다 동물이 적으면 공백
            self.ListViewLabels[i].setContent(None)
            i += 1

    def prevPage(self):
        if self.curPage <= 1:
            print("첫 페이지 입니다.")
            return
        self.curPage -= 1
        if self.curPage % 10 == 0:  # 11->10, 21->20, 31->30
            self.rqValue.pageNo -= 1
            self.setanimals()
        self.pageLabel['text'] = str(self.curPage)
        self.printListView()

    def nextPage(self):
        if self.curPage >= self.lastPage:
            print("마지막 페이지 입니다.")
            return
        self.curPage += 1
        if self.curPage % 10 == 1:  # 10->11, 20->21, 30->31
            self.rqValue.pageNo += 1
            self.setanimals()
        self.pageLabel['text'] = str(self.curPage)
        self.printListView()

    def setCategoriFrame(self, master):
        self.categoryFrame = Frame(master)
        self.categoryFrame.pack()

        row_count = 0
        Label(self.categoryFrame, font=font12, text='검색 시작일', width=10).grid(row=row_count, column=0)
        Entry(self.categoryFrame, font=font12, textvariable=self.rqValue.bgnde, justify=RIGHT, width=10).grid(
            row=row_count, column=1)
        Label(self.categoryFrame, font=font12, text='검색 종료일', width=10).grid(row=row_count, column=2)
        Entry(self.categoryFrame, font=font12, textvariable=self.rqValue.endde, justify=RIGHT, width=10).grid(
            row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, font=font12, text='전체', variable=self.rqValue.upkind, value=' ',
                    command=self.disablePrevNext).grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, font=font12, text='개', variable=self.rqValue.upkind, value='417000',
                    command=self.disablePrevNext).grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, font=font12, text='고양이', variable=self.rqValue.upkind, value='422400',
                    command=self.disablePrevNext).grid(row=row_count, column=2)
        Radiobutton(self.categoryFrame, font=font12, text='기타', variable=self.rqValue.upkind, value='429900',
                    command=self.disablePrevNext).grid(row=row_count, column=3)
        row_count += 1

        Radiobutton(self.categoryFrame, font=font12, text='전체', variable=self.rqValue.state, value=' ',
                    command=self.disablePrevNext).grid(row=row_count, column=0)
        Radiobutton(self.categoryFrame, font=font12, text='공고중', variable=self.rqValue.state, value='notice',
                    command=self.disablePrevNext).grid(row=row_count, column=1)
        Radiobutton(self.categoryFrame, font=font12, text='보호중', variable=self.rqValue.state, value='protect',
                    command=self.disablePrevNext).grid(row=row_count, column=2)
        row_count += 1

        self.setAndPrintButton = Button(self.categoryFrame, font=font12, text='출력', command=self.setAndPrint)
        self.setAndPrintButton.grid(row=row_count, column=0)

        return self.categoryFrame

    def setMainFrame(self, master):
        self.mainScrollbar = Scrollbar(master, orient="vertical")
        self.mainScrollbar.pack(side="right", fill="y")
        # scrollbar 추가를 위해서 canvas 사용
        self.mainFrame = Canvas(master, width=width, bg='light salmon',
                                 scrollregion=(0, 0, 0, 400 * self.numOfPage + 12),
                                 yscrollcommand=self.mainScrollbar.set)
        self.mainScrollbar.config(command=self.mainFrame.yview)
        self.mainFrame.pack(expand=True, side="top", fill="both")

        # canvas내에 create_window를 해야 scroll이 가능 일일히 좌표 계산을 해야함
        for i in range(self.numOfPage):
            label = ListViewLabel(self.mainFrame, font12, width=width, height=400, x=0, y=i * 400)
            self.ListViewLabels.append(label)

        return self.mainFrame

    def setPageFrame(self, master):
        self.pageFrame = Frame(master)
        self.pageFrame.pack(side="bottom")
        self.prevButton = Button(self.pageFrame, font=font12, text='이전', command=self.prevPage)
        self.prevButton.grid(row=0, column=0)
        self.pageLabel = Label(self.pageFrame, font=font12, text=str(self.curPage), width=8)
        self.pageLabel.grid(row=0, column=1)
        self.nextButton = Button(self.pageFrame, font=font12, text='다음', command=self.nextPage)
        self.nextButton.grid(row=0, column=2)

        return self.pageFrame
