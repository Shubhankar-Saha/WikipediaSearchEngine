
# coding: utf-8

# In[1]:




# In[1]:


import re
import os
import sys
import time


# In[2]:


# In[2]:


titleIndexing=dict()
textIndexing=dict()
categoryIndexing=dict()
start = time.time()
infoboxIndexing=dict()


# In[3]:


# In[3]:


pageCount=0
# xmlData=sys.argv[1]
wordPosition={}
# folderPath=sys.argv[2]
# folderPath="IndexSize"
# xmlData="/home/dhawal/Downloads/Downloads_new/2018201065/wikidata.xml"
folderPath="/mnt/7274E81574E7D9BD/Windows.old/IndexSize"
xmlData="/mnt/7274E81574E7D9BD/Windows.old/wiki_final.xml"


# In[4]:


import xml.etree.cElementTree as et
con=et.iterparse(xmlData,events=("start","end"))


# **The iter() method creates an object which can be iterated one element at a time**

# In[4]:


# In[5]:


con=iter(con)


# In[5]:


# In[6]:


import re
import nltk
stemmer = nltk.stem.SnowballStemmer('english')
pageCount=0


# In[6]:


# In[7]:


stop_words = {}
reg = re.compile("\"|,| ")
sum_text=0
stop_file = open("/mnt/7274E81574E7D9BD/Windows.old/Stop_words.txt", "r")
# stop_file=open("Stop_words.txt", "r")
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


# In[8]:


def buildFileIndexFormat(word,postingList):
    value=",".join(postingList)
    index=word+"-"+value
    index+="\n"
    return index
    


# In[10]:


# In[9]:


def indexFileWrite(typeOfIndex,NoOfFile):
    global titleIndexing
    global textIndexing
    global categoryIndexing
    global infoboxIndexing
    if typeOfIndex=="category":
        lineNo=0
        file = folderPath+ "/categoryPosting" +str(NoOfFile)+ ".txt"
        f='c'
        outfile = open(file, "w")
        categoryIndexing2=sorted(categoryIndexing)
        # print(categoryIndexing2)
        for word in categoryIndexing2:
            # index=buildFileIndexFormat(word[0],word[1])
            index=buildFileIndexFormat(word,categoryIndexing[word])
            # outfile.write(index)
#             flag=0
#             if word not in wordPosition:
#                 flag=1
#             if flag==1:
#                 wordPosition[word] = {}
#             wordPosition[word][f] =lineNo
#             x=len(index)
#             lineNo+=x;
            outfile.write(index)
        outfile.close()
        
    if typeOfIndex=="infoBox":
        lineNo=0
        file = folderPath+ "/infoBoxPosting" +str(NoOfFile)+ ".txt"
        outfile = open(file, "w")
        f='i'
        infoboxIndexing2=sorted(infoboxIndexing)
        # print(infoboxIndexing2)
        for word in infoboxIndexing2:
            flag=0
            index=buildFileIndexFormat(word,infoboxIndexing[word])
            # print(word,infoboxIndexing2[word])
            # index=buildFileIndexFormat(word[0],word[1])
#             if word not in wordPosition:
#                 flag=1
#             if flag==1:
#                 wordPosition[word] = {}
#             wordPosition[word][f] =lineNo
#             x=len(index)
#             lineNo+=x;
            # print(index)
            outfile.write(index)
        outfile.close()
        
    if typeOfIndex=="title":
        lineNo=0
        file = folderPath+ "/titlePosting" +str(NoOfFile)+ ".txt"
        outfile = open(file, "w")
        f='t'
        titleIndexing2=sorted(titleIndexing)
        for word in titleIndexing2:
            index=buildFileIndexFormat(word,titleIndexing[word])
            # index=buildFileIndexFormat(word[0],word[1])
