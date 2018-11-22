# -*- coding: utf-8 -*-

from numpy import *
import os
import jieba
import re


def loadDataSet():
    # 记录数据集，使用python的list，一共是6条，每条又包含了若干条
    in_path = r"C:\Users\Administrator\Desktop\cz\项目\觅景\MEETJINN\meetjinnDJ\algorithm\cikutxt\\"
    postingList1 = [fname for fname in os.listdir(in_path) if fname[-4:] == ".txt"]
    print (postingList1)
    # 分类向量，1 代表侮辱性文字，0代表正常言论。
    postingList = []
    for i in postingList1:
        with open(in_path + i, 'r', encoding='UTF-8') as f:
            data = f.read()
            data = data.split('\n')
            postingList.append(data)
    classVec = [1, 2, 3, 4, 5, 6, 7]
    # 返回的第一个变量是进行词条切分后的文档集合，第二个变量是一个类别标签的集合
    return postingList, classVec


# 创建一个包含在所有文档中出现的不重复词的列表
def createVocabList(dataSet):
    # 创建一个空集
    vocabSet = set([])
    # 循环实现如果这个词出现在数据集中，就创建两个集合的并集。重复的词只会被加入进去一次。也就实现了只存储不重复词的功能
    for document in dataSet:
        vocabSet = vocabSet | set(document)  # 创建两个集合的并集
    # 返回这个词汇列表
    return list(vocabSet)


# 这个函数实现的功能：将两个词汇表进行对比，如果输入的数据集在词汇表中，就让向量值为1，否则输出该词不在文档中。
# 输入的参数为词汇表及某个文档，输出的是文档向量。
def wordstoVec(vocabList, inputSet):
    # 创建一个其中所含元素都为0的向量，向量长度与词汇表长度一致
    returnVec = [0] * len(vocabList)
    # 对输入集中每一个单词执行，如果单词在词汇表中就使这个词的索引位置相应的的文档向量值为1，否则输出这个词不是词汇表中的
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print ("这个单词： %s 不是我词汇表里的!" % word)
    # 返回这个转化后的向量
    return returnVec


# 输入的参数为文档矩阵trainMatrix，以及由每篇文档类别标签所构成的向量trainCategory。
# 首先计算文档属于侮辱性文档的概率，即P(1)。因为是二类分类问题，所以可以通过1-P(1)得到p(0)。
def trainNB0(trainMatrix, trainCategory, k):
    # 训练文本单词数为训练矩阵的长度。
    TrainDocsNum = len(trainMatrix)
    # 单词数为训练矩阵第一行的长度，这只是为了初始化
    Wordsnum = len(trainMatrix[0])
    # 辱骂性词汇出现的概率为所有训练类别相加除以训练文本单词总数，因为辱骂性词汇的类别都是1.
    pbad = sum(trainCategory == k) / float(TrainDocsNum)
    # 计算p（wi|c1）和p（wi|c0），p(w|c)指在分类c下，词语w出现的样本数与分类c所有样本中所有词数
    # 让类别为0的单词出现的次数设为全为1的向量，向量的高度与单词数相同。
    p0 = ones(Wordsnum)
    # 让类别为1的单词出现的次数设为全为1的向量，向量的高度与单词数相同。
    p1 = ones(Wordsnum)
    # 设定初始一行的单词数计数为2，这也是一处改进，为了防止下溢，避免因为某个特性下概率为0 就导致整体概率为0。把计数从1改为2
    p0Denom = 2.0;
    p1Denom = 2.0
    # 让所有的向量对应元素相加，一旦某个词在文档出现，对该词对应的个数就加1。而且总词数也加1。
    # range代表从0到TrainDocsNum的整数列表
    for i in range(TrainDocsNum):
        # 假如训练种类对应的值为1就使类别1单词出现的次数加1
        if trainCategory[i] == k:
            p1 += trainMatrix[i]
        # 假如训练种类对应的值为0就使类别0单词出现的次数加1
        else:
            p0 += trainMatrix[i]
    p1Denom = sum(trainCategory == k)
    p0Denom = len(trainCategory) - p1Denom
    # 对每个元素出现的次数除以该类别中对应某行的总词数，概率进行乘法过后数值会比较小，取log方便比较
    p1Vect = log(p1 / p1Denom)
    return p1Vect, pbad


