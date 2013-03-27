#!/bin/env python
import urllib
import re
import sys
import os.path
import json

def jlistthread(thread,board):
    """Get links to images in a thread and return them as a list
    returns list of URLs or 1 when an error was encountered

    """
    thread=thread[-8:]
    try:
        link=urllib.urlopen('http://api.4chan.org/'+board+'/res/'+thread+'.json')
    except IOError:
        sys.stderr.write('URL IOError - thread not found/not connected to internet\n')
        exit(1)
    images=list()
    data=link.read()
    data=json.loads(data)
    data=data['posts']
    for each in data:
	    try:
	    	images.append(str(each['tim'])+each['ext'])
	    except KeyError:
		continue
    return images

def dlimage(image,board):
    """Downloads image specified as link and shows progressbar."""
    link='http://images.4chan.org/'+board+'/src/'+image
    if (os.path.isfile(image)):
        sys.stdout.write(image+'\t'+'[ SKIPPED ]\n')
        sys.stdout.flush()
        return 1
    imgsrc=urllib.urlopen(link)
    size=imgsrc.headers.get("content-length")
    output=open(image,'wb')
    size=int(size)//20
    sys.stdout.write(image+'\t[')
    for i in range(20):
        output.write(imgsrc.read(size))
        sys.stdout.write('.')
        sys.stdout.flush()
    sys.stdout.write(']\n')
    output.close()
    return 0

def main(thread='',folder='./'):
    count=0
    skip=0
    if thread=='':
        thread=raw_input('Thread link: ')
    board=thread[24:]
    patt=re.compile('(.*?)/')
    board=re.search(patt,board).group(1)
    images=jlistthread(thread,board)
    if len(images)==0:
        sys.stderr.write('No images found. Exitting...')
        exit(0)
    if not os.path.exists(folder):
        os.makedirs(folder)
        os.chdir(folder)
    print(folder)
    for image in images:
        temp=dlimage(image,board)
        if temp==0:
            count+=1
        else:
            skip+=1
    print('-----------------------------------')
    print('DL complete - '+str(count)+' files.')
    print('Skipped '+str(skip)+' files.')

def printhelp():
    print('4chandl.py [ LINK ] [ FOLDER ]')
    print('Downloads all images from specified thread into the FOLDER.')
    print('If no LINK is specified, script asks for one.')
    print('If no FOLDER is specified, script downloads images to current folder')

if __name__=='__main__':
    if len(sys.argv)==1:
        main()
    elif len(sys.argv)==2:
        if sys.argv[1]=='--help':
            printhelp()
        else:
            main(sys.argv[1])
    elif len(sys.argv)==3:
        main(sys.argv[1],sys.argv[2])
    else: print('Execute 4chandl.py --help for invocation details.')

