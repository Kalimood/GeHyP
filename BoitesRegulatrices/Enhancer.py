import json
from Position import Position

class Enhancer:

	def __init__(self,numChr,pos,id,typeBoite):
		self.numChr=numChr
		self.pos=pos
		self.id=id
		self.typeBoite=typeBoite

	def inRange(self,pos1,pos2):
		parcours=False
		#print("pos1= " + pos1)
		#print("pos2= " + pos2)
		for i in range(len(self.pos)):
			#print("gene start "+ str(i) + "= " + str(self.pos.list_position[i][0]) )
			#print("gene end "+ str(i) + "= " + str(self.pos.list_position[i][1]))
			if int(self.pos[0])>=int(pos1) and int(self.pos[0])<int(pos2):
				parcours = True
				#print("condition1")
			elif int(self.pos[1])>int(pos1) and int(self.pos[1])<=int(pos2):
				parcours= True
		return parcours

	def print(self):
		print(self.numChr)
		print(self.pos)
		print(self.id)
		print(self.typeBoite)
	
	
	def obj_dict(self):
		data={}
		data['Type']=self.typeBoite
		data['Chromosome']=self.numChr
		data['Position']=self.pos
		data['Id']=self.id
		return data
