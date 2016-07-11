from QuestionData import QuestionData
from QuestionData import CatoQuestionData
from DataBaseInterface import DataBaseInterface
from QuestionBaseInterface import QuestionBaseInterface
from datamodel import database
import math

class DNA:

    db = database()
    qb = QuestionBaseInterface()
    currentquestion = QuestionData()
    interestedcolo = []
    currentList = []
    answerList = []

    def __init__(self):
        self.db = database()
        self.qb = QuestionBaseInterface()
        self.currentquestion = QuestionData()
        self.interestedcolo = self.currentquestion.colos
        self.answerList = []


    def answer(self,listofstr):
        self.qb.askedq.append(self.currentquestion.qid)
        if isinstance(listofstr, str):
            listofstr = [listofstr]
        for i in listofstr:
            self.answerList.append(i)
        if self.currentquestion.iscolofilter:
            self.interestedcolo = self.currentquestion.answer(listofstr)
            currentStageNum = self.db.get_max_stage_num() + 1
            self.db.fileter_cato(self.interestedcolo,currentStageNum)
        else:
            self.interestedcolo = self.currentquestion.colos
            currentStageNum = self.db.get_max_stage_num() + 1
            self.db.filter_col(self.interestedcolo[0], listofstr, currentStageNum)
        self.currentList = self.db.get_raw_data()


    def newQ(self):
        if len(self.currentList) <= 5:
            self.currentquestion = -1
            return
        if self.currentquestion.direct[self.answerList[-1]]!=-1:
            self.currentquestion = self.qb.getQ(self.currentquestion.direct[self.answerList[-1]])
            self.checkAnswers()

    def checkAnswers(self):

        for k,v in  self.currentquestion.potentialanswers.items():
            colflaglist = []
            if self.currentquestion.iscolofilter:
                flagList = []
                for col in v:
                    flagList.append(self.db.check_colum(col,"1"))
                if not any(flagList):
                    del self.currentquestion.potentialanswers[k]
            else:
                colflaglist.append(self.db.check_colum(v[0], k))
            if not any(colflaglist) and not self.currentquestion.iscolofilter:
                del self.currentquestion.potentialanswers[k]




    def get_col_by_entropy(self):
        col_entroy = {}
        data_len = len(self.currentList)
        for col_name in self.qb.getcolums():
            col_entroy[col_name] = {}
        for single_data in self.currentList:
            for col_name in self.qb.getcolums():
                val = single_data.get(col_name)
                if val not in col_entroy[col_name]:
                    col_entroy[col_name][val] = 0
                col_entroy[col_name][val] += 1
        max_entropy = 0
        max_col_name = ""
        for col_name, col_val in col_entroy.items():
            current_entropy = 0
            for val, num in col_val.items():
                current_entropy -= (float(num) / data_len) * math.log((float(num) / data_len))
            if current_entropy >= max_entropy:
                max_entropy = current_entropy
                max_col_name = col_name
        return max_col_name


















