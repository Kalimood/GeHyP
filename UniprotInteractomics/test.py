#!/usr/bin/envpython3
#coding: utf-8                                                                                                                                                                                                                                                                                                                          


import requests, sys
import json
from collections import defaultdict


with open("TableCorrelationUniProtKBidSwissProtId.tab","r") as f1:
    for li in f1:
        ln=li.rstrip("\n")
        ls=ln.split("\t")
        #print(ls)
        idENSG=ls[0]
        idVersENSG=ls[1]
        idTranscrit=ls[2]
        idTranscritVersion=ls[3]
        mirBaseAccession=ls[4]
        mirBaseId=ls[5]
        if len(mirBaseId)>0:
            dicoEnsgMir[idENSG].append(mirBaseId)



#requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/interaction/Q99706"
requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/interaction/P03886"

r = requests.get(requestURL, headers={ "Accept" : "application/json"})
pathUniprot='/home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics'
if not r.ok:
  r.raise_for_status()
  sys.exit()

responseBody = r.text
data=json.loads(responseBody)
#print(data)
e
#print(len(data))
#print(type(data))
listInteractants=data[0]
#print(listInteractants)

Listprotein=data[0]
#print(protein)
#print(len(listInteractor))

#clé de i : 'accession':Q99706 'name':KI2L4_HUMAN,'proteinExistence':Evidence at protein level,'taxonomy':9606 'interactions':[{}]

dicoIdUniprotInteractants=defaultdict(list)

for cle,interactants in listInteractants.items():
  for i in range(len(listInteractants['interactions'][interactants])):
    print(i)
  #print(listInteractants[interactions][j])
  #print(i,'clé')
  #print(j,'valeur')
  '''
  for g in range(len(listInteractants['interactions'][j])):
    print(g)
  #print(j)
  '''


exit()
for j in range(len(listInteractants['interactions'])):
  print(i[j])
#print(listInteractor)

exit()
for dico in data:
  if type(dico)=="<class 'dict'>":
    print(type(dico))
exit()
for dico in data: 
  #print(dico,"\n"*2)
  print(data[dico])



exit()

for i in range(len(data)):
  print(i[1])






with open ("Returnrequest.json","w",encoding="utf-8") as sortie:
  json.dump(data,sortie,indent=2)
  sortie.close()
#print(responseBody)