#             flag=0
#             if word not in wordPosition:
#                 flag=1
#             if flag==1:
#                 wordPosition[word] = {}
#             wordPosition[word][f] =lineNo
#             x=len(index)
#             lineNo+=x;
            outfile.write(index)
        outfile.close()
            
    if typeOfIndex=="text":
        lineNo=0
        file = folderPath+"/textPosting" +str(NoOfFile)+ ".txt"
        outfile = open(file, "w")
        f='d'
        textIndexing2=sorted(textIndexing)
        for word in textIndexing2:
            flag=0
            index=buildFileIndexFormat(word,textIndexing[word])
            # index=buildFileIndexFormat(word[0],word[1])
#             if word not in wordPosition:
#                 flag=1
#             if flag==1:
#                 wordPosition[word] = {}
#             wordPosition[word][f] =lineNo
#             x=len(index)
#             lineNo+=x;
            outfile.write(index)
        outfile.close()


# In[10]:


stemWord={}


# In[11]:


def removeAllHttp(text):
    regExp1 = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',re.DOTALL)
    text = regExp1.sub('',text)
    return text


# In[ ]:


def removeAllTextInnerCss(text):
    regExp2 = re.compile(r'{\|(.*?)\|}',re.DOTALL)
    text = regExp2.sub('',text)
    return text


# In[ ]:


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
            # text=removeAllTextInnerCss(str(text))
            
            
        if typeOfDataSegment == "category":
            if word not in categoryIndexing:
                categoryIndexing[word]=[]
            categoryIndexing[word].append(wordPageCount)
        
#     if typeOfDataSegment == "text":
#         print(len(textIndexing))


# In[ ]:


# In[12]:
NoOFFiles=1


# In[ ]:

# pattern = re.compile("[^a-zA-Z0-9]")
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
            # print(type(text))
            text=removeAllHttp(str(text))
            text=removeAllTextInnerCss(str(text))
#             text=text.lower()
#             print(text)
            try :
                category=re.findall("\[\[Category:(.*?)\]\]",text)
                pattern = re.compile("[^a-zA-Z0-9]")
                for lines in category:
    #                 print("x")
                    count1=0
                    words=re.split(pattern,lines)
                    for word in words:
                        if word not in stemWord:
                            stemWord[word]=stemmer.stem(word.lower())
                            word=stemWord[word]
                        else:
                            word=stemWord[word]
#                         word=stemmer.stem(word.lower())
                        n5=len(word)
                        if n5<3:
                            continue 
                        elif word in stop_words:
                            continue
                        elif word=="":
                            continue
                        elif word not in categoryCount:
                            categoryCount[word]=0
                        categoryCount[word]=categoryCount[word]+1
    #             print(categoryCount)
                # if pageCount==7815:
                #     print("befor", text)
                infoBox = re.findall("{{Infobox((.|\n)*?)}}",text)
                # if len(infoBox)>0:
                #     print(pageCount)
                #     print(text)
                # if pageCount==7815:
                #     print("befor", text)
                pattern = re.compile("[^a-zA-Z0-9]")
                for lines in infoBox:
    #                 print("x")
                    for tup in lines:
                        words=re.split(pattern,tup)
                        count1=0
                        for word in words:
                            if word not in stemWord:
                                stemWord[word]=stemmer.stem(word.lower())
                                word=stemWord[word]
                            else:
                                word=stemWord[word]
#                             word=stemmer.stem(word.lower())
                            n5=len(word)
                            if n5<3:
                                continue 
                            elif word in stop_words:
                                continue
                            elif word=="":
                                continue
                            elif word not in infoBoxWordCount:
                                infoBoxWordCount[word]=0
                            infoBoxWordCount[word]=infoBoxWordCount[word]+1


                # reference=re.findall("==References==(.|\n)*?==",text)
                # if(len(reference)>1):
                #     print(reference)
                # for lines in reference:
                #     print(lines)

            except:
                # print("ddd")
                pass
            
            try:
#                 text = text.lower();
                words=re.split(pattern,text)
                for word in words:
