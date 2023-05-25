from tkinter import StringVar
import requests
url = 'https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic'
service_key = "Bst8DsrxQ7RorD2aw2vb4FGO7mfU4MQ7yrH/SYzAN6hYr5OaDJZDV4fYUgUjGtexpTALuChYvNgqV5Uhc8+SgQ=="
class ReQuestValue:
    def __init__(self):
        self.queryParams = {'serviceKey': service_key}

        self.numOfRows = 10
        self.pageNo = 1
        self.bgnde = StringVar()
        self.endde = StringVar()
        self.upkind = StringVar()
        self.upkind.set('0') # 라이도박스에 쓸거면 빈무자열 안됨.
        self.state = StringVar()
        self.state.set('0')

    def set(self):
        if self.bgnde.get(): # 값이 있으면
            if 'bgnde' in self.queryParams: # 키가 있는지
                if self.queryParams['bgnde'] != self.bgnde.get():# 이전이랑 다른값인지
                    self.pageNo = 1 #다르면 페이지 초기화
            self.queryParams['bgnde'] = self.bgnde.get()
        else:
            if 'bgnde' in self.queryParams:
                del self.queryParams['bgnde']

        if self.endde.get():
            self.queryParams['endde'] = self.endde.get()
        if self.upkind.get() != '0':
            self.queryParams['upkind'] = self.upkind.get()
        if self.state.get() != '0':
            self.queryParams['state'] = self.state.get()

        self.queryParams['numOfRows'] = str(self.numOfRows)
        self.queryParams['pageNo'] = str(self.pageNo)
    def get(self):
        return requests.get(url, params=self.queryParams)