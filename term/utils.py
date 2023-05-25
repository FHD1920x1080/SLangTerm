import ctypes
def get_windows_text_scaling():
    user32 = ctypes.windll.user32
    # DPI 스케일링 모드 가져오기
    dpi_scaling = user32.GetDpiForSystem()
    # 확대 비율 계산
    text_scaling = dpi_scaling / 96.0
    return text_scaling