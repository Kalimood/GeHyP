from Position import Position
import json

class Misc_rna:
	pos=None
	idgene=""
	note=""
	idtranscrit=""
	numberBoxes=0

	def __init__(self,pos,idgene,note,idtranscrit):
		self.pos=pos
		self.idgene=idgene
		self.note=note
		self.idtranscrit=idtranscrit
		
		

	def printMisc_rna(self):
		print("Misc_rna")
		self.pos.printPosition()
		print(self.idgene)
		print(self.note)
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
	'''
	def numberBoxes(self):
		for i in range(len(self.pos.list_position)):
			numberBoxes=i
		return numberBoxes
	'''
	

	def toJson(self):
		listObj=[]
		Misc_rna={
		"Type":"Misc_rna",
		"Id_gene":str(self.idgene),
		"Id_transcrit":(str(self.idtranscrit)),
		"Positions":self.pos.list_position,
		"Note":str(self.note),
		"NumberBoxe":int(self.pos.lenPosition())
		}

		listObj.append(Misc_rna)
		return listObj

	def obj_dict(self):
		data={}
		data['Type']="Misc_rna"
		data['Id_gene']=self.idgene
		data['Id_transcrit']=self.idtranscrit
		data['Note']=self.note
		data['Positions']=self.pos.list_position
		data['NumberBoxe']=self.pos.lenPosition()
		return data


		