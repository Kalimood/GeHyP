from Position import Position

class Mrna:
	pos=None
	idgene=""
	idtranscrit=""
	def __init__(self,pos,idgene,idtranscrit):
		self.pos=pos
		self.idgene=idgene
		self.idtranscrit=idtranscrit
		
	def printMrna(self):
		print("Exons")
		self.pos.printPosition()
		print(self.idgene)
		print(self.idtranscrit)
		print(" ")

	def inRange(self,pos1,pos2):
		parcours=False
		for i in range(len(self.pos.list_position)):
			if int(self.pos.list_position[i][0])>=int(pos1) and int(self.pos.list_position[i][0])<int(pos2):
				parcours = True
			elif int(self.pos.list_position[i][1])>int(pos1) and int(self.pos.list_position[i][1])<=int(pos2):
				parcours= True
		return parcours

	def toJson(self):
		listObj=[]
		mRNA={
		"Type":"Mrna",
		"Id_gene":str(self.idgene),
		"Id_transcrit":(str(self.idtranscrit)),
		"Positions":self.pos.list_position,
		"NumberBoxe":int(self.pos.lenPosition())
		}
		listObj.append(mRNA)
		return listObj

	def obj_dict(self):
		data={}
		data['Type']="Mrna"
		data['Id_gene']=self.idgene
		data['Id_transcrit']=self.idtranscrit
		data['Positions']=self.pos.list_position
		data['NumberBoxe']=self.pos.lenPosition()	
		return data



