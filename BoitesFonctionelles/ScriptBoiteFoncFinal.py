#!/usr/bin/envpython3
#coding: utf-8
__author__="Kevin Rayas"

#python3 /home/kevin/Bureau/StageM2/Scripttest/main/script2.py -t BoiteFonc -e homo_sapiens -c /home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat -p 1 4000000 -p 400500 990000

#Library import
import os
import fnmatch
import re
import ftplib
from ftplib import FTP
import sys
import gzip
import csv
import urllib
from urllib import request
import logging
import argparse
from collections import defaultdict
import json

#Library Class import

from Position import Position
from Gene import Gene
from Misc_rna import Misc_rna
from Mrna import Mrna
from Cds import Cds
from Utr import Utr
from GeneralChromosomeValues import GeneralChromosomeValues
#from script2  import espece,listPlage
#from BoitesFonctionnelles import BoitesFonctionnelles


#List of arguments
#espece = sys.argv[1]
#chromosome=sys.argv[2]
#start=sys.argv[2]
#end=sys.argv[3]


print("--------------------Downloading Chromosome Files------------------------")

#Functions
def download(espece,result):

    """what this function does?
    inputs :
        espece, name of specie to  download
    outputs:
        local_Destination_Path, where data have been dowloaded
    """
    #urlName = "ftp://ftp.ensembl.org/pub/release-100/embl/"+espece +"/"
    urlName = "ftp://ftp.ensembl.org/pub/current_embl/"+espece +"/"

    local_Destination_Path = result+"/"+espece +"/"
    if not os.path.exists(local_Destination_Path):
        os.makedirs(local_Destination_Path)
    else:
        logging.info(local_Destination_Path,"The directory is already created")

    os.chdir(local_Destination_Path)
    
    for fichier in files:
        if fichier.endswith('.gz'):
            chromosome=fichier
            chromosomeShort = os.path.splitext(chromosome)[0]
            local_filenames=os.listdir(local_Destination_Path)
            if chromosomeShort in local_filenames:
                print(chromosomeShort,"is already downloaded")
            else:
                logging.error("Opening",(urlName)+ ":::" +chromosome)
                try:
                    with urllib.request.urlopen(urlName+ chromosome) as response:
                        try :
                            with gzip.GzipFile(fileobj=response) as uncompressed:
                                file_content = uncompressed.read()
                            fileOutName = os.path.splitext(chromosome)
                            print("Loading and decompression successful for",fileOutName[0])
                        except :
                            logging.error("Unable to decompress file",fileOutName[0])
                    try :
                        with open(fileOutName[0], 'wb') as f:
                            f.write(file_content)
                    except :
                        logging.error("Error opening file for output",fileOutName[0])
                except:
                    logging.error("Error at opening url request : ",urlName)

    return str(local_Destination_Path) 


def cleanspace(text):
    """What this function does?
    inputs:
        text with space
    output:
        same text without space
    """
    m_space=re.compile("\\s+")
    #m_space=re.compile("\s+")
    text_clean=re.sub(m_space, '', text)
    #print("TEXTE CLEAN CORREC"+text_clean)
    #text_clean=re.sub(m_space,'',text)
    return text_clean


def get_id(champ2,champ3):
    if champ2=="gene":
        id_gene=m_gene_id.search(champ3)
        if id_gene is not None:
            id_gene=id_gene.group(2)
            return id_gene

    elif champ2=="misc_RNA":
        id_miscRNA=m_idgene.search(champ3)
        if id_miscRNA is not None:
            id_miscRNA=id_miscRNA.group()
            return id_miscRNA

    elif champ2=="mRNA":
        id_gene_mRNA=m_idgene.search(champ3)
        if id_gene_mRNA is not None:
            id_gene_mRNA=id_gene_mRNA.group()
            return id_gene_mRNA

    elif champ2=="CDS":
        id_gene_CDS=m_idgene.search(champ3)
        if id_gene_CDS is not None:
            id_gene_CDS=id_gene_CDS.group()
            return id_gene_CDS
    else:
        return('autre champ')

