
from Position import Position
import json

class Gene:
	pos=None
	nom=""
	locus=""
	note=""


	def __init__(self,pos,nom,locus,note):
		self.pos=pos
		self.nom=nom
		self.locus=locus
		self.note=note

	

	def printGene(self):
		print("Gene")
		self.pos.printPosition()
		print(self.nom)
		print(self.locus)
		print(self.note)
		print(self.boiteGene)
		print(" ")


	def inRange(self,pos1,pos2):
		parcours=False
		#print("pos1= " + pos1)
		#print("pos2= " + pos2)
		for i in range(len(self.pos.list_position)):
			#print("gene start "+ str(i) + "= " + str(self.pos.list_position[i][0]) )
			#print("gene end "+ str(i) + "= " + str(self.pos.list_position[i][1]))
			if int(self.pos.list_position[i][0])>=int(pos1) and int(self.pos.list_position[i][0])<int(pos2):
				parcours = True
				#print("condition1")

			elif int(self.pos.list_position[i][1])>int(pos1) and int(self.pos.list_position[i][1])<=int(pos2):
				parcours= True
				#print("condition2")
		#print("parcours= " + str(parcours))
			
		return parcours


	def toJson(self):
		
		gene={
		"Type":"Gene",
		"Id_gene":str(self.nom),
		"Positions":self.pos.list_position,
		"Locus":str(self.locus),
		"Note":str(self.note),
		"NumberBoxe":int(self.pos.lenPosition())
		}

	def obj_dict(self):
		data={}
		data['Type']='Gene'
		data['Nom']=self.nom
		data['Positions']=self.pos.list_position
		data['Locus']=self.locus
		data['Note']=self.note
		data['NumberBoxe']=self.pos.lenPosition()
		return data

			





		'''
		if isinstance(obj,Gene):
			return {"__class__":"Gene",
				"Id":obj.nom,
				"Positions":obj.pos,
				"Locus":obj.locus,
				"Note":obj.note}
		'''
		raise TypeError(repr(obj)+"isn't serialized")


'''
{"listGene":[
{"Type": "Gene", "Id_gene": "ENSG00000223972.5", "Positions": [["11869", "14409"]], "Locus": "DDX11L1", "Note": "\"DEAD/H-boxhelicase11like1[Source:HGNCSymbol;Acc:HGNC:37102]\""},
{"Type": "Gene", "Id_gene": "ENSG00000227232.5", "Positions": [["14404", "29570"]], "Locus": "WASH7P", "Note": "\"WASPfamilyhomolog7,pseudogene[Source:HGNCSymbol;Acc:HGNC:38034]\""},
{"Type": "Gene", "Id_gene": "ENSG00000278267.1", "Positions": [["17369", "17436"]], "Locus": "MIR6859-1", "Note": "\"microRNA6859-1[Source:HGNCSymbol;Acc:HGNC:50039]\""}
]
}
'''