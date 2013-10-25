import shutil
import sys
import md5
import os
import exceptions
import subprocess
from tkMessageBox import askquestion
from tkFileDialog import askopenfilename
from tkSimpleDialog import askstring
from Tkinter import Tk
def rel(path):
    return os.path.join(os.path.dirname(__file__),path)
config = open(rel('gamelist.conf'), 'r').read()
data = eval(config)

Tk().withdraw()
ans  = askquestion("Image", "Do you want to enter a custom command? (otherwise we ask for a execudable)")

if ans == 'no':    
    cmd = askopenfilename() 
    cmd += askstring("Flags","Addional flags: ")
    if len(cmd)<1:
        print "pleas enter something next time"
        sys.exit(0)
else: 
    cmd = askstring("Command","Command: ")
     
title = askstring("Title","Title: ")
if len(title)<1:
    print "pleas enter something next time"
    sys.exit(0)
desc = askstring("Description","Description: ")
if len(desc)<1:
    print "pleas enter something next time"
    sys.exit(0)




ans  = askquestion("Image", "Do you want to add an cutom image?")

if ans == 'no':
    print "oke, we are done, tanx"
    img = "img/basic.bmp"
else: 
    ans  = askquestion("Image", "We can take a screenshot by starting the app and waiting some time do you want that? (Else you have to give a custom path))")
    img  = "img/"+str(md5.new(title).hexdigest())+".bmp"
    if ans == 'yes':
        time = askstring("Time","How long will you need to start the game?")
        os.system("scrot -d "+time+" "+rel(img)+" &")
        subprocess.call(cmd,shell=True)
        ans  = askquestion("Succes", "Did it work?")
        if ans != "yes":
            sys.exit(0)
    else: 
        path = askopenfilename()
        if len(path)<1:
            shutil.copyfile(path,img)

    
newd = {'title':title,'disc':desc,'cmd':cmd,'img':img}
data = [newd]+data


data =map(str,data)
f = open(rel("gamelist.conf"),"w")
f.write("[\n  ")
f.write(",\n  ".join(data))
f.write("\n]")
f.close()

