#!/usr/bin/envpython3
#coding: utf-8
import sys
import os
import stat
#os.path.dirname
#os.getcwd()

pathBoitesFonc='/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles'
#pathCommun=os.environ('/home/kevin/Bureau/StageM2/Scripttest')
Type=str(sys.argv[1])
espece=str(sys.argv[2])
listPlage=[]

for i in range(3,len(sys.argv)):
    plage=sys.argv[i]
    plage=plage.split(",")
    start=int(plage[0])
    end=int(plage[1])
    listPlage.append([start,end])

if Type == 'BoiteFonc':    
    exec(compile(open('/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py').read(), '/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py', 'exec'))
    
    #exec(open('~/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py').read())
    #os.system('/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py')



elif Type=='MicroArn':
    exec(compile(open('/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py').read(), '/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/scripttest2.py', 'exec'))
    exec(compile(open('/home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/script/scriptMirdb.py').read(), '/home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/script/scriptMirdb.py', 'exec'))



#Chercher chemin relatif par rapport ou se toruve le script. set env
#Recuperer et de savoir dans quel repertoire jexecute le script. A l'install tous mes fichiers doivent etre dans le même repertoire