from xlearn.webserver.trainer import *
import numpy as np
from colorama import Fore
from os.path import join
import re

CUP = '\x1b[1A'
ER = '\x1b[2K'
NL = CUP + ER


params = {}
params["modelId"] = "15"
params["paramsId"] = "4"


questions = {}

job = getJob(params)
job.model.loadRedisParams()

def getPPx(sentance):

    perplex = job.evaluate_sentance(sentance)
    return float(perplex[0]["Perplexity"])


def parseSentance(sent):
    idx = sent.index(" ")
    sno = sent[:idx]
    sentEval = sent[idx+1:]
    sentEval = sentEval.strip()
    sentEval = sentEval.replace("[","")
    sentEval = sentEval.replace("]","")

    sno = sno.replace(")","")
    option = sno[-1]
    qno = int(sno[:-1])

    return qno, option, sentEval


def parseQuests():
    f = open("Data/Holmes.machine_format.questions.txt", 'r')
    lines = f.readlines()

    for line in lines:
        qno, opt, sent = parseSentance(line)
        
        qdict = questions.get(qno, {})
        qdict[opt] = sent
        questions[qno] = qdict

    f.close()

def parseAns():
    f = open("Data/Holmes.machine_format.answers.txt", 'r')
    lines = f.readlines()

    for line in lines:
        qno, opt, sent = parseSentance(line)
        
        qdict = questions.get(qno, {})
        qdict["Ans"] = opt
        questions[qno] = qdict

    f.close()

parseQuests()
parseAns()

cumScore = 0.0

def evalQuestion(quest):

    ppxMax = 9999999
    ppxId = 'x'
    global cumScore

    for k in quest:
        if k == "Ans":
            continue

        ppx = getPPx(quest[k])

        if k == quest["Ans"]:
            cumScore += ppx
        
        if ppx < ppxMax:
            ppxMax = ppx
            ppxId = k

    return ppxId == quest["Ans"]


totalCorrect = 0

print params
print "TOBEDELETED"

for i,ques in enumerate(questions):

    totalCorrect += int(evalQuestion(questions[ques]))

    mean = (float(totalCorrect) /float(i+1) )*100.0
    meanPPX = cumScore / float(i+1)
    print NL , "%d/%d - Acc %.3f%%, Ppx %.3f " % (i+1, len(questions), mean , meanPPX)