#                     word=word.lower()
                    if word not in stemWord:
                        stemWord[word]=stemmer.stem(word.lower())
                        word=stemWord[word]
                    else:
                        word=stemWord[word]
#                     word=stemmer.stem(word)
                    n5=len(word)
                    if n5<3:
                        continue 
                    elif word in stop_words:
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
#                 text=text.lower()
                # if "gandhi" in text:
                #     print(title,pageCount)
                titlePosition.append(titleFp.tell())
                titleFp.write(title)
                pattern = re.compile("[^a-zA-Z0-9]")
                words=re.split(pattern,text)
                for word in words:
#                     word=word.lower()
#                     word=stemmer.stem(word)
                    if word not in stemWord:
                        stemWord[word]=stemmer.stem(word.lower())
                        word=stemWord[word]
                    else:
                        word=stemWord[word]
                    n5=len(word)
                    if n5<3:
                        continue 
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
        
            if pageCount%60000==0:
                indexFileWrite("category",NoOFFiles)
                indexFileWrite("infoBox",NoOFFiles)
                indexFileWrite("title",NoOFFiles)
                indexFileWrite("text",NoOFFiles)
                NoOFFiles=NoOFFiles+1
                titleIndexing.clear()
                infoboxIndexing.clear()
                categoryIndexing.clear()
                textIndexing.clear()
            if pageCount%50000==0:
                # print(pageCount)
                stemWord={}
        elem.clear() 


# In[ ]:


# In[13]:


# print(sum_text)
# print(sum_title)Come up with few knock-knock jokes , add them to your data so that one in-frequent item set becomes frequent.(The jokes doesn't have to be funny! or semantically correct)


# In[14]:


# titleIndexing


# In[15]:


# In[ ]:


import pickle
file = open(folderPath+"/titlePositions.pickle", "wb")
pickle.dump(titlePosition, file)
file.close()


# In[ ]:


# In[16]:
# print(len(stemWord))
# testfile="wordDictSize.txt"
# fp_test=open(testfile,"w+")
# list1=stemWord.keys()
# lis1=",".join(list1)
# fp_test.write(lis1)
# fp_test.close()
indexFileWrite("category",NoOFFiles)
indexFileWrite("infoBox",NoOFFiles)
indexFileWrite("title",NoOFFiles)
indexFileWrite("text",NoOFFiles)


# In[17]:Come up with few knock-knock jokes , add them to your data so that one in-frequent item set becomes frequent.(The jokes doesn't have to be funny! or semantically correct)


# In[ ]:


# print(len(categoryIndexing))
# print(len(titleIndexing))
# print(len(infoboxIndexing))
# print(len(textIndexing))


# In[18]:




# In[19]:
filePtrs={}


# In[ ]:


from heapq import *


# In[ ]:


def getTfIdfOfWord(word,postingList,fp,typ,lineNo):
    wordIdf={}
    docs=postingList.split(",")
    idf=math.log10(pageCount/len(docs))
    for doc in docs:
        if ":" in doc:
            docNo,count=doc.split(":")
            tf = 1 + math.log10(int(count))
            wordIdf[str(docNo)] = round(idf * tf, 2)
    wordIdf = sorted(wordIdf.items(), key = operator.itemgetter(1), reverse = True)
    finalDoc=[]
    topCount=0
#     print(wordIdf)
    for doc in wordIdf:
        key=doc[0]
        value=doc[1]
        final=str(key)+":"+str(value)
        finalDoc.append(final)
        topCount=topCount+1
        if topCount==10:
            break;
    
    if typ=="category":
        if word not in wordPosition:
            wordPosition[word]={}
#         fp.write(finalDoc)
        wordPosition[word]['c']=lineNo
        index=",".join(finalDoc)
        index+="\n";
        lineNo=lineNo+len(index)
