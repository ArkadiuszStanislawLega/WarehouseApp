from tkinter import Label, Widget
from PIL import ImageTk, Image


class LogoView (Widget):
    def __init__(self, file_path, width, height, master=None, cnf={}, **k):
        image = Image.open(file_path)
        resiz_image = image.resize((width, height))
        img = ImageTk.PhotoImage(resiz_image)

        self.__l_logo = Label(master,
                              image=img,
                              width=width,
                              height=height)
        self.__l_logo.image = img
        self.__l_logo.pack()
