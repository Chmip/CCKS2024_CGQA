from hanlp_restful import HanLPClient

import json



class my_hanlp():
    def __init__(self):
        self.HanLP = HanLPClient('https://www.hanlp.com/api', auth='NTcyMEBiYnMuaGFubHAuY29tOjZWcG53Y0FhcWRsN2NmZ2M=', language='zh') # auth不填则匿名，zh中文，mul多语种
        self.questions = []

    def batch(self, questions):
        if len(questions) > 200:
            self.questions.append(questions[0:200])
            self.batch(questions[200:])
        else:
            self.questions.append(questions)



    def fenci(self, questions):
        self.batch(questions)
        doc = []
        for question in self.questions:
            doc.extend(self.HanLP.tokenize(question, coarse=True))
        return doc

    def dependency(self, questions):
        self.batch(questions)
        docs = {"tok/fine": [],
                "dep":[]}
        for question in self.questions:
            doc = self.HanLP.parse(question, tasks=['dep', 'sdp'])
            docs["tok/fine"].extend(doc["tok/fine"])
            docs["dep"].extend(doc["dep"])

            doc.pretty_print()
        return docs



        docdep = doc["dep"]
        doctok = doc["tok/fine"]
        self.fx(docdep, doctok, qs)


    def fx(self, docdep, doctok, qs):
        for index, value in enumerate(docdep):
            print(qs[index])
            print(value)
            ing = 0
            while value[ing][0] != 0:
                print(doctok[index][ing], end=' ')
                ing = value[ing][0] - 1
            print()
            print()

    def SRL(self, questions):
        self.batch(questions)
        docs = {"tok/fine": [],
                "srl": []}
        for question in self.questions:
            doc = self.HanLP.parse(question, tasks=['srl'])
            docs["tok/fine"].extend(doc["tok/fine"])
            docs["srl"].extend(doc["srl"])
            doc.pretty_print()
        return docs

