import time
from tkinter import *

class Table: 
	def __init__(self,root,S):
		#S.tiler()
		self.root=root
		self.S=S
	# code for creating table
	def update_rule(self):
		for i in range(self.S.size):
			for j in range(self.S.size):
				self.e = Entry(self.root, width=20, fg='blue',font=('Arial',16,'bold'))
				self.e.grid(row=i, column=j)
				self.e.insert(END, self.S.weights_print[j][i])
