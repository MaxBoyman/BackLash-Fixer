import time
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()
init_time=time.time()
print("INOA, BackLash Fixer For Gcode\nhttps:\\tupa.ir\nPress Any Key to Cotinue")
input()
print("Enter Backlash For X Axis:")
Blx=float(input())
print("Enter Backlash For Y Axis:")
Bly=float(input())

with open("engrave.nc","r") as file :
    filedata = file.read()
    file.close()
first_ind=0
second_ind=0
x=0
num=filedata.count("G01")
print(num)
swchx=0
swchy=0

first_ind=filedata.find("G00 X",filedata.find("G00 X0")+1)
newdata=filedata[:first_ind]
filedata=filedata[first_ind:]
filedata=filedata.splitlines()


l=len(filedata)
print("Initial Lenght:",l)
printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


while x<l:

    filedata[x]=filedata[x].split(" ")
    # print(filedata[x])
    # printProgressBar(x, l, prefix = 'Stage One> Progress:', suffix = 'Complete', length = 100)
    x=x+1
print("Splited Lenght:",len(filedata))
n=0
x=0
while x<l:
    if len(filedata[x])>1:
        if "X" in filedata[x][1]:
            x1=float(filedata[x][1][1:])
            y1=float(filedata[x][2][filedata[x][2].find("Y")+1:])
            # print(x1,y1)
            if "X" in filedata[x+1][1]:
                x2=float(filedata[x+1][1][1:])
                y2=float(filedata[x+1][2][filedata[x+1][2].find("Y")+1:])
                n=1
                # print(x2,y2)
            elif "Z" in filedata[x+1][1]:
                if "M" in filedata[x+2][0]:
                    n=0
                else:
                    x2=float(filedata[x+2][1][1:])
                    y2=float(filedata[x+2][2][filedata[x+2][2].find("Y")+1:])
                    n=2
            elif "F" in filedata[x+1][1]:
                x2=float(filedata[x+4][1][1:])
                y2=float(filedata[x+4][2][filedata[x+4][2].find("Y")+1:])
                n=4
            else:
                n=0

            # print("X1:",x1,"Y1:",y1,"X2:",x2,"Y2:",y2,"Processed:",x)
            if n!=0:
                xt=x2
                if (x2<x1 and swchx==0):
                    swchx=-1
                elif (x2>x1 and swchx==0):
                    swchx=1
                elif (x2>x1 and swchx==1):
                    pass
                elif (x2<x1 and swchx==1):
                    x2=x2+Blx
                elif (x2<x1 and swchx==-1):
                    pass
                elif (x2>x1 and swchx==-1):
                    x2=x2-Blx
                else:
                    pass

                yt=y2
                if (y2<y1 and swchy==0):
                    swchy=-1
                elif (y2>y1 and swchy==0):
                    swchy=1
                elif (y2>y1 and swchy==1):
                    pass
                elif (y2<y1 and swchy==1):
                    y2=y2+Bly
                elif (y2<y1 and swchy==-1):
                    pass
                elif (y2>y1 and swchy==-1):
                    y2=y2-Bly
                else:
                    pass
            
            if n==1:
                # if f_except==True:
                #     newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
                #     f_except=False
                filedata[x+1][1]=str("X"+str("{0:.4f}".format(x2)))
                filedata[x+1][2]=str("Y"+str("{0:.4f}".format(y2)))
                # newdata=newdata+str(filedata[x+1][0])+" "+str(filedata[x+1][1])+" "+str(filedata[x+1][2])+"\n"
            elif n==2:
                # if f_except==True:
                #     newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
                #     f_except=False
                filedata[x+2][1]=str("X"+str("{0:.4f}".format(x2)))
                filedata[x+2][2]=str("Y"+str("{0:.4f}".format(y2)))
                # newdata=newdata+str(filedata[x+2][0])+" "+str(filedata[x+2][1])+" "+str(filedata[x+2][2])+"\n"
            elif n==4:
                # if f_except==True:
                #     newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
                #     f_except=False
                filedata[x+4][1]=str("X"+str("{0:.4f}".format(x2)))
                filedata[x+4][2]=str("Y"+str("{0:.4f}".format(y2)))
                # newdata=newdata+str(filedata[x+4][0])+" "+str(filedata[x+4][1])+" "+str(filedata[x+4][2])+"\n"
            else:
                pass
                # newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
    # else:
        # if len(filedata[x])==3:
        #     newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
        # elif len(filedata[x])==2:
        #     newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+"\n"
        # elif len(filedata[x])==1:
        #     newdata=newdata+str(filedata[x][0])+"\n"
        # else:
        #     newdata=newdata+"\n"

    
    # printProgressBar(x, l, prefix = 'Stage 2> Progress:', suffix = 'Complete', length = 100)
    x=x+1
x=0
while x<l:
    if len(filedata[x])==3:
        newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+" "+str(filedata[x][2])+"\n"
    elif len(filedata[x])==2:
        newdata=newdata+str(filedata[x][0])+" "+str(filedata[x][1])+"\n"
    elif len(filedata[x])==1:
        newdata=newdata+str(filedata[x][0])+"\n"
    else:
        newdata=newdata+"\n"
    printProgressBar(x, l, prefix = 'Stage 3> Progress:', suffix = 'Complete', length = 100)
    x=x+1

# print(newdata)
with open("Fixed.nc","x+") as file :
    file.seek(0)
    file.write(newdata)
    file.close()
print("\r\n")
print("Procces Finished. Time Elapsed:",time.time()-init_time)