# 朴素贝叶斯分类函数
def classifyNB(vec2Classify, p1Vec, p2Vec, p3Vec, p4Vec, p5Vec, p6Vec, p7Vec, pClass1, pClass2, pClass3, pClass4,
               pClass5, pClass6, pClass7):
    # 元素相乘,对应元素相乘，然后将词汇表中所有词的对应值相加，然后将该值加到类别的对数概率上。
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p2 = sum(vec2Classify * p2Vec) + log(pClass2)
    p3 = sum(vec2Classify * p3Vec) + log(pClass3)
    p4 = sum(vec2Classify * p4Vec) + log(pClass4)
    p5 = sum(vec2Classify * p5Vec) + log(pClass5)
    p6 = sum(vec2Classify * p6Vec) + log(pClass6)
    p7 = sum(vec2Classify * p7Vec) + log(pClass7)
    # 比较类别的概率返回大概率对应的类别标签。
    print ([p1, p2, p3, p4, p5, p6, p7])
    return ([p1, p2, p3, p4, p5, p6, p7].index(max([p1, p2, p3, p4, p5, p6, p7])) + 1)


# 便利函数，封装了所有操作。
def testingNB(str1):
    # 加载数据集
    listOPosts, listClasses = loadDataSet()
    # 创建词汇表
    myVocabList = createVocabList(listOPosts)
    # 创建一个空集
    trainMat = []
    # 循环所有数据集中词汇，转化为词汇向量
    for postingDoc in listOPosts:
        trainMat.append(wordstoVec(myVocabList, postingDoc))
    # 调用函数计算0类词出现概率和1类词出现的概率以及辱骂性词汇出现的概率
    p1V, pb1 = trainNB0(array(trainMat), array(listClasses), 1)
    p2V, pb2 = trainNB0(array(trainMat), array(listClasses), 2)
    p3V, pb3 = trainNB0(array(trainMat), array(listClasses), 3)
    p4V, pb4 = trainNB0(array(trainMat), array(listClasses), 4)
    p5V, pb5 = trainNB0(array(trainMat), array(listClasses), 5)
    p6V, pb6 = trainNB0(array(trainMat), array(listClasses), 6)
    p7V, pb7 = trainNB0(array(trainMat), array(listClasses), 7)
    testEntry = str1
    testEntry=re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), str1)
    testEntry = jieba.cut(testEntry)

    thisDoc = array(wordstoVec(myVocabList, testEntry))
    a=classifyNB(thisDoc, p1V, p2V, p3V, p4V, p5V, p6V, p7V, pb1, pb2, pb3, pb4, pb5, pb6, pb7)
    print (
    testEntry, '被分到: ', classifyNB(thisDoc, p1V, p2V, p3V, p4V, p5V, p6V, p7V, pb1, pb2, pb3, pb4, pb5, pb6, pb7),
    '类\n', '美食概率：\n', p3V)
    return a


# 应用部分：使用朴素贝叶斯过滤垃圾邮件，使用到交叉验证。
# 数据准备会有垃圾邮件文件夹下面全部是标记的垃圾邮件，正常邮件文件夹下是正常邮件。
# textParse函数接受一个字符串并将其解析为字符串列表，把大写字符转化成小写，并且只存储大于两个字母的词。
# spamTest函数在50封邮件中选取10篇邮件随机选择为测试集交叉验证。


# if __name__ == "__main__":
#     # listOPosts,listClasses = loadDataSet()
#     # myVocabList = createVocabList(listOPosts)
#     # print ('       ————————————————————我的词汇列表：——————————————————\n',myVocabList)
#     # trainMat = []
#     # for postinDoc in listOPosts:
#     #     trainMat.append(wordstoVec(myVocabList, postinDoc))
#     # p0V,p1V,pAb = trainNB0(trainMat, listClasses)
#     testingNB()
