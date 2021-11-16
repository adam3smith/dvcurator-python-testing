#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
import requests
import os

def get_citation(host, doi, token):
	# Scrape data and metadata from dataverse
	key = {'X-Dataverse-Key': token}
	dataset_url = 'https://' + host 
	dataset_url += '/api/datasets/:persistentId/?persistentId=' + doi
	dataset = requests.get(dataset_url, headers=key)
	citation=dataset.json()['data']['latestVersion']['metadataBlocks']['citation']['fields']
	fields = [] # Make an index of all the metadata fields
	values = []
	for entry in citation:
		fields.append(entry['typeName'])
		values.append(entry['value'])
	return dict(zip(fields, values)) 

def download_dataset(host, doi, token, folder_name, dropbox):
	import urllib.request
	import zipfile

	folder_path = 'QDR Project - ' + folder_name
	folder_path = os.path.join(dropbox, folder_path)
	
	edit_path = os.path.join(folder_path, "QDR Prepared")
	if not os.path.exists(folder_path):
		os.makedirs(edit_path) # Creates parents as well
		print("Directory '%s' created" %folder_path)

	zip_url = 'https://' + host
	zip_url += '/api/access/dataset/:persistentId/?persistentId=' + doi
	zip_url += '&key=' + token
	zip_path = os.path.join(folder_path, "Original Deposit.zip")
	zip_return = urllib.request.urlretrieve(zip_url, zip_path)
	print("Original archive downloaded to '%s'" %zip_path)

	with zipfile.ZipFile(zip_path, 'r') as zip_ref:
		zip_ref.extractall(edit_path)
		print("Archive files extracted to '%s'" %edit_path)
		
	os.remove(os.path.join(edit_path, 'MANIFEST.TXT'))
	return edit_path
