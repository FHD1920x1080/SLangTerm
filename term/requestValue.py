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
        self.upkind.set(' ') # 라디오박스에 쓸거면 ''같은 빈문자열은 안되고 쓰레기 값이라도 있어야함 그래서 공백 한칸 씀
        self.state = StringVar()
        self.state.set(' ')


    def setParams(self, key, value):
        if value and value != ' ': # 값이 있으면, 공백 제거로 할 수도 있지만 이게 더 빠를듯
            self.queryParams[key] = value
        else: #
            self.queryParams.pop(key, None) # 없으면 None이 반환되는데 딱히 반환값은 필요 없음

    def set(self):
        tempParams = self.queryParams
        self.setParams('bgnde', self.bgnde.get())
        self.setParams('endde', self.endde.get())
        self.setParams('upkind', self.upkind.get())
        self.setParams('state', self.state.get())
        # 지역코드 set 추가해야함

        self.setParams('numOfRows', str(self.numOfRows))
        self.setParams('pageNo', str(self.pageNo))
    def getValue(self):
        return requests.get(url, params=self.queryParams)