def get_position(champ2,champ3):
    if champ2=="source":
        position_chromosome=m_position.findall(champ3)
        
        return Position(position_chromosome)

    elif champ2=="gene":
        list_position_gene=m_position.findall(champ3)
        #print(list_position_gene)
        return Position(list_position_gene)
        
    
    elif champ2=="misc_RNA":
        list_positions_miscRNA=m_position.findall(champ3)
        return Position(list_positions_miscRNA)
       
        
    elif champ2 =="mRNA":
        list_positions_exons=m_position.findall(champ3)
        return Position(list_positions_exons)
    
    elif champ2=="CDS":
        list_positions_CDS=m_position.findall(champ3)
        return Position(list_positions_CDS)

    else:
        return('autre champ')
        
def get_locus(champ2,champ3):

    if champ2=="gene":
        locus_gene=m_locus.search(champ3)

        if locus_gene is not None:
            locus_gene=locus_gene.group(2)
            return locus_gene

        else:
            return('autre champ')

def get_note(champ2,champ3):

    if champ2=="gene":
        note_gene=m_note.search(champ3)

        if note_gene is not None:
            note_gene=note_gene.group(2)
            return note_gene
    elif champ2=="misc_RNA":
        note_miscRNA=m_note_miscRNA.search(champ3)

        if note_miscRNA is not None:
            note_miscRNA=note_miscRNA.group(2)
            return note_miscRNA

    elif champ2 =="CDS":
        note_transcrit_id_CDS=m_idtranscrit.search(champ3)
        if note_transcrit_id_CDS is not None:
            note_transcrit_id_CDS=note_transcrit_id_CDS.group()
            return note_transcrit_id_CDS


def get_id_transcrit(champ2,champ3):

    if champ2=="misc_RNA":
        id_transcrit_miscRNA=m_idtranscrit.search(champ3)

        if id_transcrit_miscRNA is not None:
            id_transcrit_miscRNA=id_transcrit_miscRNA.group()
            return id_transcrit_miscRNA

    elif champ2=="mRNA":
        id_transcrit_mRNA=m_idtranscrit.search(champ3)

        if id_transcrit_mRNA is not None:
            id_transcrit_mRNA=id_transcrit_mRNA.group()
            return id_transcrit_mRNA

def get_id_protein(champ2,champ3):
    if champ2=="CDS":
        id_protein_CDS=m_id_protein.search(champ3)
        if id_protein_CDS is not None:
            id_protein_CDS=id_protein_CDS.group()
            return id_protein_CDS




def createUtra(list_mRNA,list_CDS):
    list_Utra_obj=[]

    for i in range(len(list_mRNA)):

        for j in range(len(list_CDS)):

            if list_mRNA[i].idtranscrit==list_CDS[j].note:
                mRna_start=list_mRNA[i].pos.getStart(0)
                mRna_end=list_mRNA[i].pos.getEnd(-1)
                Cds_start=list_CDS[j].pos.getStart(0)
                Cds_end=list_CDS[j].pos.getEnd(-1)
                
                
                if Cds_start < mRna_start:
                    logging.info("Error: A CDS cant begin before an Exon")

                elif Cds_start > mRna_end:
                    logging.info("Error: A CDS must begin before the end of ARNm")
                

                list_positions_mRNA=list_mRNA[i].pos.getlistPosition()
                list_positions_CDS=list_CDS[j].pos.getlistPosition()
                
                for positions_CDS in range(len(list_positions_CDS)):
                    pos_s_Cds=list_positions_CDS[positions_CDS][0]
                    pos_e_Cds=list_positions_CDS[positions_CDS][1]

                    for positions_mRna in range(len(list_positions_mRNA)):
                        pos_s_Mrna=list_positions_mRNA[positions_mRna][0]
                        pos_e_Mrna=list_positions_mRNA[positions_mRna][1]


                        if int(pos_s_Cds)<int(pos_e_Mrna) and int(pos_s_Cds)>int(pos_s_Mrna):
                            list_Utra=[]
                            list_ind_Utra=[]           
                            UTRa=[int(pos_s_Mrna),int(pos_s_Cds)-1]
                            list_ind_Utra.append(positions_mRna+1)
                            list_Utra.append(UTRa)
                            Utra_pos=Position(list_Utra)
                            Utra_obj=Utr(Utra_pos,list_ind_Utra)
                            #Utra_obj.printUtra()
                            list_Utra_obj.append(Utra_obj)
                               
                            break
                                      
    return list_Utra_obj
                


