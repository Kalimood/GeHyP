def download(espece,result):
	ftp = ftplib.FTP('ftp.ensembl.org')
	ftp.login()
	ftp.cwd('/pub/release-104/regulation/'+espece)
	files=ftp.nlst()
	
	local_Destination_Path = result+"/"+espece +"/"
	urlName='http://ftp.ensembl.org/pub/release-104/regulation/'+espece+'/'

	if not os.path.exists(local_Destination_Path):
		os.makedirs(local_Destination_Path)
	else:
		logging.info(local_Destination_Path,"The directory is already created")

	os.chdir(local_Destination_Path)
	#exit(files)
	
	for fichier in files:
		if fichier.endswith('.gz'):
			chromosome=fichier
			chromosomeShort = os.path.splitext(chromosome)[0]
			local_filenames=os.listdir(local_Destination_Path)
			if chromosomeShort in local_filenames:
				print(chromosomeShort,"is already downloaded")
				print("Francois le BOSS")
			else:
				logging.error("Opening",(urlName)+ ":::" +chromosome)
				try:
					print("On va s'en sortir")
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