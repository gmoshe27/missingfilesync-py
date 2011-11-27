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

def exit(folder):
	print folder
	sys.exit()

def copyfile(filename, srcfolder, dstfolder):
	# create the folder
	if not os.path.exists(dstfolder):
		os.makedirs(dstfolder)
	
	srcfile = os.path.join(srcfolder, filename)
	dstfile = os.path.join(dstfolder, filename)
	
	#print 'copying ' + srcfile + ' to ' + dstfile
	shutil.copy2(srcfile, dstfile)

def main():
	if len(sys.argv) < 3:
		usage()
		sys.exit()

	src = os.path.normpath(sys.argv[1])
	dst = os.path.normpath(sys.argv[2])
	
	try:
		# test that the source path exists
		if not os.path.exists(src):
			print 'Did you type in the source folder correctly?'
			exit(src)
	except (IOError, WindowsError), e:
		print 'Error accessing the source or device:'
		exit(src)
	
	try:
		# test the destination path
		if not os.path.exists(dst):
			# try to create the directory
			os.makedirs(dst)
	except (IOError, WindowsError), e:
		print 'Could not access or create the destination folder:'
		exit(dst)
	
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
		
		for filename in files:
			file = os.path.join( relpath, filename )
			if file not in fileSet:
				copyfile(filename, srcfolder, dstfolder)

if __name__ == "__main__":
	main()
