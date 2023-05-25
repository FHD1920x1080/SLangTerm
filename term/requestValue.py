from tkinter import StringVar
import requests
url = 'http://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic'
service_key = "Bst8DsrxQ7RorD2aw2vb4FGO7mfU4MQ7yrH/SYzAN6hYr5OaDJZDV4fYUgUjGtexpTALuChYvNgqV5Uhc8+SgQ=="
class RequestValue:
    def __init__(self, numOfPage):
        self.numOfRows = 10 * numOfPage
        self.pageNo = 1
        self.queryParams = {'serviceKey': service_key, 'numOfRows': str(self.numOfRows), 'pageNo': str(self.pageNo)}

        self.bgnde = StringVar()
        self.endde = StringVar()
        self.upkind = StringVar()
        self.upkind.set('0') # 라디오박스에 쓸거면 빈무자열 안됨.
        self.state = StringVar()
        self.state.set('0')


    def setParams(self, key, value):
        if key in self.queryParams: # 키가 있는지
            if value:  # 값이 있으면
                if self.queryParams[key] != value:# 이전이랑 다른값인지 같으면 수정 안함
                    self.queryParams[key] = value
                    self.pageNo = 1 #다르면 페이지 초기화
            else: # 없으면 삭제하고 페이지 초기화
                del self.queryParams[key]
                self.pageNo = 1
        else:
            if value:
                self.queryParams[key] = value
                self.pageNo = 1  # 다르면 페이지 초기화
    def setParamsRadio(self, key, value):
        if key in self.queryParams: # 키가 있는지
            if value != '0':  # 값이 있으면
                if self.queryParams[key] != value:# 이전이랑 다른값인지 같으면 수정 안함
                    self.queryParams[key] = value
                    self.pageNo = 1 #다르면 페이지 초기화
            else: # 없으면 삭제하고 페이지 초기화
                del self.queryParams[key]
                self.pageNo = 1
        else:
            if value != '0':  # 값이 있으면
                self.queryParams[key] = value
                self.pageNo = 1  # 다르면 페이지 초기화

    def set(self):
        self.setParams('bgnde', self.bgnde.get())
        self.setParams('endde', self.endde.get())
        self.setParamsRadio('upkind', self.upkind.get())
        self.setParamsRadio('state', self.state.get())

        self.queryParams['numOfRows'] = str(self.numOfRows)
        self.queryParams['pageNo'] = str(self.pageNo)
    def getValue(self):
        return requests.get(url, params=self.queryParams)