#         print(index)
#         print(lineNo)
        fp.write(index)
        return lineNo
    if typ=="title":
        if word not in wordPosition:
            wordPosition[word]={}
        wordPosition[word]['t']=lineNo
        index=",".join(finalDoc)
        index+="\n";
        lineNo=lineNo+len(index)
        fp.write(index)
        return lineNo
    if typ=="infoBox":
        if word not in wordPosition:
            wordPosition[word]={}
#         fp.write(finalDoc)
        wordPosition[word]['i']=lineNo
        index=",".join(finalDoc)
        index+="\n";
        lineNo=lineNo+len(index)
        fp.write(index)
        return lineNo
    if typ=="text":
        if word not in wordPosition:
            wordPosition[word]={}
#         fp.write(finalDoc)
        wordPosition[word]['d']=lineNo
        index=",".join(finalDoc)
        index+="\n";
        lineNo=lineNo+len(index)
#         print(index)
#         print(lineNo)
        fp.write(index)
        return lineNo
        


# In[ ]:


def mergeCategory(filePtrs,typ,heap):
    lineNo=0
    w=0
#     print(heap)
    heapify(heap)
    fileDelete=""
    if typ=="category":
            fp_output=open(folderPath+"/categoryPosting.txt","w")
            fileDelete=folderPath +"/categoryPosting"
    if typ=="infoBox":
            fp_output=open(folderPath+"/infoBoxPosting.txt","w")
            fileDelete=folderPath +"/infoBoxPosting"
    if typ=="text":
            fp_output=open(folderPath+"/textPosting.txt","w")
            fileDelete=folderPath +"/textPosting"
    if typ=="title":
            fp_output=open(folderPath+"/titlePosting.txt","w")
            fileDelete=folderPath +"/titlePosting"
    try:
        while w<=NoOFFiles:
            x,fileNo=heappop(heap)
            word=x[:x.find("-")]


            postingList=x[x.find("-")+1:]
    #         print(fileNo,filePtrs)
            fp=filePtrs[int(fileNo)]
            nextLine=fp.readline()[:-1]
    #         print(nextLine)
            if nextLine:
                heappush(heap,(nextLine,fileNo))
            else:
                fp.close()
                fileName = fileDelete+str(fileNo)+".txt"
                os.remove(fileName)
                w=w+1

            if w==NoOFFiles:
                break


            while(1):
                y,fileNo=heappop(heap)
                wordNext=y[:y.find("-")]
                postingListNext=y[y.find("-")+1:]
                if wordNext==word:
                    postingList=postingList+","+postingListNext
                    fp=filePtrs[int(fileNo)]
                    nextLine=fp.readline()[:-1]
                    if nextLine:
                        heappush(heap,(nextLine,fileNo))
                    else:
                        fp.close()
                        fileName = fileDelete+str(fileNo)+".txt"
                        os.remove(fileName)
                        w=w+1; 
                else:
                    heappush(heap,(y,fileNo))
                    break;

    #         if word=="napier":
    #             print(postingList)
            #we have one word and one posting list
            # print(word,postingList)
            lineNo=getTfIdfOfWord(word,postingList,fp_output,typ,lineNo)
    except IndexError:
        pass
        
        


# In[ ]:


