#!/usr/bin/python

import os, sys, shutil
import ConfigParser

def usage():
	print 'Missing File Sync (c) Gad Berger 2011\n'
	print 'Usage: python missingfilesync.py [configsection] [[sourcefolder] [destfolder]]'
	print ''
	print 'Missing File Sync is a script that only copies new files to a destination'
	print 'folder. Files with the same name and path will not be copied.'
	print ''
	print 'sourcefolder    Folder containing the files you want to sync'
	print 'destfolder      Folder that you want to update with new files'
	print ''
	print 'ex specifying directories directly:'
	print '\tpython missingfilesync.py "c:\User\Me\Amazon MP3" "e:\Music\Amazon MP3"'
	print ''
	print 'ex specifying config section:'
	print '\tpython missingfilesync.py sdcard'

def exit():
	sys.exit()
	
def copyfile(filename, srcfolder, dstfolder):
	# create the folder
	if not os.path.exists(dstfolder):
		os.makedirs(dstfolder)
	
	srcfile = os.path.join(srcfolder, filename)
	dstfile = os.path.join(dstfolder, filename)
	
	shutil.copy2(srcfile, dstfile)

def readconfig(section):
	try:
		config = ConfigParser.ConfigParser()
		if len(config.read('mfs.cfg')) == 0:
			print 'Boo hoo, I could not find the config file "mfs.cfg".'
			print 'Make sure you are running this script in the same folder as the config file'
			exit()
			
		src = config.get(section, "sourcefolder")
		dst = config.get(section, "destfolder")
	except ConfigParser.NoOptionError, e:
		print 'Did not find one of the required sections in the configuration file'
		print e.message
		exit()
		
	return (src, dst)

def main():
	print 'Missing File Sync (c) Gad Berger 2011\n'
	
	if len(sys.argv) == 2:
		# try to get the folders from the config file
		(src, dst) = readconfig(sys.argv[1])
		
		# and just in case someone puts the strings in quotes .. like I did :)
		src = src.replace('\"', '')
		dst = dst.replace('\"', '')
	elif len(sys.argv) == 3:
		src = sys.argv[1]
		dst = sys.argv[2]
	else:
		usage()
		exit()

	# normalize the paths so windows strings work
	src = os.path.normpath(src)
	dst = os.path.normpath(dst)
	
	try:
		# test that the source and destination paths exist
		if not os.path.exists(src):
			print 'Are you sure you typed the source folder in correctly?'
			exit()
		if not os.path.exists(dst):
			# try to create the directory
			print 'Creating destination folder', dst
			os.makedirs(dst)
	except (IOError, WindowsError), e:
		print 'Error accessing the source/destination folder or device'
		exit()
	
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
