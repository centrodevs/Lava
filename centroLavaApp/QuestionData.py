from Question import Question


class QuestionData(object):

    rawstring = ""
    colos = []
    potentialanswers = {}
    iscolofilter = False
    qid = ""
    isradio = False

    def __init__(self):
        self.rawstring = ""
        self.colos = []
        self.potentialanswers = {}
        self.iscolofilter = False
        self.qid = ""
        self.isradio = False
        self.descriptions = {}

    def toQestion(self):
        type = "checkbox"
        if self.isradio:
            type = "radio"
        question = Question(qid=self.qid,text=self.rawstring,type=type,options=self.potentialanswers.keys())
        question.descriptions = self.descriptions
        return question

    def answer(self, answerstrList):
        if self.isradio:
            return self.potentialanswers[answerstrList[0]]
        else:
            listofresp = []
            for ans in answerstrList:
                for ans2 in self.potentialanswers[ans]:
                    listofresp.append(ans2)
            return listofresp

class CatoQuestionData(QuestionData):

   def __init__(self):
       QuestionData.__init__(self)
       self.direct = {}