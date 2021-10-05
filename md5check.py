import os
import hashlib
import sys

##
#    #> md5check.py arg1 arg2
# Script's arguments:
#    arg1: path to the txt file with hash and filename to use as template //
#           File format: first column has hash number, second column file name
#    arg2: path to the check files // path to ISOs, Files, etc.... if is a file, then the script take a MD5hash

md5offiles=sys.argv[1] # md5offiles
path=sys.argv[2] # path to ISO
fileconut=0
okfiles=0
notok=0

#md5offiles='c:\\users\\power\\md5.txt'
#path='C:\\Users\\power\\git\\Python\\zFilePractice\\'
#path='C:\\Users\\power\\git\\Python\\'


def Read_Two_Column_File(file_name):
    thisdict = { }

    with open(file_name, 'r') as data:
        x = []
        y = []
        for line in data:
            p = line.split()
            thisdict.update({p[0]:p[1]})

    return thisdict



def checkmd5(arch):
    # File to check
    file_name = 'filename.exe'

    md5_object = hashlib.md5()
    block_size = 128 * md5_object.block_size
    a_file = open(arch, 'rb')

    chunk = a_file.read(block_size)
    while chunk:
        md5_object.update(chunk)
        chunk = a_file.read(block_size)

    md5_returned = md5_object.hexdigest()
    return md5_returned



def comparemd5(original_md5,md5_returned):
    if original_md5 == md5_returned:
        print ("MD5 verified.")
    else:
        print ("MD5 verification failed!.")



## Main Code

print("-----------------------")
print("-----------------------")
print("Reading template from ",md5offiles)
thisdict = Read_Two_Column_File(md5offiles)

print("Scanning folder ",path)
wrongfiles=[]
okhash=[]
with os.scandir(path) as i:
    for entry in i:
        if entry.is_file():
            md5returned=checkmd5(entry)
            fileconut=fileconut+1
            if md5returned in thisdict:
               # print("Correct match: ",entry, "MD5returned: ",md5returned,"found in MD5 in reference file: ",thisdict.get(md5returned) )
                okfiles=okfiles+1
                tmp="Correct Hash: "+str(entry)+ "MD5returned: "+md5returned+" found in MD5 in template file. "#+thisdict.get(md5returned)
                okhash.append(tmp)
            else:
                notok=notok+1
                tmp="Wrong Hash "+ str(entry)+"MD5returned: "+md5returned
                wrongfiles.append(tmp)

numberofelements=len(wrongfiles)
print()
print("-----------------------")
print("Scan Finish")

#print("Number of Correct File's hash according to template file: #", okfiles)
print(*okhash, sep="\n")
print(*wrongfiles, sep="\n")

print("Number of files Scanned: ",fileconut)
print("Number of Correct File's hash according to template file: #", okfiles)
print("Number of Wrong Hash not matching template:               #",numberofelements)

if (notok>=0):
    #print("Number List with Files not matching Hash according to template: #",numberofelements)
    sys.exit(1) # code 1, something is wrong
else:
    sys.exit(os.EX_OK) # code 0, all ok

