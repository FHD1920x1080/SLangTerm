# 잡스러운 함수들 모아두는 파일
import ctypes
import webbrowser


def get_windows_text_scaling():
    user32 = ctypes.windll.user32
    # DPI 스케일링 모드 가져오기
    dpi_scaling = user32.GetDpiForSystem()
    # 확대 비율 계산
    text_scaling = dpi_scaling / 96.0
    return text_scaling


def webOpen(url):
    webbrowser.open(url)


def bring_to_front(widget):
    widget.lift()

def scroll_canvas(event, canvas):
    if event.delta > 0:
        canvas.yview_scroll(-1, "units")
    else:
        canvas.yview_scroll(1, "units")

def on_configure(event, canvas):
    # 스크롤바의 길이를 콘텐츠에 맞게 조절
    canvas.config(scrollregion=canvas.bbox('all'))