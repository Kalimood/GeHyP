from Position import Position
class Utr:
	pos=None
	list_ind=[]
	print("Class UTR")
	print("")

	def __init__(self,pos,list_ind):
		self.pos=pos
		self.list_ind=list_ind

	def printUtra(self):
		print("UTRa")
		self.pos.printPosition()
		print(self.list_ind)
		print("")

	def printUtrb(self):
		print("UtrB")
		self.pos.printPosition()
		print(self.list_ind)
		print("")

	def toJsona(self):
		UTRa={
		"Type":"UTRa",
		"Positions":self.pos.list_position,
		"Indices":self.list_ind
		}
		return UTRa

	def toJsonb(self):
		UTRb={
		"Type":"UTRb",
		"Positions":self.pos.list_position,
		"Indices":self.list_ind
		}
		return UTRb





