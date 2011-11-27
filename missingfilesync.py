#!/usr/bin/python

import os
import sys
import shutil

def usage():
	print 'Missing File Sync (c) Gad Berger 2011\n'
	print 'Usage: python missingfilesync.py [sourcefolder] [destfolder]'
	print ''
	print 'Missing File Sync is a script that only copies new files to a destination'
	print 'folder. Files with the same name and path will not be copied.'
	print ''
	print 'sourcefolder    Folder containing the files you want to sync'
	print 'destfolder      Folder that you want to update with new files'
	print ''
	print 'ex:'
	print '\tpython missingfilesync.py "c:\User\Me\Amazon MP3" "e:\Music\Amazon MP3"'

def copyfile(filename, srcfolder, dstfolder):
	# create the folder
	if not os.path.exists(dstfolder):
		os.makedirs(dstfolder)
	
	srcfile = os.path.join(srcfolder, filename)
	dstfile = os.path.join(dstfolder, filename)
	
	shutil.copy2(srcfile, dstfile)

def main():
	if len(sys.argv) < 3:
		usage()
		sys.exit()

	print 'Missing File Sync (c) Gad Berger 2011\n'
	
	src = os.path.normpath(sys.argv[1])
	dst = os.path.normpath(sys.argv[2])
	
	try:
		# test that the source and destination paths exist
		if not os.path.exists(src):
			print 'Are you sure you typed the source folder in correctly?'
			exit(src)
		if not os.path.exists(dst):
			# try to create the directory
			print 'Creating destination folder', dst
			os.makedirs(dst)
	except (IOError, WindowsError), e:
		print 'Error accessing the source/destination folder or device'
		sys.exit()
	
	fileList = []
	
	# scan the destination path and save all details into a list
	for path, dirs, files in os.walk(dst):
		for filename in files:
			relpath = os.path.relpath(path, dst)
			file = os.path.join( relpath, filename )
			fileList.append( file )
		
	fileSet = set(fileList)

	for srcfolder, dirs, files in os.walk(src):
		relpath = os.path.relpath(srcfolder, src)
		dstfolder = os.path.join(dst, relpath)
		
		if len(files) > 0:
			print 'syncing', relpath, '...'

		for filename in files:
			file = os.path.join( relpath, filename )
			if file not in fileSet:
				copyfile(filename, srcfolder, dstfolder)
	
	print 'all done!'
	
if __name__ == "__main__":
	main()