def mergeFiles(typ):
    
    if typ=="category":
        heap=[]
        for i in range(1,NoOFFiles+1):
            fileName = folderPath +"/categoryPosting"+str(i)+".txt"
            fp = open(fileName, "r")
            filePtrs[i]=fp
            firstLine=fp.readline()[:-1]
            heap.append((firstLine,i))
        mergeCategory(filePtrs,"category",heap)
        # for i in range(1,NoOFFiles+1) :
        #     filePtrs[i].close()
        #     fileName = folderPath +"/categoryPosting"+str(i)+".txt"
        #     os.remove(fileName)
            
    if typ=="infoBox":
        heap=[]
        filePtrs.clear()
        for i in range(1,NoOFFiles+1):
            fileName = folderPath +"/infoBoxPosting"+str(i)+".txt"
            fp = open(fileName, "r")
            filePtrs[i]=fp
            firstLine=fp.readline()[:-1]
            heap.append((firstLine,i))
        mergeCategory(filePtrs,"infoBox",heap)
        # for i in range(1,NoOFFiles+1) :
        #     filePtrs[i].close()
        #     fileName = folderPath +"/infoBoxPosting"+str(i)+".txt"
        #     os.remove(fileName)
    if typ=="text":
        heap=[]
        filePtrs.clear()
        for i in range(1,NoOFFiles+1):
            fileName = folderPath +"/textPosting"+str(i)+".txt"
            fp = open(fileName, "r")
            filePtrs[i]=fp
            firstLine=fp.readline()[:-1]
            heap.append((firstLine,i))
        mergeCategory(filePtrs,"text",heap)
        # for i in range(1,NoOFFiles+1) :
        #     filePtrs[i].close()
        #     fileName = folderPath +"/textPosting"+str(i)+".txt"
        #     os.remove(fileName)
        
    if typ=="title":
        heap=[]
        filePtrs.clear()
        for i in range(1,NoOFFiles+1):
            fileName = folderPath +"/titlePosting"+str(i)+".txt"
            fp = open(fileName, "r")
            filePtrs[i]=fp
            firstLine=fp.readline()[:-1]
            heap.append((firstLine,i))
        mergeCategory(filePtrs,"title",heap)
        # for i in range(1,NoOFFiles+1) :
        #     filePtrs[i].close()
        #     fileName = folderPath +"/titlePosting"+str(i)+".txt"
        #     os.remove(fileName)
        
        
    


# ### K WAY MERGE###

# In[ ]:


import math
import operator
mergeFiles("category")


# In[ ]:


mergeFiles("text")
mergeFiles("infoBox")
mergeFiles("title")


# In[ ]:


# def writePostingList(fp,fp1,f):
#     lineNo=0
#     for line in fp.readlines():
#         pos=line.find("-")
#         word = line[:pos]
#         flag=0
#         posting_list = line[pos+1:]
#         if word not in wordPosition:
#             flag=1
#         if flag==1:
#             wordPosition[word] = {}
#         wordPosition[word][f] =lineNo
#         x=len(posting_list)
#         lineNo+=x;
#         fp1.write(posting_list)
#     return fp,fp1


# In[20]:


# import os


# In[ ]:


# In[21]:


# file = folderPath+"/title.txt"
# file1 = folderPath+"/titlePosting.txt"
# fp = open(file, "r")
# fp1 = open(file1, "w+")
# fp,fp1=writePostingList(fp,fp1,"t")
# fp1.close()
# fp.close()
# os.remove(folderPath+"/title.txt")

# file = folderPath+"/category.txt"
# file1 = folderPath+"/categoryPosting.txt"
# fp = open(file, "r")
# fp1 = open(file1, "w+")
# fp,fp1=writePostingList(fp,fp1,"c")
# fp1.close()
# fp.close()
# os.remove(folderPath+"/category.txt")

# file = folderPath+"/infoBox.txt"
# file1 = folderPath+"/infoBoxPosting.txt"
# fp = open(file, "r")
# fp1 = open(file1, "w+")
# fp,fp1=writePostingList(fp,fp1,"i")
# fp1.close()
# fp.close()
# os.remove(folderPath+"/infoBox.txt")

# file = folderPath+"/text.txt"
# file1 = folderPath+"/textPosting.txt"
# fp = open(file, "r")
# fp1 = open(file1, "w+")
# fp,fp1=writePostingList(fp,fp1,"d")
# fp1.close()
# fp.close()
# os.remove(folderPath+"/text.txt")


# In[ ]:






# In[22]:


# wordPosition
# print(len(wordPosition))


# In[23]:


# In[ ]:


file = open(folderPath+"/wordPositions.pickle", "wb")
# file = open("wordPositions.pickle", "wb")
pickle.dump(wordPosition, file)
file.close()
end = time.time()
print("Index Build in - " + str(end - start) + "s")

