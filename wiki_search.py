
# coding: utf-8

# In[15]:


import time
import nltk
import sys


# In[16]:


stop_file = open("Stop_words.txt", "r")
content = stop_file.read()
sum_text=0
stop_words={}


# In[17]:


import re
reg = re.compile("\"|,| ")
import nltk
stemmer = nltk.stem.SnowballStemmer('english')
content = re.split(reg, content)
sum_title=0
for word in content :
    if word :
        stop_words[word] = True


# In[ ]:


folderPath=sys.argv[1]


# In[18]:


titleTags = open(folderPath+"/title_tags.txt", "r")
resutltantListFieldQuery=[]


# In[19]:


import pickle
titlePosition = pickle.load(open(folderPath+"/titlePositions.pickle", "rb"))
wordPosition = pickle.load(open(folderPath+"/wordPositions.pickle", "rb"))


# In[20]:


def findTitle(documentList):
#     print(documentList)
    titleList=[]
    if "," in documentList:
        list1=documentList.split(",")
        for doc in list1:
            docNo,count=doc.split(":")
            position=titlePosition[int(docNo)-1]
            titleTags.seek(position)
            title = titleTags.readline()[: -1]
#             print(title)
            titleList.append(title)
    else:
        docNo,count=documentList.split(":")
        position=titlePosition[int(docNo)-1]
        titleTags.seek(position)
        title = titleTags.readline()[: -1]
        titleList.append(title)
        
    return titleList


# In[21]:


def findDocumentList(position,fp):
    fp.seek(position)
    s=fp.readline()[: -1]
    return s


# In[22]:


file = folderPath+"/titlePosting.txt"
fp_title = open(file, "r")

file = folderPath+"/infoBoxPosting.txt"
fp_infoBox = open(file, "r")

file = folderPath+"/categoryPosting.txt"
fp_category = open(file, "r")

file = folderPath+"/textPosting.txt"
fp_text = open(file, "r")


# In[23]:


def searchPosition(word,type1):
    return wordPosition[word][type1]
#     documentList=[]
#     for key,document in wordPosition:
#         if key==type1:
#             documentList=document
#     return documentList


# In[24]:


def intersection(lst1, lst2): 
    tup1 = map(tuple, lst1) 
    tup2 = map(tuple, lst2)  
    return list(map(list, set(tup1).intersection(tup2))) 


# In[25]:


def searchWordOfFieldQuery(word):
    global resutltantListFieldQuery
    positions=wordPosition[word]
#     print(positions)
    for tag in positions:
        position=positions[tag]
        if tag=="t":
            documentList=findDocumentList(position,fp_title)
#             print(documentList)
            titleList_t=findTitle(documentList)
            resutltantListFieldQuery.append(titleList_t)
        if tag=="d":
            documentList=findDocumentList(position,fp_text)
#             print(documentList)
            titleList_d=findTitle(documentList)
#             print(titleList_d)
            resutltantListFieldQuery.append(titleList_d)
        if tag=="c":
            documentList=findDocumentList(position,fp_category)
            titleList_c=findTitle(documentList)
            resutltantListFieldQuery.append(titleList_c)
        if tag=="i":
            documentList=findDocumentList(position,fp_infoBox)
            titleList_i=findTitle(documentList)
            resutltantListFieldQuery.append(titleList_i)


# In[26]:


def search(path_to_index, queries):
    result=[]
    noOfQueries=len(queries)
    
    for data in range(0,noOfQueries):
        query=queries[data]
        flag=1
        query=query.lower()
        query=query.strip()
        if query=="exit":
            break
        resultantList=[]
        resutltantListFieldQuery.clear()
        if ":" in query:
            flag=0
            queryTags=[]
            if "," in query:
                queryTags=query.split(",")
            else:
                queryTags.append(query)
            for tag in queryTags:
                tagName,words=tag.split(":")
                count1=0
                words=words.split()
                for word in words:
                    word=stemmer.stem(word)
                    if word not in wordPosition:
                        continue
                    if tagName not in wordPosition[word]:
                        continue
                    if tagName=="t":
                        position=searchPosition(word,"t")
    #                     print(word,position)
    #                     print("ARe u kiddign")
                        if position==0:
                            continue
                        documentList=findDocumentList(position,fp_title)
                        titleList_t=findTitle(documentList)
                        resultantList.append(titleList_t)

                    if tagName=="d":
                        position=searchPosition(word,"d")
                        if position=="":
                            continue
    #                     print("ARe u kiddignddddddddddddddddddddddddddddd")
                        documentList=findDocumentList(position,fp_text)
                        titleList_d=findTitle(documentList)
                        resultantList.append(titleList_d)
                    if tagName=="i":
                        position=searchPosition(word,"i")
                        if position=="":
                            continue
    #                     print("ARe u kiddiiiiiiiiiiiiiiiiiiiii")
                        documentList=findDocumentList(position,fp_infoBox)
                        titleList_i=findTitle(documentList)
                        resultantList.append(titleList_i)
                    if tagName=="c":
                        position=searchPosition(word,"c")
                        if position=="":
                            continue
    #                     print("ARe u kiddcccccccccccccccccccccccccccc")
                        documentList=findDocumentList(position,fp_category)
                        titleList_c=findTitle(documentList)
                        resultantList.append(titleList_c)
        else:
            words=query.split()
            for word in words:
                word=stemmer.stem(word)
                if word not in wordPosition:
                    continue
                searchWordOfFieldQuery(word)
    #     print("lengthhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh    ",len(resultantList))

        if len(resultantList)==0 and flag==0:
            print("No result found")

        elif len(resutltantListFieldQuery)==0 and flag==1:
            print("No result found")
        elif flag==0:
            ans=[]
            if len(resultantList)==1:
                result.append(resultantList)
                for i in resultantList[0]:
                    print(i)
                continue

            n=len(resultantList)
            ans=resultantList[0]
            for i in range(1,n):
                setA=set(ans)
    #             print(setA)
                setB=set(resultantList[i])
                ans=list(setA | setB )
            result.append(ans)
            for i in ans:
                print(i)
        else:
            ans=[]
    #         print(resutltantListFieldQuery)
            if len(resutltantListFieldQuery)==1:
                result.append(resutltantListFieldQuery)
                for i in resutltantListFieldQuery[0]:
                    print(i)
                continue

            n=len(resutltantListFieldQuery)
    #         print(n)
            ans=resutltantListFieldQuery[0]
    #         t = list(set(q) & set(w))
            for i in range(1,n):
    #             print("inside")
                setA=set(ans)
    #             print(setA)
                setB=set(resutltantListFieldQuery[i])
                ans=list(setA | setB )
    #             print("dd ",ans)
            result.append(ans)
            for i in ans:
                print(i)
    return result


# In[27]:


def read_file(testfile):
    with open(testfile, 'r') as file:
        queries = file.readlines()
    return queries


# In[28]:


def write_file(outputs, path_to_output):
    '''outputs should be a list of lists.
        len(outputs) = number of queries
        Each element in outputs should be a list of titles corresponding to a particular query.'''
    with open(path_to_output, 'w') as file:
        for output in outputs:
            for line in output:
                file.write(line.strip() + '\n')
            file.write('\n')


# In[29]:


def main():
    path_to_index = sys.argv[1]
    testfile = sys.argv[2]
    path_to_output = sys.argv[3]

    queries = read_file(testfile)
    outputs = search(path_to_index, queries)
    write_file(outputs, path_to_output)


if __name__ == '__main__':
    main()

