import requests
import xml.etree.ElementTree as ET
import tkinter
url = 'https://apis.data.go.kr/1543061/abandonmentPublicSrvc/abandonmentPublic'
service_key = "Bst8DsrxQ7RorD2aw2vb4FGO7mfU4MQ7yrH/SYzAN6hYr5OaDJZDV4fYUgUjGtexpTALuChYvNgqV5Uhc8+SgQ=="
queryParams = {'serviceKey': service_key, 'upkind':'417000', 'pageNo': '1', 'numOfRows': '20'}
response = requests.get(url, params=queryParams)
print(response.url)
root = ET.fromstring(response.text)
window = tkinter.Tk()
window.title("뭐시기")

frame = tkinter.Frame(window)
frame.pack()

header = ["kindCd", "age", "careNm", "careAddr"]

for i, col_name in enumerate(header):
    label = tkinter.Label(frame, text=col_name, font=("Helvetica", 14, "bold"))
    label.grid(row=0, column=i)

row_count = 1
for item in root.iter("item"):
    kindCd = item.findtext("kindCd")
    age = item.findtext("age")
    careNm = item.findtext("careNm")
    careAddr = item.findtext("careAddr")

    data = [kindCd, age, careNm, careAddr]
    for i, value in enumerate(data):
        label = tkinter.Label(frame, text=value, font=("Helvetica", 12))
        label.grid(row=row_count, column=i)

    row_count += 1

window.mainloop()