from tkinter import Tk
from tkinter.filedialog import askopenfilename


def findimg():
	Tk().withdraw() 
	imgname = askopenfilename() #retorna o path da imagem
	return imgname
