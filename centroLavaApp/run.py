from flask import Flask, render_template, request, json, session
from LavaSession import LavaSession
from DNA import DNA
from datamodel import database
from QuestionBaseInterface import QuestionBaseInterface
from Question import Question
import sys
import nltk
app = Flask(__name__)
app.secret_key = '5656798291'


############################ Session Init Info ############################


SESSION_INFO = LavaSession(username="johndoe1", name="John Doe")
PORT = 5099
dna = DNA()
INITIALIZED = [
      "Agriculture",
      "Food and Beverage",
      "Services",
      "Products",
      "Healthcare",
      "Open Entry"
    ]
dna.interestedcolo = INITIALIZED
dna.db = database()
dna.qb = QuestionBaseInterface()
dna.currentquestion = dna.qb.matchColo(INITIALIZED)
SESSION_INFO.question = dna.currentquestion.toQestion()




########################## Session Init Info Ends ##########################


@app.route("/centroSubmitFollow", methods=['GET', 'POST'])
def ajaxSubmit():
    """
    Handles HTTP requests (GET and POST) that are sent through ajax (i.e. without control of page redirection).

    :return: A serialized json object that contains the session information to be used in javascript
    """

    postRequest = request.json or request.form # Short circuit the data fetch
    print postRequest
    print postRequest.getlist('answer')
    alist = eval("".join(postRequest.getlist('answer')))
    statusid =  postRequest.getlist('id')[0]
    if statusid == "-2" and dna.currentquestion == -1:
        SESSION_INFO.result = dna.currentList
        q = Question()
        q.qid = "-1"
        SESSION_INFO.question = q
        SESSION_INFO.answerlist = dna.answerList
        return json.dumps({"session_info": SESSION_INFO.toJson()})
    elif statusid != "-2":
        if alist == []:
            return json.dumps({"session_info": SESSION_INFO.toJson()})
        if dna.currentquestion != -1:
            dna.answer(alist)
            dna.newQ()

        if dna.currentquestion == -1 or dna.currentquestion == "error":
            print "error got"
            SESSION_INFO.result = dna.currentList
            q = Question()
            q.qid = "-1"
            SESSION_INFO.question = q
            SESSION_INFO.answerlist = dna.answerList
            return json.dumps({"session_info": SESSION_INFO.toJson()})
        SESSION_INFO.question = dna.currentquestion.toQestion()
        print SESSION_INFO.toJson()
        return json.dumps({"session_info": SESSION_INFO.toJson()})
    else:
        return json.dumps({"session_info": SESSION_INFO.toJson()})

@app.route("/centroBackFollow", methods=['GET', 'POST'])
def ajaxBack():
    dna.db.restore_data(len(dna.answerList))

    if len(dna.qb.askedq) != 0:
        dna.answerList.pop(-1)
        qbnow = dna.qb.askedq[-1]
        print dna.qb.askedq
        dna.qb.askedq.pop(-1)
        dna.currentquestion = dna.qb.getQ(qbnow)
        SESSION_INFO.question = dna.currentquestion.toQestion()
    return json.dumps({"session_info": SESSION_INFO.toJson()})



@app.route("/centrosubmit", methods=['GET', 'POST'])
def redirectSubmit():
    """
    Handles HTTP requests (GET and POST) with redirection after the request submission.

    :return: The rendered new page that will be displayed, with relevant arguments provided
    """
    postRequest = request.json or request.form or request.args
    print postRequest

    rawText = str(postRequest.items()[0][1])
    collist = key_words_filter(rawText)
    if len(collist) != 0:
        dna.db.fileter_cato(collist,0)
    if dna.currentquestion.qid == -1:
        print "error got"
        SESSION_INFO.result = dna.currentList
        q = Question()
        q.qid = "-1"
        SESSION_INFO.question = q
        SESSION_INFO.answerlist = dna.answerList




    return render_template('question.html', session_info=json.dumps(SESSION_INFO.toJson()))

@app.route("/finalresult", methods=['GET', 'POST'])
def submitResult():
    print SESSION_INFO.answerlist
    print SESSION_INFO.result
    return render_template('finalresult.html', session_info=SESSION_INFO.toJson())



@app.route("/")
@app.route("/index")
def index():
    """
    Handles requests to the home page (index page)

    :return: The rendered index page that will be displayed, with rele
    """
    global SESSION_INFO
    SESSION_INFO = LavaSession(username="johndoe1", name="John Doe")
    global dna
    dna = DNA()
    dna.interestedcolo = INITIALIZED
    dna.db = database()
    dna.qb = QuestionBaseInterface()
    dna.currentquestion = dna.qb.matchColo(INITIALIZED)
    SESSION_INFO.question = dna.currentquestion.toQestion()
    #session['sid'] = SESSION_INFO.sid
    print SESSION_INFO.toJson()
    return render_template('index.html', session_info=SESSION_INFO.toJson())

def key_words_filter(raw_txt):
    key_words_mapping_list = {}
    col_list = set()

    with open('expand_keywords.txt', 'r') as file:
        for line in file:
            line = line.split("|")
            map_words = set()
            words = line[1].split(",")
            for token in words:
                map_words.add(token.strip().lower())
            key_words_mapping_list[line[0]] = map_words

    stopwords = nltk.corpus.stopwords.words('english') + ['.', ',', '?', '(', ')', ':', '"', '-', '{', '}', '\'', '--',
                                           '\'s', '\'re', 'the', 'you']
    stopwords = set(stopwords)

    tokens = nltk.word_tokenize(raw_txt)

    filtered_words = [word.lower() for word in tokens if word not in stopwords]
    filtered_words = set(filtered_words)

    for single_word in filtered_words:
        for col_name, col_key_words in key_words_mapping_list.items():
            if single_word in col_key_words:
                print single_word
                print col_name
                print "************"
                col_list.add(col_name)

    return list(col_list)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        PORT = eval(sys.argv[1])
    app.run(host="0.0.0.0", port=PORT)
