import json


class Position:
	list_position=[]

	def __init__(self,list_position):
		self.list_position=list_position

	def getStart(self,value):
		return self.list_position[value][0]

	def getEnd(self,value):
		return self.list_position[value][1]
	
	def printPosition(self):
		print(self.list_position)

	def getlistPosition(self):
		return self.list_position

	def getListReverse(self):
		list_reversed=[]
		for i,e in (reversed(list(enumerate(self.list_position)))):
			list_reversed.append(e)
		return list_reversed

	def lenPosition(self):
		total=0
		for i in range(len(self.list_position)):
			total=i+1
		return total

	def lenListPosition(self):
		longueur=len(self.list_position)
		print(longueur)



