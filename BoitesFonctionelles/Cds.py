from Position import Position

class Cds:
	pos=None
	idgene=""
	idprotein=""
	note=""

	def __init__(self,pos,idgene,idprotein,note):
		self.pos=pos
		self.idgene=idgene
		self.idprotein=idprotein
		self.note=note

		

	def printCds(self):
		print("CDS")
		self.pos.Printposition()
		print(self.idgene)
		print(self.idprotein)
		print(self.note)
		print(" ")

	def inRange(self,pos1,pos2):
		parcours=False
		for i in range(len(self.pos.list_position)):
			if int(self.pos.list_position[i][0])>=int(pos1) and int(self.pos.list_position[i][0])<int(pos2):
				parcours = True
			elif int(self.pos.list_position[i][1])>int(pos1) and int(self.pos.list_position[i][1])<=int(pos2):
				parcours= True
		return parcours


	def obj_dict(self):
		data={}
		data['Type']='CDS'
		data['Id_gene']=self.idgene
		data['Id_protein']=self.idprotein
		data['Id_transcrit']=self.note
		data['Positions']=self.pos.list_position
		data['NumberBox']=self.pos.lenPosition()
		return data

