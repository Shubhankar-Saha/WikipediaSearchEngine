
# coding: utf-8

# In[1]:


import re
import os
import nltk
import sys
import time


# In[2]:


titleIndexing=dict()
textIndexing=dict()
categoryIndexing=dict()
start = time.time()
infoboxIndexing=dict()


# In[3]:


pageCount=0
xmlData=sys.argv[1]
folderPath=sys.argv[2]
# xmlData="/home/dhawal/Downloads/IRE/wikidata.xml"

import xml.etree.cElementTree as et
con=et.iterparse(xmlData,events=("start","end"))


# **The iter() method creates an object which can be iterated one element at a time**

# In[4]:


con=iter(con)


# In[5]:


import re
import nltk
stemmer = nltk.stem.SnowballStemmer('english')
pageCount=0


# In[6]:


stop_words = {}
reg = re.compile("\"|,| ")
sum_text=0
stop_file = open("Stop_words.txt", "r")
content = stop_file.read()
content = re.split(reg, content)
sum_title=0
for word in content :
    if word :
        stop_words[word] = True


# In[7]:


titleFp = open(folderPath+"/title_tags.txt", "w")


# In[8]:


titlePosition=[]


# In[9]:


def buildFileIndexFormat(word,postingList):
    value=",".join(postingList)
    index=word+"-"+value
    index+="\n"
    return index
    


# In[10]:


def indexFileWrite(typeOfIndex):
    global titleIndexing
    global textIndexing
    global categoryIndexing
    global infoboxIndexing
    if typeOfIndex=="category":
        file = folderPath+ "/category" + ".txt"
        outfile = open(file, "w")
        for word in sorted(categoryIndexing):
            index=buildFileIndexFormat(word,categoryIndexing[word])
            outfile.write(index)
        outfile.close()
        
    if typeOfIndex=="infoBox":
        file = folderPath+ "/infoBox" + ".txt"
        outfile = open(file, "w")
        for word in sorted(infoboxIndexing):
            index=buildFileIndexFormat(word,infoboxIndexing[word])
            outfile.write(index)
        outfile.close()
        
    if typeOfIndex=="title":
        file = folderPath+ "/title" + ".txt"
        outfile = open(file, "w")
        for word in sorted(titleIndexing):
            index=buildFileIndexFormat(word,titleIndexing[word])
            outfile.write(index)
        outfile.close()
            
    if typeOfIndex=="text":
        file = folderPath+"/text" + ".txt"
        outfile = open(file, "w")
        for word in sorted(textIndexing):
            index=buildFileIndexFormat(word,textIndexing[word])
            outfile.write(index)
        outfile.close()


# In[11]:


def buildIndex(wordCountDict,pageCount,typeOfDataSegment):
    global titleIndexing
    global textIndexing
    global categoryIndexing
    global infoboxIndexing
    for word in wordCountDict:
        wordCount=str(wordCountDict[word])
        pageNo=str(pageCount)
        wordPageCount=pageNo+":"+wordCount
        if typeOfDataSegment == "title":
            if word not in titleIndexing:
                titleIndexing[word]=[]
            titleIndexing[word].append(wordPageCount)
        
        if typeOfDataSegment == "infoBox":
            if word not in infoboxIndexing:
                infoboxIndexing[word]=[]
            infoboxIndexing[word].append(wordPageCount)
            
        if typeOfDataSegment == "text":
            if word not in textIndexing:
                textIndexing[word]=[]
            textIndexing[word].append(wordPageCount)
            
            
        if typeOfDataSegment == "category":
            if word not in categoryIndexing:
                categoryIndexing[word]=[]
            categoryIndexing[word].append(wordPageCount)
        
#     if typeOfDataSegment == "text":
#         print(len(textIndexing))


# In[12]:


for event, elem in con:
#     print(event)
#     print(elem.tag)
#     replace {} everything in between this by empty we get just tagname
    tag=re.sub(r"{.*}","",elem.tag)
#     print(tag)
    if event =="start":
        if tag=="page":
            categoryCount={}
            titleWords={}
            pageCount+=1
            infoBoxWordCount={}
            remainingText={}
#             print("x")
    elif event == "end":
        if tag == "text":
#             print("x")
            text=elem.text
