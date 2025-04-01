
class ValueBoxes:
	CtcfNumber=0
	TfNumber=0
	OpenChromNumber=0
	EnhancNumber=0
	PromoteNumber=0
	PromoteFlkNumber=0
	totalNumberRegulBox=0

	def __init__(self,CtcfNumber,TfNumber,OpenChromNumber,EnhancNumber,PromoteNumber,PromoteFlkNumber,totalNumberRegulBox):
		self.CtcfNumber=CtcfNumber
		self.TfNumber=TfNumber
		self.OpenChromNumber=OpenChromNumber
		self.EnhancNumber=EnhancNumber
		self.PromoteNumber=PromoteNumber
		self.PromoteFlkNumber=PromoteFlkNumber
		self.totalNumberRegulBox=totalNumberRegulBox

	def obj_dict(self):
		data={}
		data['Type']="GeneralValueRegulatoryBoxes"
		data['CtcfNumber']=self.CtcfNumber
		data['Tf Number']=self.TfNumber
		data['Open Chromatine Region Number']=self.OpenChromNumber
		data['Enhancer Number']=self.EnhancNumber
		data['Promoter Number']=self.PromoteNumber
		data['Promoter Flanking Region Number']=self.PromoteFlkNumber
		data['Total Regulatory Boxes']=self.totalNumberRegulBox
		return data

		
		