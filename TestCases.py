'''
Updated on Sept 15, 2011

@name: Test Cases, tool for create test procedures
@author: Nicola Di Giorgio

Ver 1.0.2
'''


import time
from xml.dom import minidom


OUTPUT_FILE="testcase.txt"
XML_FILE=".\config.xml"


def pp(a,b):
  print a+' '+str(b)
  raw_input('press enter')
  
class testCase():
  
  def __init__(self):

    #instance variables
    self.name=''
    self.procedures=[]
    self.conf_base={}
    self.DELIMITER=''

    #open xml file

    tree=minidom.parse(XML_FILE)

    self.name=tree.documentElement.getAttribute("name") #read the test name

    
    #read the conf element
    conf=tree.getElementsByTagName("conf")[0]
     
    for i in conf.childNodes:
      if i.nodeName[0]=='#': continue
      try: self.conf_base[i.nodeName] =i.firstChild.data
      except: self.conf_base[i.nodeName] = ""
    self.conf_base['date']=time.ctime()


    #read the test procedures
    procedures=tree.getElementsByTagName("procedures")[0]
    for i in procedures.childNodes:
      if i.nodeName[0]=='#': continue
      self.procedures.append([i.getAttribute("name"),i.getAttribute("values").split(',')])

    #read the procedure delimiter
    self.DELIMITER=procedures.getAttribute("delimiter")
    
    self.writeFile(self.conf_base,self.procedures,'testcase_'+self.name+'.txt')


  def createListProcedures(self,procedures):

    #Formatta i casi

    procedure=[]
    for i in procedures:
      procedure.append(IterArray.iterAll(i))

    tmp1=[]
    for i in procedure:
  
      tmp2=[]
      for k in i:
        tmp2=tmp2+[str(k[0])+self.DELIMITER+str(k[1])] #merge
      tmp1.append(tmp2)
          
    
    listProcedures=IterArray.iterAll(tmp1)
    return listProcedures
    

  def writeFile(self,conf,procedures,outputFile=OUTPUT_FILE):

    header="=== TEST CASE: "+self.name+" ==="

    
    
    try:
      f=open(outputFile,'w')

      f.writelines(header+"\n\n")

      cfg=''
      #Stampa la configurazione
      for i in conf.iterkeys():
        cfg+=str(i)+': '+conf[i]+'\n'

      cfg+='\n'+IterArray.printPossibleProcedures(self.printArray(procedures))+'\n\n'

      f.writelines(cfg)

      #Stampa list procedures
      listProcedures=self.createListProcedures(procedures)

      f.writelines(IterArray.printArray(listProcedures))

      #createFile(header,cfg,IterArray.printArray(listCases))
    finally:
      f.close()


  def shuffleList(self,array):
    pass
  
  def printArray(self,array):
    newArray=[]
    for i in array:
      if type(i)==list:
        newArray.append(self.printArray(i))
      else: newArray.append(str(i))
    return newArray
    

class IterArray():

  @staticmethod
  def __join(a1,a2): #si aspetta due array
    nuovalista=[]
    for i in a1:
      
      for k in a2:
        if type(i)!=list:
          nuovalista.append([i,k])
        else:
          t=i[:]
          t.append(k)
          nuovalista.append(t)
    return nuovalista

  @staticmethod
  def iterAll(arr):
    if type(arr[0])==list: temp=arr[0] #you have to feed join with two arrays!
    else: temp=[arr[0]]
    
    for i in arr[1:]:
      temp=IterArray.__join(temp,i)
    return temp

  @staticmethod
  def printArray(arr,spacing=1):
    txt=''
    tmp=''
    for i in enumerate(arr):  
      try:
        if tmp!='':
          if i[1][0]!=tmp: txt+='\n';
      except: pass
      txt+=str(i[0]+1).ljust(4)+' '+str(i[1])+'\n'
      tmp=i[1][0];
    return txt

  @staticmethod
  def printPossibleProcedures(arr):
    txt='\nTest Procedures\n\n'
    for i in arr:
      txt+=str(i[0])+'=='+str(i[1])+'\n'
    return txt

if __name__=="__main__":
  testCase()

  

