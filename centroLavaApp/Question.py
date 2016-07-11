import collections


def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data

class Question:

    def __init__(self, qid="", text="", type="text", options=[]):
        self.qid = qid
        self.questionText = text
        self.answerType = type
        self.descriptions = {}

        if type not in ["checkbox", "radio", "dropdown"]:
            self.options = []
        else:
            self.options = options
        self.subquestions = []

    def toJson(self):
        return {
            "qid": str(self.qid),
            "text": str(self.questionText),
            "answer_type": str(self.answerType),
            "options": [str(opt) for opt in self.options],
            "subquestions": self.subquestions,
            "descriptions": convert(self.descriptions)
        }