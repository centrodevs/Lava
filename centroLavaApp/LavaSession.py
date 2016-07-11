import random
import string


class LavaSession(object):

    def __init__(self, sid="", stage=1, question=None, username="anonymous",
                 name="Anonymous", location="Unknown"):
        """
        Initialize a new Centro Lava session, which essentially corresponds to a user's information and status.

        :param sid:
        :param stage:
        :param question:
        :param username:
        :param name:
        :param location:
        """
        self.sid = sid if sid != "" else self.random_id()
        self.username = username
        self.name = name
        self.location = location
        self.stage = stage if stage > 0 else 1
        self.potentialProviders = []
        self.question = question
        self.postCallback = "/centroSubmit" if stage == 1 else "/centroSubmitFollow"
        self.result = []
        self.answerlist = []

    @staticmethod
    def random_id(size=6, chars=string.ascii_uppercase + string.digits):
        """
        Generate a random string id.

        @param size: The desired length of the id
        @param chars: The set of acceptable characters in the id
        @return: The generated string format id
        """
        return ''.join(random.choice(chars) for _ in range(size))

    def toJson(self):
        return {
            "session_id": self.sid,
            "username": self.username,
            "name": self.name,
            "stage": self.stage,
            "question": self.question.toJson() if self.question else {},
            "location": self.location,
            "callback": self.postCallback,
            "result": self.result,
            "answerlist": [ans for ans in self.answerlist if ans.lower() not in ["yes", "no"] and len(ans) > 2]
        }