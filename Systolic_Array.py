from typing import List
from MAC import MAC
import numpy
from tkinter import *
#import display

class Table: 
	def __init__(self,root,S):
		#S.tiler()
		self.root=root
		self.S=S

	# code for creating table
	def update_rule(self):
		self.timestamp = Text(self.root, height = 3, width=12, bg='black', fg='green',font=('Comic Sans MS',16,'bold'))
		self.timestamp.tag_configure("tag_name",justify='center')		
		self.timestamp.grid(column=0,row=0,columnspan=self.S.size)
		self.timestamp.insert(END,"\nCycles: "+str(self.S.num_cycles))
		self.timestamp.tag_add("tag_name", "1.0", "end")

		for i in range(self.S.size):
			for j in range(self.S.size):
				col="white"
				back="black"
				if ((i%2 + j%2) ==1):
					col="black"
					back="white"
				self.e = Text(self.root, height = 3, width=12, bg=back, fg=col,font=('Comic Sans MS',12,'bold'))
				self.e.tag_configure("tag_name",justify='center')
				self.e.grid(row=i+1, column=j)
				l=["(",str(round(self.S.weights_print[i][j],2)),"\n*",str(round(self.S.input_a[i][j],2)),")\n+",str(round(self.S.input_res[i][j],2))]
				self.e.insert(END, " ".join(l))
				self.e.tag_add("tag_name", "1.0", "end")
				
class SystolicArray:
	def __init__(self,size : int,disp_on):
		self.size = size
		self.buffered_vals = [[0]*size for i in range(size)]
		self.active_vals = [[0]*size for i in range(size)]
		self.systolic_array = [[MAC() for j in range(size)] for i in range(size)]
		self.input_a = [[0]*size for i in range(size)]
		self.input_res = [[0]*size for i in range(size)]
		self.switch_arr = [0]*size
		self.weights_print=[[0]*size for i in range(size)]
		self.disp_on=disp_on
		self.num_cycles = 0
		if(self.disp_on):
			self.root=Tk()
			self.root.title('Systolic Array')
			self.disp_obj=Table(self.root,self)

	def push_weights(self,weight_array : List[float]):
		# if(len(weight_array)!=self.size):
		#     raise(ValueError('Input value size does not match systolic array size'))
		self.buffered_vals = [weight_array] + self.buffered_vals[0:-1]

	def switch_weights(self):
		#self.active_vals = [[j for j in i] for i in self.buffered_vals]
		self.switch_arr[0] = 1

	def init_inputs(self,a_list : List[float]):
		if(len(a_list)!=self.size):
			# raise(ValueError('Input value size does not match systolic array size'))
			diff=self.size-len(a_list)
			col=len(a_list[0])
			for i in range(diff):
				a_list.append([0 for i in col])
		self.input_a =  [[a_list[i]]+[self.systolic_array[i][j-1].reg_a for j in range(1,self.size)] for i in range(self.size)]
		self.input_res = [[0]*self.size] + [[self.systolic_array[i-1][j].reg_result for j in range(self.size)] for i in range(1,self.size)]

	def compute_MAC(self):
		x_list = []
		y_list = []
		z_list = []

		for i in range(self.size):
			if(self.switch_arr[i]==1):
				self.active_vals[i]=self.buffered_vals[i]
			for j in range(self.size):
				x_list.append(self.input_a[i][j])
				y_list.append(self.active_vals[i][j])
				z_list.append(self.input_res[i][j])

		M = MAC()
		res = M.MAC_list(x_list,y_list,z_list)

		for i in range(self.size):
			for j in range(self.size):
				self.systolic_array[i][j].reg_a = self.input_a[i][j]
				self.systolic_array[i][j].reg_result = res[i*self.size+j]

		return res

	def get_outputs(self):
		return([self.systolic_array[-1][i].reg_result for i in range(self.size)])

	def systolic_clock(self,a_list : List[float]):
		self.init_inputs(a_list)
		self.compute_MAC()
		self.switch_arr = [0] + self.switch_arr[0:-1]
		return(self.get_outputs())

	def multiply_stream(self,input_mat,weights):
		self.weights_print=weights
		f = open('instructions.ss','a')
		for i in weights[-1::-1]:
			f.write('push'+str(i)+'\n') #Assembly for weight push
			self.push_weights(i)

		f.write('switch\n') #Assembley for switch
		self.switch_weights()

		#shift the input matrix
		input_mat_shifted = [[0 for j in range(self.size)] for i in range(len(input_mat)*2-1)]
		for i in range(len(input_mat)):
			input_mat[i]+=[0 for ko in range(self.size-len(input_mat[i]))]
			for j in range(self.size):
				input_mat_shifted[i+j][j] = input_mat[i][j]

		res = []
		for i in input_mat_shifted:
			self.num_cycles = self.num_cycles + 1 # increment clock cycle counter
			f.write('input'+str(i)+'\n') #Assembley for input
			res.append(self.systolic_clock(i))
			#update display
			if(self.disp_on):
				self.disp_obj.update_rule()
				self.root.update()
		for i in range(self.size-1):
			self.num_cycles = self.num_cycles + 1 # increment clock cycle counter
			f.write('input'+str([0]*self.size)+'\n') #Assembley for input
			res.append(self.systolic_clock([0]*self.size))
			#update display
			if(self.disp_on):
				self.disp_obj.update_rule()
				self.root.update()
		res = res[self.size-1:]
		
		res_shifted = [[0 for j in range(self.size)] for i in range(len(input_mat))]
		for i in range(len(input_mat)):
			for j in range(self.size):
				res_shifted[i][j] = res[i+j][j]
		# print(numpy.transpose(res_shifted))
		f.close()
		return res_shifted

# S = SystolicArray(2)
# print(S.multiply_stream([[1,2],[3,4],[5,6],[7,8]],[[1,1],[1,1]]))
# S.push_weights([1,1])
# S.push_weights([1,1])
# S.switch_weights()
# print(S.systolic_clock([1,0]))
# S.push_weights([0,1])
# print(S.systolic_clock([3,2]))
# S.push_weights([1,0])
# print(S.systolic_clock([0,4]))
# S.switch_weights()
# print(S.systolic_clock([1,0]))
# print(S.systolic_clock([3,2]))
# print(S.systolic_clock([0,4]))
# print(S.systolic_clock([0,0]))