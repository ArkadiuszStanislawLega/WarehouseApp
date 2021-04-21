from tkinter import Label, Widget
from PIL import ImageTk, Image
from mag_app_constans import LOGO_PATH, SIZE_LOGO_HEIGHT, SIZE_LOGO_WIDTH


class LogoView (Widget):
    def __init__(self, master=None, cnf={}, **k):
        image = Image.open(LOGO_PATH)
        resiz_image = image.resize((SIZE_LOGO_WIDTH, SIZE_LOGO_HEIGHT))
        img = ImageTk.PhotoImage(resiz_image)

        self.__l_logo = Label(master,
                              image=img,
                              width=SIZE_LOGO_WIDTH,
                              height=SIZE_LOGO_HEIGHT)
        self.__l_logo.image = img
        self.__l_logo.pack()
