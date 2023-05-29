from tkinter import *
from tkinter import font
from animal import *
import tkWindow

#이미지 출력을 위한 모듈
from PIL import ImageTk, Image
import requests
import io


# 이름이 라벨일뿐 캔버스로 써도 되고..
# 이걸 mainFrame 오른쪽 위에 노트북으로 처리하면 될듯
class SimpleViewCanvas:
    errorMsg = None  # 오류메시지
    reqNo = None  # 요청번호
    resultCode = None  # 결과코드
    resultMsg = None  # 결과메세지
    desertionNo = None  # 유기번호
    filename = None  # 썸네일 이미지
    happenDt = None  # 접수일
    happenPlace = None  # 발견장소
    kindCd = None  # 품종
    colorCd = None  # 색상
    age = None  # 나이
    weight = None  # 체중
    noticeNo = None  # 공고번호
    noticeSdt = None  # 공고시작일
    noticeEdt = None  # 공고종료일
    popfile = None  # 고화질 Image
    processState = None  # 상태
    sexCd = None  # 성별
    neuterYn = None  # 중성화여부
    specialMark = None  # 특징
    careNm = None  # 보호소이름
    careTel = None  # 보호소전화번호
    careAddr = None  # 보호장소
    orgNm = None  # 관할기관
    chargeNm = None  # 담당자
    officetel = None  # 담당자연락처
    noticeComment = None  # 특이사항
    numOfRows = None  # 한 페이지 결과 수
    pageNo = None  # 페이지 번호
    totalCount = None  # 전체 결과 수
    image = None
    def __init__(self, master, font, width=0, height=0, x=0, y=0, ):
        self.canvas = Canvas(master, relief="groove", borderwidth=10, bg='lightgray', width=width - 40,
                             height=height)  # 스크롤바 두께만큼 작게함
        master.create_window(x, y, anchor="nw", window=self.canvas)
    def clearContent(self):
        self.kindCd['text'] = ''
        self.age['text'] = ''
        self.careNm['text'] = ''
        self.careAddr['text'] = ''

    def setContent(self, animal):
        self.kindCd['text'] = animal.kindCd
        self.age['text'] = animal.age
        self.careNm['text'] = animal.careNm
        self.careAddr['text'] = animal.careAddr

    def clearImage(self):
        self.image.configure(image='')

    def setImage(self, animal, ordPage, curPage):
        imageGet = requests.get(animal.filename, stream=True)
        imageSet = imageGet.content
        img = Image.open(io.BytesIO(imageSet))
        img = img.resize((200, 200), Image.ANTIALIAS)

        if ordPage != curPage: # 위 과정 거친 이후에 이미 다른페이지 와버렸으면 적용하면 안됨. 멀티쓰레딩 문제.
            return False
        imgTk = ImageTk.PhotoImage(img)
        self.image.configure(image=imgTk)
        self.image.image = imgTk
        return True

    def detailPage(self):
        print("detail")
        pass

class ListViewCanvas(SimpleViewCanvas):
    def __init__(self, master, font, width=0, height=0, x=0, y=0, ):
        self.canvas = Canvas(master, relief="groove", borderwidth=5, bg='cornsilk1', width=width-40, height=height)# 스크롤바 두께만큼 작게함
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
        self.image = Label(self.canvas, image='')
        self.canvas.create_window(10, 130, anchor="nw",window=self.image)

        #사진 클릭으로 동물에 대한 자세한 출력
        self.image.bind("<Button-1>", lambda event: self.detailPage())

class GridViewCanvas(SimpleViewCanvas):
    pass

class PopUpCanvas(SimpleViewCanvas):
    def __init__(self, master, font, width=0, height=0, x=0, y=0, ):
        self.canvas = Canvas(master, relief="groove", borderwidth=10, bg='lightgray', width=width - 40,
                             height=height)  # 스크롤바 두께만큼 작게함
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
        self.image = Label(self.canvas, image='')
        self.canvas.create_window(10, 130, anchor="nw", window=self.image)

        # 사진 클릭으로 동물에 대한 자세한 출력
        self.image.bind("<Button-1>", lambda event: self.detailPage())

# 상세 보기 라벨, 이거 자체에 지도를
class DetaileVeiwCanvas(SimpleViewCanvas):
    pass
