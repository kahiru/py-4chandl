#!/usr/bin/env python
import getopt
import urllib
import re
import sys
import os.path
import json
import inspect

def jlistthread(thread,board,x,y):
    """Get links to images in a thread and return them as a list
    returns list of URLs or 1 when an error was encountered

    """
    patt=re.compile('p(\d*)$')
    thread=re.search(patt,thread).group(1)
    try:
        link=urllib.urlopen('http://api.4chan.org/'+board+'/res/'+thread+'.json')
    except IOError:
        sys.stderr.write('URL IOError - thread not found/not connected to internet\n')
        exit(1)
    images=list()
    data=link.read()
    data=json.loads(data)
    data=data['posts']
    skip=0
    for each in data:
	    try:
		if int(each['w'])<int(x):
			if int(each['h'])<int(y) or y==-1:
				sys.stdout.write((str(each['tim'])+each['ext']+' [ '+str(each['w'])+'x'+str(each['h'])+' ]\t'+'[ SKIPPED AS LOWRES]\n'))
				skip+=1
				continue
	    	images.append((str(each['tim'])+each['ext'],(each['w'],each['h'])))
	    except KeyError:
		continue
    return (images,skip)

def dlimage(image,board):
    """Downloads image specified as link and shows progressbar."""
    link='http://images.4chan.org/'+board+'/src/'+image[0]
    if (os.path.isfile(image[0])):
        sys.stdout.write(image[0]+' [ '+str(image[1][0])+'x'+str(image[1][1])+' ]\t'+'[ SKIPPED ]\n')
        sys.stdout.flush()
        return 1
    imgsrc=urllib.urlopen(link)
    size=imgsrc.headers.get("content-length")
    output=open(image[0],'wb')
    size=int(size)//20
    sys.stdout.write(image[0]+' [ '+str(image[1][0])+'x'+str(image[1][1])+' ]\t[')
    for i in range(20):
        output.write(imgsrc.read(size))
        sys.stdout.write('.')
        sys.stdout.flush()
    sys.stdout.write(']\n')
   
    output.close()
    return 0

def main(thread,folder,x,y):
    count=0
    print(folder)
    if thread=='':
        thread=raw_input('Thread link: ')
    board=thread[24:]
    patt=re.compile('(.*?)/')
    board=re.search(patt,board).group(1)
    images,skip=jlistthread(thread,board,x,y)
    if len(images)==0:
        sys.stderr.write('No images found. Exitting...')
        exit(0)
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chdir(folder)
    for image in images:
        temp=dlimage(image,board)
        if temp==0:
            count+=1
        else:
            skip+=1
    print('----------------------------------------------------------')
    print('DL complete - '+str(count)+' files.')
    print('Skipped '+str(skip)+' files.')

def printhelp():
    print('4chandl.py [ LINK ] [ FOLDER ]')
    print('Downloads all images from specified thread into the FOLDER.')
    print('If no LINK is specified, script asks for one.')
    print('If no FOLDER is specified, script downloads images to current folder')

if __name__=='__main__':
	optlist,args=getopt.getopt(sys.argv[1:], "x:y:hv", ['help','verbose'])
	x=y=-1
	for o, a in optlist:
		if o in ('-v', '--verbose'):
			verbose=True
		elif o in ('-x'):
			x=a
			print(x)
		elif o in ('-y'):
			print(a)
			y=a
		elif o in ('--help','-h'):
			printhelp()
			sys.exit()
	if len(args)==2:
		folder=args[1]
		link=args[0]
	elif len(args)==1:
		folder='./'
		link=args[0]
	else:
		printhelp()
		sys.exit()
	main(link,folder,x,y)
