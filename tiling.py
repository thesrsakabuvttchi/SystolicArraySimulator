# WxI
import numpy
import copy
from Systolic_Array import SystolicArray

class hostcaller:
	def __init__(self,systolic,disp_on=True):
		self.systolic=systolic
		self.disp_on=disp_on
		self.sysobj= SystolicArray(systolic,self.disp_on)
		#stream from files
		W=open("weightmat.txt","r")
		I=open("inputmat.txt","r")
		buf=W.readlines()
		#load the weight dimensions and the weights
		self.wdims=[int(i) for i in buf[0].split()]
		self.weights=[[float(i) for i in tmp.split()] for tmp in buf]
		self.weights=self.weights[1:]
		buf=I.readlines()
		#load the input dimensions and the inputs
		self.idims=[int(i) for i in buf[0].split()]
		self.inputs=[[float(i) for i in tmp.split()] for tmp in buf]
		self.inputs=self.inputs[1:]
		W.close()
		I.close()
	def tiler(self):
		#display object
		if (self.wdims[1]!=self.idims[0]):
			print("Not possible")
			return -1
		# weights=[["w"+str(i)+","+str(j) for j in range(1,wdims[1]+1)]for i in range(1,wdims[0]+1)]
		# inputs=[["i"+str(i)+","+str(j) for j in range(1,idims[1]+1)]for i in range(1,idims[0]+1)]
		print("Weights:",self.wdims)
		print("Input:",self.idims)
		# number of iterations horizontally/ along the rows
		row_blocks=int(self.wdims[1]/self.systolic)
		if(self.wdims[1]%self.systolic>0):
			row_blocks+=1

		# number of iterations vertically/ along the columns
		col_blocks=int(self.wdims[0]/self.systolic)
		if(self.wdims[0]%self.systolic>0):
			col_blocks+=1

		final_ans=[[0 for m in range(self.idims[1])]for u in range(self.wdims[0])]
		base_row=0
		# list all the weight ranges
		for j in range(0,col_blocks):
			for i in range(0,row_blocks):
				w_print=[] # stores the accessible weights
				i_print=[] # stores the rows required

				# print the corners of the submatrix pulled from the weight matrix
				# x is horizontal axis
				x1=i*self.systolic
				y1= j*self.systolic
				x2= min(i*self.systolic+self.systolic-1,self.wdims[1]-1)
				y2= min(j*self.systolic+self.systolic-1,self.wdims[0]-1)
				print("x1= ",x1,"y1= ",y1)
				print("x2= ",x2,"y2= ",y2)
				# get the corresponding columns
				i_print=copy.deepcopy(self.inputs[i*self.systolic : 1+min(i*self.systolic+self.systolic-1,self.wdims[1]-1)])
				
				# add zeroes to make it execution ready
				# num_z=0
				# for itr in range(len(i_print)):
				# 	i_print[itr]=[0 for ijk in range(num_z)] + i_print[itr] + [0 for ijk in range(self.systolic-1-num_z)]
				# 	num_z+=1
				# prepare the immediate weights to be loaded onto the systolic array
				for x in range(j*self.systolic,1+min(j*self.systolic+self.systolic-1,self.wdims[0]-1)):
					w_print.append(self.weights[x][i*self.systolic : 1+min(i*self.systolic+self.systolic-1,self.wdims[1]-1)])
				
				#print the states according to the telens reference
				# w_print_transpose=numpy.transpose(w_print).tolist()
				# for ko in range(len(w_print_transpose)):
				# 	print(i_print[ko][-1::-1],"\t",w_print_transpose[ko])
				# print("\n")

				# print the states
				print("weight= ")
				for krow in w_print:
					print(krow)
				print("input= ")
				for krow in i_print:
					print(krow)
				
				# expected intermediate
				print("Expected-inter:")
				print(numpy.dot(w_print,i_print))

				#padding weights(making it 4x4)
				for k in range(self.systolic-len(w_print)):
					w_print.append([])
				for k in range(self.systolic):
					w_print[k]+=[0 for u in range(self.systolic-len(w_print[k]))]
				#padding inputs (making it rows x min(self.systolic,len(inputs[0])))
				for k in range(len(i_print)):
					if(len(i_print[k])<self.systolic):
						i_print[k]+=[0 for iu in range(self.systolic-len(i_print[k]))]
				
				w_print_transpose=numpy.transpose(w_print).tolist()
				i_print_transpose=numpy.transpose(i_print).tolist()
				# compute the sums
				inter_ans=numpy.transpose(self.sysobj.multiply_stream(i_print_transpose,w_print_transpose)).tolist()
				for p in range(y1,y2+1):
					for q in range(self.idims[1]):
						final_ans[p][q]+=inter_ans[p-y1][q]
				base_row+=(y2-y1)+1
		
		# print(self.weights,self.inputs)
		print("Expected Final")
		print(numpy.dot(self.weights,self.inputs))
		print("Computed:")
		print(numpy.array(final_ans))
		print("Errors:")
		print(numpy.dot(self.weights,self.inputs)-numpy.array(final_ans))
		return(numpy.array(final_ans))
				
	

#wdims - weight dimentions -- 32 rows, 42 columns
# idims - input dimentions	
# wdims=[12,15] 
# idims=[15,12] # number of features = idmis[0]
# systolic=16

# tiler(wdims,idims,systolic)


# S= hostcaller(8)
# S.tiler()