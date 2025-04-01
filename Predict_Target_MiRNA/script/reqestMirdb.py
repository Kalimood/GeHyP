#!/usr/bin/envpython3
#coding: utf-8

import requests
import time
import os
import csv
import json
import pandas as pd
from bs4 import BeautifulSoup
from collections import defaultdict

#with requests.Session() as s:
urlMining='http://mirdb.org/mirdb/mining.html'
urlTableau='http://mirdb.org/cgi-bin/mining.cgi'

requests.get(urlMining)
interMir={'searchType':'miRNA','FuncMir':'ON','excludeGene':'ON','minScore':'60','excludeMir':'ON','maxTarget':'2000','species':'Human','miRsample':'on','searchBox':'hsa-let-7a-5p,hsa-miR-1-3p,hsa-miR-9-3p','submitButton':'Go'}
reponse=requests.post(urlTableau,data=interMir)
#print(reponse.text)


if reponse.ok:
    dfs=pd.read_html(reponse.text,header=None)
    dfInteract=dfs[1]
    header=dfInteract.head(1)
    header=header.values.tolist()[0]
    #print(header)

    #dfInteract=pd.DataFrame([dfInteract],columns=header)
    dfInteract.columns=header
    dfInteract.drop(0,0,inplace=True)
    del dfInteract['Target Detail']


    requestURL = "https://www.ebi.ac.uk/proteins/api/proteins/interaction/HACD3"
    r = requests.get(requestURL, headers={ "Accept" : "application/json"})
        
      #pathUniprot='/home/kevin/Bureau/StageM2/Scripttest/UniprotInteractomics'
    if not r.ok:
        r.raise_for_status()
            #continue

    responseBody = r.text
    pritn(responseBody)
    print(dfInteract.head(10))
    #dfInteract.iloc[]
    #dfInteract.loc[[:, ["1", "2", "3","4","5"]]
    
    #dfInteract.loc[df.index[n], 'Btime'] = x

    #print(dfInteract)

    
    
'''
for df in dfs:
    print(df[2])
#print('dataframe1',df[0])
#print('dataframe2',df[1])
#df.drop(['Target Detail'],axis=1)
'''



'''
results2=defaultdict(list)
results=[]
infostr=[]
if reponse.ok:
    soup=BeautifulSoup(reponse.text,'html.parser')
    table=soup.find("table",id='table1')
    tablerows=table.find_all('tr')[1:]
    tableheaders=table.find_all('b')[1:]
    for i in tableheaders:
        header=i.text
        print(header)
    for tr in tablerows:
        #infostr.append(tr)
        tds=tr.find_all('td')[1:]

        for td in tds:
            row=td.text
            
            print(row)
            results.append(row)
    
#print(results)
    
'''




'''
données formulaire
searchType	"miRNA"
FuncMir	"ON"
excludeGene	"ON"
minScore	"60"
excludeMir	"ON"
maxTarget	"2000"
species	"Human"
miRsample	"on"
searchBox	"hsa-let-7a-5p,+hsa-miR-1-3p,+hsa-miR-9-3p"
submitButton	"Go"
'''