def createUtrB(list_mRNA,list_CDS):
    list_Utrb_obj=[]

    for i in range(len(list_mRNA)):

        for j in range(len(list_CDS)):

            if list_mRNA[i].idtranscrit==list_CDS[j].note:
                mRna_start=list_mRNA[i].pos.getEnd(-1)
                mRna_end=list_mRNA[i].pos.getStart(0)
                Cds_start=list_CDS[j].pos.getEnd(-1)
                Cds_end=list_CDS[j].pos.getStart(0)
                
                
                if Cds_start > mRna_start:
                    logging.info("Error: A CDS cant begin before an Exon")


                elif Cds_start < mRna_end:
                    logging.info("Error: A CDS must begin before the end of ARNm")
                

                list_positions_mRNA=list_mRNA[i].pos.getlistPosition()
                list_positions_CDS=list_CDS[j].pos.getlistPosition()

                for positions_CDS in reversed(range(len(list_positions_CDS))):

                    pos_s_Cds=list_positions_CDS[positions_CDS][1]
                    pos_e_Cds=list_positions_CDS[positions_CDS][0]

                    for positions_mRna in reversed(range(len(list_positions_mRNA))):

                        pos_s_Mrna=list_positions_mRNA[positions_mRna][1]
                        pos_e_Mrna=list_positions_mRNA[positions_mRna][0]

                        if int(pos_s_Cds) > int(pos_s_Mrna):
                            logging.info("Open reading frame must stop before the end of ARNm ")

                        elif int(pos_s_Cds)> int(pos_e_Mrna) and int(pos_s_Cds)< int(pos_s_Mrna):
                            list_Utrb=[]
                            list_ind_Utrb=[]           
                            UTRb=[int(pos_s_Cds)+1,int(pos_s_Mrna)]
                            list_ind_Utrb.append(positions_mRna+1)
                            list_Utrb.append(UTRb)
                            Utrb_pos=Position(list_Utrb)
                            Utrb_obj=Utr(Utrb_pos,list_ind_Utrb)
                            #Utrb_obj.printUtrb()
                            list_Utrb_obj.append(Utrb_obj)
                            
                            break
    return list_Utrb_obj


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser ( description="")
    #parser.add_argument('-c', '--chromosome', dest="chromosome", default='/home/kevin/Bureau/StageM2/homo_sapiens/Homo_sapiens.GRCh38.104.chromosome.1.dat',help="Enter the path to the file which contain all the data of chromosome ending by.dat from Ensembl (/pub/current_embl/'+espece)")
    parser.add_argument('-c', '--chromosome', dest="chromosome", default='/home/kevin/Bureau/Cours/Fac/Keke/GeHyP/Result/ResultJson',help="Enter the path to the file which contain all the data of chromosome ending by.dat from Ensembl (/pub/current_embl/'+espece)")
    parser.add_argument('-e', '--espece', dest="espece", default='homo_sapiens',
    help="""Enter the name of the specie you want to study""")

    #help="""Enter the name of the file where the result will be store""")
    parser.add_argument('-p','--plage',dest="plage",type=int, nargs='+', action='append', 
    help='enter the plage you want like -p 1 4000000 -p 400500 990000')

    parser.add_argument('-r', '--result', dest="result", help="""Enter the path of the result you want t""")

    
    
    #Verification of arguments
    args=parser.parse_args()
    print(args.plage)
    espece=args.espece
    chromosome=args.chromosome
    listPlage=args.plage
    result=args.result
    print("RESULT CORREC",result)
    if not os.path.exists(result):
        os.makedirs(result)
    
    #exit(result)

    ftp = ftplib.FTP('ftp.ensembl.org')
    ftp.login()
    ftp.cwd('/pub/current_embl/'+espece)

    #ftp.cwd('/pub/release-100/embl/'+espece)
    files = ftp.nlst()
    
    local_Destination_Path = result+"/"+espece +"/"
    whereAreMyData = download(espece,result)
    
    m_position = re.compile("(\d+)[.][.](\d+)")
    m_idgene = re.compile("ENSG\d+[.]\d+")
    m_idtranscrit = re.compile("ENST\d+[.]\d+")
    m_gene_id=re.compile('([/]gene)=(ENSG\d+[.]\d+)')
    m_locus=re.compile('([/]locus_tag)=["](.+)["]([/])')
    m_note=re.compile('([/]note)=(.+)')
    m_note_miscRNA=re.compile('["]([/]note)=["](.+)["][/]')
    m_idtranscrit=re.compile('ENST\d+[.]\d+')
    m_id_protein=re.compile('ENSP\d+[.]\d+')
    m_specie=re.compile("(DE\s+)(.+)(chromosome)")
    wipchamp2=""
    wipchamp3=""
    id_gene=""
    locus_gene=""
    note_gene=""
    list_gene=[]
    dicoGenePlage=defaultdict(list)
    list_plage_gene=[]
    list_miscRna=[]
    dicoMiscRnaPlage=defaultdict(list)
    list_mRNA=[]
    dicoMrnaPlage=defaultdict(list)
    list_CDS=[]
    dicoCdsPlage=defaultdict(list)
    listObjTot=[]
    listObjgene=[]
    listObjMiscRNA=[]
    listObjCds=[]
    listObjMrna=[]
    listObjgene=[]
    JsonData=[]
    dic_BoiteFonctionnelles_Json=defaultdict(list)
    dicListBoitefonc=defaultdict(list)
    numerochromosome=""
    start_chromosome=""
    end_chromosome=""
    genomeref=""
    info_species=""
    totalNumberBoxes=0
    geneNumber=0
    miscRnaNumber=0
    mRnaNumber=0
    cdsNumber=0
    generalChromosomeValues={}
    totalBoxes=0
    totalMrnaBoxes=0
    totalCdsBoxes=0
    totalMiscRnaBoxes=0
    dicBoiteFonctionnelles=defaultdict(lambda:defaultdict(int))
    #listPlage=[]
    listNumberGenePlage=[]
    listNumberMiscRnaPlage=[]
    listNumberMrnaPlage=[]
    listNumberCDSPlage=[]
    valeurs=""
    dicoGene=defaultdict(list)
    dicoCds=defaultdict(list)
    dicoMiscRna=defaultdict(list)
    dicoMrna=defaultdict(list)
    dicoGeneralChromosomeValues=defaultdict(list)
    dico4=defaultdict(list)
    dicoPosition=defaultdict(dict)

    choice_chromosome=args.chromosome
    
    with open(choice_chromosome, mode='rt') as file:

        for li in file:
            champ1=li[0:2]
            champ2=li[3:21]
            champ3=li[21:]
            champ1_net=cleanspace(champ1)
            champ2_net=cleanspace(champ2)
            champ3_net=cleanspace(champ3)

            if li.startswith('AC'):
                chromosome = li
                chromosome = chromosome.split(':')
                genomeref = chromosome[1]
                numerochromosome = chromosome[2]
                start_chromosome = chromosome[3]
                end_chromosome = chromosome[4]

            elif li.startswith('DE'):
                info_specie=m_specie.search(li)
                if info_specie is not None:
                    info_species=info_specie.group(2)


            elif champ1_net=="FT":

                if len(champ2_net)==0:
                    wipchamp3+=champ3_net

                else:
                    if len(wipchamp2)!=0 and len(wipchamp3)!=0:
                        #print(wipchamp2,wipchamp3)
                        pos_o=get_position(wipchamp2,wipchamp3)
                        idGene_o=get_id(wipchamp2,wipchamp3)
                        locus_o=get_locus(wipchamp2,wipchamp3)
                        note_o=get_note(wipchamp2,wipchamp3)
                        idTranscrit_o=get_id_transcrit(wipchamp2,wipchamp3)
                        idProtein_o=get_id_protein(wipchamp2,wipchamp3)
                        #boiteGene=Gene.numberBoxes(list_position_gene)
                        #print(listPlage)
                        for j in range(len(listPlage)):
                            start=listPlage[j][0]
                            end=listPlage[j][1]
                            #print(listPlage[j])
                            
                            if wipchamp2=="gene":
                                gene=Gene(pos_o,idGene_o,locus_o,note_o)
                               
                                if gene.inRange(start,end):
                                    dicoGenePlage [str(listPlage[j])].append(gene)
                                    #list_gene.append(gene)
                                
                            elif wipchamp2=="misc_RNA":
                                misc_RNA=Misc_rna(pos_o,idGene_o,note_o,idTranscrit_o)
                                #misc_RNA.printMisc_rna()
                                if str(listPlage[j]) not in dicoMiscRnaPlage:
                                    dicoMiscRnaPlage[str(listPlage[j])]=[]
                                if misc_RNA.inRange(start,end):
                                    totalMiscRnaBoxes+=misc_RNA.pos.lenPosition()
                                    #list_miscRna.append(misc_RNA)
                                    dicoMiscRnaPlage[str(listPlage[j])].append(misc_RNA)
                                    
                                    #print(totalMiscRnaBoxes)

                            elif wipchamp2=="mRNA":
                                mRNA=Mrna(pos_o,idGene_o,idTranscrit_o)
                                #mRNA.printMrna()

                                if str(listPlage[j]) not in dicoMrnaPlage:
                                    dicoMrnaPlage[str(listPlage[j])]=[]

                                if mRNA.inRange(start,end):
                                    totalMrnaBoxes+=mRNA.pos.lenPosition()
                                    #list_mRNA.append(mRNA)
                                    dicoMrnaPlage[str(listPlage[j])].append(mRNA)
                                    
                                    #print(totalMrnaBoxes)

                            elif wipchamp2=="CDS":
                                cds=Cds(pos_o,idGene_o,idProtein_o,note_o)
                                #cds.printCds()
                                if str(listPlage[j]) not in dicoMrnaPlage:
                                    dicoMrnaPlage[str(listPlage[j])]=[]
                                if cds.inRange(start,end):
                                    totalCdsBoxes+=cds.pos.lenPosition()
                                    #list_CDS.append(cds)
                                    dicoCdsPlage[str(listPlage[j])].append(cds)
                                    
                                #print(totalCdsBoxes)


                    wipchamp3=""
                    wipchamp3+=champ3_net
                    wipchamp2=champ2_net


                    #list_Utra_o=createUtra(list_mRNA,list_CDS)
                    #list_Utrb_o=createUtrB(list_mRNA,list_CDS)
                                        #print(wipchamp2)
                                        #print(wipchamp3) 
    
    dicoGlobPlageType=defaultdict(lambda:defaultdict(list))
    dicoGeneralChromosomeValues=(lambda:defaultdict(list))

    #print(dicoGenePlage)
    #print(type(dicoGlobPlageType))
    #print(dicoGenePlage)

    for plage,listGene in dicoGenePlage.items():
        geneNumberPlage=len(listGene)
        listNumberGenePlage.append([geneNumberPlage,plage])
        
        for geneobj in listGene:
            gene=geneobj.obj_dict()
            dicoGlobPlageType[plage]["Gene"].append(gene)
            #dicoGeneralChromosomeValues[plage]["Gene"].append(listNumberGenePlage)
    #print(listNumberGenePlage)
    #print(dicoGeneralChromosomeValues)
    for plage,listMiscRna in dicoMiscRnaPlage.items():
        MiscRnaNumberPlage=len(listMiscRna)
        listNumberMiscRnaPlage.append([MiscRnaNumberPlage,plage])
        

        for MiscRnaObj in listMiscRna :
            miscrna=MiscRnaObj.obj_dict()
            dicoGlobPlageType[plage]["Misc_rna"].append(miscrna)
    
    #print(dicoMrnaPlage)
    
    for plage,listMrna in dicoMrnaPlage.items():
        mRnaNumberPlage=len(listMrna)
        listNumberMrnaPlage.append([mRnaNumberPlage,plage])
        #print('PlageDebug',plage)
        for MrnaObj in listMrna :
            mrna=MrnaObj.obj_dict()
            dicoGlobPlageType[plage]["Mrna"].append(mrna)
    
    for plage,listCds in dicoMrnaPlage.items():
        CdsNumberPlage=len(listCds)
        listNumberCDSPlage.append([CdsNumberPlage,plage])
        for CdsObj in listCds :
            cds=CdsObj.obj_dict()
            dicoGlobPlageType[plage]["CDS"].append(cds)



    #print(listNumberGenePlage)
    #print(listNumberMiscRnaPlage)
    #print(listNumberMrnaPlage)

