#!/usr/bin/envpython3
#coding: utf-8

from collections import defaultdict
import os
import json

dicoEnsgMir=defaultdict(list)
listDico=[]


with open("TableENSG-MIR.tab","r") as f1:
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


print('--------------------------------- Ecriture Résultats---------------------------------------------')

local_Destination_Path_Results ='/home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Result_Json'
os.chdir(local_Destination_Path_Results)

with open("ResultTableENSG-Mir.json","w",encoding="utf-8") as sortie:
    resultsEnsgMir=json.dumps(dicoEnsgMir,indent=2)
    sortie.write(resultsEnsgMir)

with open("ResultTableMirHomo_sapiens.json","w",encoding="utf-8") as sortie:
    for ensg,listMir in dicoEnsgMir.items():
        resultsMir=json.dumps(listMir,indent=2)
        sortie.write(resultsMir)




