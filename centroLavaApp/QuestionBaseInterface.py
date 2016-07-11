import json
from QuestionData import QuestionData
from QuestionData import CatoQuestionData
class QuestionBaseInterface:
    def __init__(self):
        self.questionDict = {}
        self.parseQuestionIn("QuestionDatabase")
        self.askedq = []

    def parseQuestionIn(self,questionfiledes):
        with open(questionfiledes) as data_file:
            data = json.load(data_file)
            for k,v in data.items():
                if v["iscolfilter"]:
                    qd = CatoQuestionData()
                    qd.direct = v["nextq"]
                else:
                    qd = QuestionData()
                qd.descriptions = v["descriptions"]
                qd.colos = v["cols"]
                qd.isradio = v["isradio"]
                qd.iscolofilter = v["iscolfilter"]
                qd.qid = k
                qd.rawstring = v["rawstring"]
                qd.potentialanswers = v["potentialanswers"]
                self.questionDict[''.join(qd.colos)] = qd

    def matchColo(self,coloList):
        print coloList
        try:
            return self.questionDict[''.join(coloList)]
        except:
            return "error"

    def getQ(self, qid):
        for k, v in self.questionDict.items():
            if v.qid == str(qid):
                return v

    def getcolums(self):
        listofcolo = []
        for k, v in self.questionDict.items():
            if v.iscolofilter == False and v.qid not in self.askedq:
                listofcolo += v.colos
        listofcolo = list(set(listofcolo))
        return listofcolo