#             text=text.lower()
#             print(text)
            try :
                category=re.findall("\[\[Category:(.*?)\]\]",text)
                pattern = re.compile("[^a-zA-Z]")
                for lines in category:
    #                 print("x")
                    count1=0
                    words=re.split(pattern,lines)
                    for word in words:
                        word=stemmer.stem(word.lower())
                        if word in stop_words:
                            continue
                        elif word=="":
                            continue
                        elif word not in categoryCount:
                            categoryCount[word]=0
                        categoryCount[word]=categoryCount[word]+1
    #             print(categoryCount)
                infoBox = re.findall("{{Infobox(.*?)}}", text)
                pattern = re.compile("[^a-zA-Z]")
                for lines in infoBox:
    #                 print("x")
                    words=re.split(pattern,lines)
                    count1=0
                    for word in words:
                        word=stemmer.stem(word.lower())
                        if word in stop_words:
                            continue
                        elif word=="":
                            continue
                        elif word not in infoBoxWordCount:
                            infoBoxWordCount[word]=0
                        infoBoxWordCount[word]=infoBoxWordCount[word]+1
            except:
                pass
            
            try:
                text = text.lower();
                words=re.split(pattern,text)
                for word in words:
#                     word=word.lower()
                    word=stemmer.stem(word)
                    if word in stop_words:
                        continue
                    elif word=="":
                        continue
                    elif word not in remainingText:
                        remainingText[word]=0
                    remainingText[word]=remainingText[word]+1 
            except:
                pass
                    
        elif tag=="title":
            text=elem.text
            if text!="":
                title=text
                title+="\n"
                text=text.lower()
                titlePosition.append(titleFp.tell())
                titleFp.write(title)
                pattern = re.compile("[^a-zA-Z]")
                words=re.split(pattern,text)
                for word in words:
#                     word=word.lower()
                    word=stemmer.stem(word)
                    if word in stop_words:
                        continue
                    elif word=="":
                        continue
                    elif word not in titleWords:
                        titleWords[word]=0
                    titleWords[word]=titleWords[word]+1 
                    
        if tag=="page":
#             print("title",len(titleWords))
#             print("text",len(remainingText))
            sum_text=sum_text+len(remainingText)
            sum_title=sum_title+len(titleWords)
            buildIndex(titleWords,pageCount,"title")
            buildIndex(remainingText,pageCount,"text")
            buildIndex(infoBoxWordCount,pageCount,"infoBox")
            buildIndex(categoryCount,pageCount,"category")
        elem.clear() 


# In[13]:


# print(sum_text)
# print(sum_title)


# In[14]:


# titleIndexing


# In[15]:


import pickle
file = open(folderPath+"/titlePositions.pickle", "wb")
pickle.dump(titlePosition, file)
file.close()


# In[16]:


indexFileWrite("category")
indexFileWrite("infoBox")
indexFileWrite("title")
indexFileWrite("text")


# In[17]:


# print(len(categoryIndexing))
# print(len(titleIndexing))
# print(len(infoboxIndexing))
# print(len(textIndexing))


# In[18]:


wordPosition={}


# In[19]:


def writePostingList(fp,fp1,f):
    lineNo=0
    for line in fp.readlines():
        pos=line.find("-")
        word = line[:pos]
        flag=0
        posting_list = line[pos+1:]
        if word not in wordPosition:
            flag=1
        if flag==1:
            wordPosition[word] = {}
        wordPosition[word][f] =lineNo
        x=len(posting_list)
        lineNo+=x;
        fp1.write(posting_list)
    return fp,fp1


# In[20]:


import os


# In[21]:


file = folderPath+"/title.txt"
file1 = folderPath+"/titlePosting.txt"
fp = open(file, "r")
fp1 = open(file1, "w+")
fp,fp1=writePostingList(fp,fp1,"t")
fp1.close()
fp.close()
os.remove(folderPath+"/title.txt")

file = folderPath+"/category.txt"
file1 = folderPath+"/categoryPosting.txt"
fp = open(file, "r")
fp1 = open(file1, "w+")
fp,fp1=writePostingList(fp,fp1,"c")
fp1.close()
fp.close()
os.remove(folderPath+"/category.txt")

file = folderPath+"/infoBox.txt"
file1 = folderPath+"/infoBoxPosting.txt"
fp = open(file, "r")
fp1 = open(file1, "w+")
fp,fp1=writePostingList(fp,fp1,"i")
fp1.close()
fp.close()
os.remove(folderPath+"/infoBox.txt")

file = folderPath+"/text.txt"
file1 = folderPath+"/textPosting.txt"
fp = open(file, "r")
fp1 = open(file1, "w+")
fp,fp1=writePostingList(fp,fp1,"d")
fp1.close()
fp.close()
os.remove(folderPath+"/text.txt")


# In[ ]:






# In[22]:


# wordPosition
# print(len(wordPosition))


# In[23]:


file = open(folderPath+"/wordPositions.pickle", "wb")
pickle.dump(wordPosition, file)
file.close()
end = time.time()
print("Index Build in - " + str(end - start) + "s")
