class GeneralChromosomeValues:
	Specie=""
	Genome=""
	Chromosome=0
	Start_Chromosome=0
	End_Chromosome=0
	TotalNumberOfSegments=0
	TotalBoxes=0
	GeneNumber=0
	cdsNumber=0
	cdsBoxes=0
	miscRNAnumber=0
	miscRNABoxes=0
	mRNAnumber=0
	mRNABoxes=0

	def __init__(self,specie,genomeref,chromosome,startC,endC,totalNumberSegments,totalBoxes,geneNumber,cdsNumber,cdsBoxes,miscRNAnumber,miscRNABoxes,mRNAnumber,mRNABoxes):
		self.specie=specie
		self.genomeref=genomeref
		self.chromosome=chromosome
		self.startC=startC
		self.endC=endC
		self.totalNumberSegments=totalNumberSegments
		self.totalBoxes=totalBoxes
		self.geneNumber=geneNumber
		self.cdsNumber=cdsNumber
		self.cdsBoxes=cdsBoxes
		self.miscRNAnumber=miscRNAnumber
		self.miscRNABoxes=miscRNABoxes
		self.mRNAnumber=mRNAnumber
		self.mRNABoxes=mRNABoxes

	def obj_dict(self):
		data={}
		data['Type']="GeneralChromosomeValues"
		data['Specie']=self.specie
		data['Genomeref']=self.genomeref
		data['StartChromosome']=self.startC
		data['EndChromosome']=self.endC
		data['Total Number Of Segments']=self.totalNumberSegments
		data['Total Boxes']=self.totalBoxes
		data['Gene Number']=self.geneNumber
		data['CDS Number']=self.cdsNumber
		data['CDS Boxes']=self.cdsBoxes
		data['miscRNAnumber']=self.miscRNAnumber
		data['Misc_RNA Boxes']=self.miscRNABoxes
		data['mRNAnumber']=self.mRNAnumber
		data['mRNABoxes']=self.mRNABoxes
		return data

		
