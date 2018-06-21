#!/usr/bin/env python
import sys
import os
from os.path import basename
import zipfile
import re
import filecmp
from datetime import datetime
from os.path import getmtime
import time

# Given directories and list of the files found inside the directories.

dirlist=[]
filelist=[]

# Option Control Variables

isNextZip = False
zipOption = False
zipFilename = ""
isNextSm = False
isNextBg = False
isNextBefore = False
isNextAfter = False
noFileList = False
deleteOption = False
isNextPattern = False
patternOption = False
dupcontOption = False
dupnameOption = False
statsOption = False
bgOption = False
smOption = False
bigger = ""
smaller = ""
beforeOption = False
afterOption = False
traversedFileCount = 0
traversedFileSize = 0
foundFileCount = 0
foundFileSize = 0
uniqFileCount = 0
uniqFileSize = 0


# Iterate over the given arguments. Catch options into their respective variables, put directories to dirlist.

for i,param in enumerate(sys.argv):
	if isNextZip == True:
		isNextZip = False
		zipFilename = param
		continue
	if isNextPattern == True:
		isNextPattern = False
		pattern = re.compile(param)
		continue
	if isNextSm == True:
		isNextSm = False
		smaller = param
		continue
	if isNextBg == True:
		isNextBg = False
		bigger = param
		continue
	if isNextAfter == True:
		isNextAfter = False
		after = param
		continue
	if isNextBefore == True:
		isNextBefore = False
		before = param
		continue
	if i==0:
		pass
	elif param[0]=='-': # If a parameter starts with - it is an option.
		if param=='-zip':
			isNextZip = True
			zipOption = True
		if param=='-match':
			isNextPattern = True
			patternOption = True
		if param=='-nofilelist':
			noFileList = True
		if param=='-delete':
			deleteOption = True
		if param=='-duplcont':
			dupcontOption = True
		if param=='-duplname':
			dupnameOption = True
		if param=='-stats':
			statsOption = True
		if param=='-smaller':
			isNextSm = True
			smOption = True
		if param=='-bigger':
			isNextBg = True
			bgOption = True
		if param=='-before':
			isNextBefore = True
			beforeOption = True
		if param=='-after':
			isNextAfter = True
			afterOption = True			
	else:
		dirlist.append(param)
		
if not dirlist:
	dirlist.append(".")

for param in dirlist: # Call os.walk on directories. Add all found files to filelist.
	if os.path.isdir(param):
		for root, directories, filenames in os.walk(param):
			for filename in filenames:
				if os.path.join(root,filename) not in filelist:
					traversedFileCount+=1 #Keep data for -stats option.
					traversedFileSize+=os.path.getsize(os.path.join(root,filename))
					filelist.append(os.path.join(root,filename))
	else:
		print "Directory " + param + " does not exist."

if patternOption: # Remove the files that doesn't match the given regex.
	filelist = [x for x in filelist if pattern.match(basename(x))]

# A basic disjoint-set implementation for grouping duplicates.
def climb(wh,arr):
	if arr[wh]!=wh:
		arr[wh] = climb(arr[wh],arr)
	return arr[wh]

def merge(wh,wh2,arr):
	arr[climb(wh,arr)] = climb(wh2,arr)

# Get the time of modification of a file and translate it into the correct format.
def myTime(file):
	str1 = time.ctime(os.path.getmtime(file)) # Fri Jun 07 16:54:31 2013
	datetime_object = datetime.strptime(str1, '%a %b %d %H:%M:%S %Y')
	return datetime_object.strftime("%Y%m%dT%H%M%S") # 06/07/2013

# Multipliers for the size suffixes.
units = {"B":1, "K": 10**3, "M": 10**6, "G": 10**9, "T": 10**12}

# Parse the read filesize to bytes. 
def parseSize(sizeofile):
	unit = "B"
	if str.isalpha(sizeofile[len(sizeofile)-1]):
		unit = sizeofile[len(sizeofile)-1]
		num = int(sizeofile[:-1])
	else:
		num = int(sizeofile)
	return int(float(num)*units[unit])

# Remove the files modified before/after the given times.
if beforeOption:
	filelist = [x for x in filelist if myTime(x)<before]

if afterOption:
	filelist = [x for x in filelist if myTime(x)>after]

# Remove the files bigger/smaller than the given sizes.
if bgOption:
	filelist = [x for x in filelist if os.path.getsize(x)>=parseSize(bigger)]

if smOption:
	filelist = [x for x in filelist if os.path.getsize(x)<=parseSize(smaller)]

# Uses the disjoint-set to group and sort the duplicate files.
if dupcontOption and not noFileList:
	dad = range(0,len(filelist))
	for i,param in enumerate(filelist):
		for j,param2 in enumerate(filelist):
			if (i<j and filecmp.cmp(param, param2, shallow=False)):
				merge(j,i,dad)
	grouplist = []
	for param in range(len(filelist)):
		grouplist.append([])

	for i,par in enumerate(dad):
		grouplist[climb(par,dad)].append(filelist[i])
	for gr in grouplist:
		if len(gr)>1:
			gr.sort()
			for fil in gr:
				print fil
			print "------"
		if len(gr)>0:
			# Keep the data for the -stats option.
			uniqFileCount += 1
			uniqFileSize += os.path.getsize(gr[0])

#Key for sorting groups by filename.
def compar(a):
	if(len(a) == 0):
		return '0'
	return basename(a[0])

# Uses the disjoint-set to group and sort the duplicate files.
if dupnameOption and not noFileList:
	dad = range(0,len(filelist))
	for i,param in enumerate(filelist):
		for j,param2 in enumerate(filelist):
			if (i<j and basename(param)==basename(param2)):
				merge(j,i,dad)
	grouplist = []
	for param in range(len(filelist)):
		grouplist.append([])
	for i,par in enumerate(dad):
		grouplist[climb(par,dad)].append(filelist[i])
	grouplist.sort(key=compar)
	for gr in grouplist:
		if len(gr)>1:
			gr.sort()
			for fil in gr:
				print fil
			print "------"
		if len(gr)>0:
			uniqFileCount += 1

for param in filelist: #Keep the data for -stats option.
	foundFileCount+=1
	foundFileSize+=os.path.getsize(os.path.join(root,param))

if not noFileList and not dupcontOption and not dupnameOption: #Print out the found files if parameters are correct.
	for param in filelist:
		print param

if statsOption and not noFileList: #Print out stats.
	print "Traversed file count: " + str(traversedFileCount)
	print "Traversed file size: " + str(traversedFileSize) + " bytes"
	print "Found file count: " + str(foundFileCount)
	print "Found file size: " + str(foundFileSize) + " bytes"
	if dupcontOption:
		print "Unique file count: " + str(uniqFileCount)
		print "Unique file size: " + str(uniqFileSize) + " bytes"
	if dupnameOption:
		print "Unique file count: " + str(uniqFileCount)

if zipOption: # Zip matching files into a zip.
	zipf = zipfile.ZipFile(zipFilename, 'w', zipfile.ZIP_DEFLATED)
	for param in filelist:
		zipf.write(param,basename(param))
	zipf.close()

if deleteOption: # Delete matching files.
	for param in filelist:
		os.remove(param)