# Stockage des variables et ecriture de l'objet generalChromosomeValues
    
    #geneNumber=len(list_gene)
    #miscRnaNumber=len(list_miscRna)
    #mRnaNumber=len(list_mRNA)
    #cdsNumber=len(list_CDS)
    #totalNumberSegments=geneNumber+miscRnaNumber+mRnaNumber+cdsNumber
    #totalBoxes=geneNumber+totalMiscRnaBoxes+totalMrnaBoxes+totalCdsBoxes

    
   
    #print(dico4)
    #print("coucou")
    #print(listNumberMrnaPlage)
    #print(listNumberGenePlage)
    
    
    #!!!
    
    for i in range(len(listNumberGenePlage)):
        geneNumber=listNumberGenePlage[i][0]
        miscRnaNumber=listNumberMiscRnaPlage[i][0]
        mRnaNumber=listNumberMrnaPlage[i][0]
        cdsNumber=listNumberCDSPlage[i][0]
        totalNumberSegments=geneNumber+miscRnaNumber+mRnaNumber+cdsNumber
        totalBoxes=geneNumber+totalMiscRnaBoxes+totalMrnaBoxes+totalCdsBoxes
        
        #print(geneNumber)
        #print(listNumberGenePlage[i][0])
    

        generalChromosomeValues=GeneralChromosomeValues(info_species,genomeref,numerochromosome,start_chromosome,end_chromosome,totalNumberSegments,totalBoxes,geneNumber,cdsNumber,totalCdsBoxes,miscRnaNumber,totalMiscRnaBoxes,mRnaNumber,totalMrnaBoxes)
        jsonChromosomeValues=generalChromosomeValues.obj_dict()
        dicoGlobPlageType[listNumberGenePlage[i][1]]["GeneralChromosomeValues"].append(jsonChromosomeValues)
        #dicoGlobPlageType[plage]["GeneralChromosomeValues"].append(jsonChromosomeValues)
    #print(dicoGlobPlageType)
    

    #boitesfoncJson=BoitesFonctionnelles(jsonChromosomeValues,listObjgene,listObjMiscRNA,listObjMrna,listObjCds)
    #print(listPlage)
    #print(dico4)
    #print(dicoPosition)
        
        #for liste in dico4["Misc_rna"]:
        #print(liste["Note"])
        

    print('--------------------------------------------Ecriture JSON Du Parsing----------------------------------------------------------')
    localPathExit = result+"/"+espece+"/"+str(listPlage)+"/"
    #exit(listPlage)
    localPathExit=cleanspace(localPathExit)

    print("CHEMIN RESULTAT CORREC",result)
    print("Chemin SORTIE JSON",localPathExit)
    
    if not os.path.exists(localPathExit):
        os.makedirs(localPathExit)
    
    logging.info("Le fichier de sortie Json est creer")
    os.chdir(localPathExit)

    try:
        with open("chromosome"+numerochromosome+".json","w",encoding="utf-8") as fichier:
            json.dump(dicoGlobPlageType,fichier,indent=2)
            print(dicoGlobPlageType)
            fichier.close()

    except:
        logging.error("Error Writting Files")



