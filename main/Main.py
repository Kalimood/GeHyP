#!/usr/bin/python3
#coding: utf-8
import sys
import os
import stat
import argparse
import re
import logging
#os.path.dirname
#os.getcwd()

#pathBoitesFonc='/home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles'
pathBoitesFonc='/home/kevin/Bureau/Cours/Fac/Keke/GeHyP/BoitesFonctionelles'
##Exemple bash submission
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat -p  1 600000 -p 750000 900000 -j /home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat -p  1 600000 -p 750000 900000 -p 950000 1500000 -j /home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/ 
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t Protein -e  homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat -p  1 600000 -p 750000 900000 -p 950000 1500000 -j /home/kevin/Bureau/StageM2/Scripttest/BoitesFonctionelles/SortieJson/homo_sapiens/ -i /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab -r /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/ResultJson

#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t Protein -e  homo_sapiens -c /home/kevin/Bureau/StageM2/Scripttest/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 5000000 7000000 -p 10000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json -r /home/kevin/Bureau/StageM2/Scripttest/Result
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t Protein -e  homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 5000000 7000000 -p 10000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json/ -r /home/kevin/Bureau/StageM2/Scripttest/Result
#correc python3 /home/kevin/Bureau/Cours/Fac/Keke/GeHyP/main/script2.py -t Protein -e  homo_sapiens -c /home/kevin/Bureau/Cours/Fac/Keke/GeHyP/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.4.dat -p 14000 78000 -p 10000000 12000000 -i /home/kevin/Bureau/Cours/Fac/Keke/GeHyP/UniprotInteractomics/TableCorrelationUniProtKBidSwissProtId.tab -j /home/kevin/Bureau/Cours/Fac/Keke/GeHyP/Result/json/ -r /home/kevin/Bureau/Cours/Fac/Keke/GeHyP/Result/resultatFinalCorrec
#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t MicroArn -e  homo_sapiens -c /home/kevin/Bureau/StageM2/Scripttest/Result/json/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.2.dat -p 11000000 12000000 -p 5900000 6000000 -p 11000000 12000000 -i /home/kevin/Bureau/StageM2/Scripttest/Predict_Target_MiRNA/Raw/TableENSG-MIR.tab -j /home/kevin/Bureau/StageM2/Scripttest/Result/json/ -r /home/kevin/Bureau/StageM2/Scripttest/Result
parser = argparse.ArgumentParser ( description="")

parser.add_argument('-c', '--chromosome', dest="chromosome", default='',help="Enter the path to the file  which contain the data downloaded automatically from Ensembl (Homo_sapiens.GRCh38.104.chromosome.1.dat) for the functional boxes and only the number of chromosome for the Regulatory")

parser.add_argument('-p','--plage',dest="plage", type=int, nargs='+', action='append', 
help='file list')

parser.add_argument('-t','--type',dest="type",default='',help="Select which type of interactor you want (BoiteFonc or MicroArn or Protein)")

parser.add_argument('-e','--espece',dest="espece",default='',help="Select which specie)")

parser.add_argument('-j','--json',dest="json",default='',help="Enter the path to the file which contain the result of ")
parser.add_argument('-i','--table',dest="table",default='',help="Enter the path to the file which contain the conversion table between ENSG and Mir")
parser.add_argument('-r','--result',dest="result",default='',help="Enter the path to the file which contain the result of all program")
parser.add_argument('-n','--ncbi',dest="ncbi",default='',help="Enter the path to the file which contain the conversion table between Ensg and NcbiId")
parser.add_argument('-u','--uniprot',dest="uniprot",default='',help="Enter the path to the file which contain the conversion table between Enst and UniprotId")


args=parser.parse_args()
Type=args.type
espece=args.espece
chromosome=args.chromosome
json=args.json
listPlage=args.plage
selfDir = os.path.dirname(os.path.abspath(__file__))
selfDirback=os.path.split(selfDir)[0]
#print(selfDir,'cheminFichier')
#print(selfDirback,'cheminFichieravant')
pathTableInteractants=args.table
pathResult=args.result
pathNcbi=args.ncbi
pathUniprot=args.uniprot


if not os.path.exists(pathResult):
    print("pathResultNEXISTEPAS")
    os.makedirs(pathResult)

m_space=re.compile("\\s+")
json=args.json+str(listPlage)+'/'
json=re.sub(m_space,'',json)
print("PATH JSON MAIN",json)

    
if Type in ['BoiteFonc','MicroArn','Protein']:
    print(listPlage)
    #cmd='python3 {}/BoitesFonctionelles/ScriptBoiteFoncFinal.py -c {} -e {} -r {}'.format(selfDirback,chromosome,espece,pathResult+"/json")
    cmd='python3 {}/BoitesFonctionelles/ScriptBoiteFoncFinal.py -c {} -e {} -r {}'.format(selfDirback,chromosome,espece,pathResult+"/ResultJson")
    #Manière d'écrire, accolade permet de dire ce qu'il ya dans.format, le premier (ici chromosome va aller dans les accolades)
    cmdplage=""
    for i in listPlage:
        cmdplage+=' -p ' + " ".join(map(str,i))
    
    cmd+=cmdplage
    #Map permet de parcourir tous les elements de la liste i 
    print(pathResult)
    os.system(cmd)

if Type=='BoitesReg':
    cmdReg='python3 {}/BoitesRegulatrices/BoitesRegFinal.py -c {} -e {} -r {}'.format(selfDirback,chromosome,espece,pathResult+"/ResultJson")
    for i in listPlage:
        cmdplage+=' -p ' + " ".join(map(str,i))
    
    cmdReg+=cmdplage
    os.system(cmdReg)

if Type=='MicroArn':
    cmd2='python3 {}/Predict_Target_MiRNA/script/scriptMirdb.py -c {} -j {} -t {} -n {} -u {} -r {} '.format(selfDirback,chromosome,json,pathTableInteractants,pathNcbi,pathUniprot,pathResult+"/InteractMiRNA")
    cmd2+=cmdplage 
    os.system(cmd2)

if Type=='Protein':
    cmd3='python3 {}/UniprotInteractomics/request.py  -c {} -j {} -t {} -r {}'.format(selfDirback,chromosome,json,pathTableInteractants,pathResult+"/UniprotInteractomics")
    print("CMD3",cmd3)
    cmd3+=cmdplage
    os.system(cmd3)
    

    


#exit()


