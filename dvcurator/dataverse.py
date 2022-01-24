#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

def get_citation(host, doi, token=""):
	import requests
	
	# Scrape data and metadata from dataverse
	dataset_url = 'https://' + host 
	dataset_url += '/api/datasets/:persistentId/?persistentId=' + doi
	if (not token):
		dataset = requests.get(dataset_url)
	else:
		key = {'X-Dataverse-Key': token}
		dataset = requests.get(dataset_url, headers=key)
	citation=dataset.json()['data']['latestVersion']['metadataBlocks']['citation']['fields']
	fields = [] # Make an index of all the metadata fields
	values = []
	for entry in citation:
		fields.append(entry['typeName'])
		values.append(entry['value'])
	return dict(zip(fields, values)) 

def download_dataset(host, doi, token, folder_name, dropbox):
	import zipfile, os, requests #, urllib.request

	folder_path = 'QDR Project - ' + folder_name
	folder_path = os.path.join(dropbox, folder_path)
	
	edit_path = os.path.join(folder_path, "QDR Prepared")
	if not os.path.exists(folder_path):
		os.makedirs(edit_path) # Creates parents as well
		print("Directory '%s' created" %folder_path)

	zip_url = 'https://' + host
	zip_url += '/api/access/dataset/:persistentId/?persistentId=' + doi
	if token.strip():
		zip_url += '&key=' + token
	#print(zip_url)

	zip_path = os.path.join(folder_path, "Original Deposit.zip")
	r = requests.get(zip_url)
	with open(zip_path, 'wb') as outfile:
		outfile.write(r.content)
		
	#zip_return = urllib.request.urlretrieve(zip_url, zip_path)
	print("Original archive downloaded to '%s'" %zip_path)

	with zipfile.ZipFile(zip_path, 'r') as zip_ref:
		zip_ref.extractall(edit_path)
		print("Archive files extracted to '%s'" %edit_path)

	manifest = os.path.join(edit_path, 'MANIFEST.TXT')
	if (os.path.exists(manifest)):
		os.remove(manifest)
		
	return edit_path
