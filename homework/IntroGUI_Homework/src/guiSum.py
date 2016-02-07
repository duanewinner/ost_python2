#!/usr/local/bin/python3

from tkinter import *

class Application(Frame):
	"""Application main windows class."""
	def __init__(self, master=None):
		"""Main fram initiaization (mostly delegated)"""
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		
	def createWidgets(self):
		"""Add all the widgets to the main frame."""
		top_frame = Frame(self)
		self.number1_label = Label(top_frame, font=("Sans",16), text="Number 1:")
		self.number1 = Entry(top_frame, font=("Sans",16))
		self.number1_label.pack(side=LEFT)
		self.number1.pack(side=RIGHT)
		top_frame.pack(side=TOP)
		
		middle_frame = Frame(self)
		self.number2_label = Label(middle_frame, font=("Sans",16), text="Number 2:")
		self.number2 = Entry(middle_frame, font=("Sans",16))
		self.number2_label.pack(side=LEFT)
		self.number2.pack(side=RIGHT)
		middle_frame.pack(side=TOP)

		bottom_frame = Frame(self)		
		self.label = Label(bottom_frame, text="= SUM", fg="#6666d5", font=("Courier",20), pady=20)
		self.label.pack(side=TOP)	
		self.handleb = Button(bottom_frame, text="Add", fg="green", font=("Sans",16), command=self.handle).pack(side=LEFT)
		self.QUIT = Button(bottom_frame, text="Quit", fg="red", font=("Sans",16), command=self.quit).pack(side=RIGHT)
		bottom_frame.pack(side=BOTTOM)
		
	def handle(self):
		"""Handle a click of the "Add" button by converting numbers to
		type "float", and adding them together, or display "***ERROR***"
		if input cannot be converted to float."""

		number1 = self.number1.get()
		number2 = self.number2.get()
		
		try:
			self.label.config(text=float(number1)+float(number2), fg="#a90bab")
		except:
			self.label.config(text="***ERROR***", fg="red")
		
root = Tk()
app = Application(master=root)
app.mainloop()
