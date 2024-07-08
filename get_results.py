

from neo4j import AnswerSearcher

from classify import QuestionFeature
import json
import re



class AnswerGet:
    def __init__(self):
        self.qf = QuestionFeature()
        self.asr = AnswerSearcher()
        self.represent = []
        self.initialize()


    def initialize(self):
        with open('construct_train.json', 'r', encoding='utf-8') as f:
            train = json.loads(f.read())
        for represent_q, represent_item in train.items():
            self.represent.append([represent_q] + represent_item)
        print(self.represent)


        for represent_index, represent_item in enumerate(self.represent):
            parser_result = self.qf.parser(represent_item[0])
            if parser_result:
                self.represent[represent_index].append(parser_result['code'])
                words_index = []
                for word1 in represent_item[1]:
                    index_mapper = []
                    for index, words in parser_result.items():
                        if index == 'code':
                            pass
                        for word_index, word2 in enumerate(words):
                            if word1 == word2:
                                index_mapper.append([index, word_index])
                    words_index.append(index_mapper)
                self.represent[represent_index].append(words_index)


    def cdh0(self):
        for key_question, value in self.represent.items():
            parser_result = self.qf.parser(key_question)
            if parser_result:
                self.represent[key_question].append(parser_result['code'])
                words_index = []
                for word1 in value[2]:
                    index_mapper = None
                    for index, words in parser_result.items():

                        if index == 'code':
                            pass
                        for word_index, word2 in enumerate(words):
                            if word1 == word2:
                                index_mapper = (index, word_index)
                                break
                        if index_mapper != None:
                            break
                    words_index.append(index_mapper)
                self.represent[key_question].append(words_index)

    def mapper(self, mapper_list, parser):
        print(parser)
        mapper_words = []

        for mapper in mapper_list:

            if len(mapper) > 0 :
                string_dict = {}
                for mapper_item in mapper:
                    if mapper_item != None and mapper_item[0] in parser:
                        string_item = parser[mapper_item[0]][mapper_item[1]]
                    else:
                        string_item = None
                    if string_item not in string_dict:
                        string_dict[string_item] = 0
                    string_dict[string_item] += 1
                sorted_dict = sorted(string_dict.items(), key=lambda x: x[1], reverse=True)

                string_item = sorted_dict[0][0]

                if string_item != None:
                    match = re.search('\"([^"]+)', string_item, re.DOTALL)
                    if match:
                        string_item = match.group(1)
                    else:
                        match = re.search('([^"]+)', string_item, re.DOTALL)
                        if match:
                            string_item = match.group(1)

                if string_item == '':
                    mapper_words.append(None)
                else:
                    mapper_words.append(string_item)
            else:
                mapper_words.append(None)

        print(mapper_words)
        return mapper_words





    def fit(self, question):
        question_parser = self.qf.parser(question)
        question_code = question_parser['code']
        similarity_list = []
        for represent_index, represent_item in enumerate(self.represent):
            sim = self.qf.cosine_similarity(question_code, represent_item[3])
            print(represent_item[0], sim)
            similarity_list.append([represent_index, sim])

        if len(similarity_list) == 0:
            return False
        else:

            sorted_dict = sorted(similarity_list, key=lambda x: x[1], reverse=True)
            print(sorted_dict[0][1])
            if sorted_dict[0][1] < 0.6:
                return False

            mapper_words = self.mapper(self.represent[sorted_dict[0][0]][4], question_parser)

            return self.asr.get_result(self.represent[sorted_dict[0][0]][2], mapper_words)









def get_result():
    ag = AnswerGet()

    count = 0
    right = 0
    last_result = {}
    consider = []

    with open('./data/train_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
    for index, _ in qa_data.items():
        question = qa_data[index]['question']
        fit_result = ag.fit(question)
        if fit_result == []:
            last_result[index] = ["无"]
        elif fit_result:
            last_result[index] = fit_result
            answer = qa_data[index]['answer']
            print(answer)
            print(fit_result)
            print('\n\n\n')


            if set(fit_result) == set(answer):
                right += 1
            else:
                print('我错了：', question)
            count += 1
            if fit_result == []:
                last_result[index] = ["无"]

        else:
            consider.append([question])
            last_result[index] = ["无"]
    print(count)
    print(right)
    print(consider)
    print(len(consider))




def get_result_test():
    ag = AnswerGet()
    count = 0
    right = 0
    last_result = {}

    with open('./data/test_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
    for index, _ in qa_data.items():
        question = qa_data[index]['question']
        fit_result = ag.fit(question)
        if fit_result:

            last_result[index] = fit_result
            answer = ['无']
            print(answer)
            print(fit_result)

            if fit_result == answer:
                right += 1
            count += 1
            if fit_result == []:
                last_result[index] = ["无"]
        else:
            last_result[index] = ["无"]
    print(count)
    print(right)

    with open('data9.json', 'w', encoding='utf-8') as f:
        json.dump(last_result, f, ensure_ascii=False, indent=4)


def test():
    ag = AnswerGet()
    print(ag.represent)
    fit_result = ag.fit('李亚洲毕业于哪所大学？')
    print(fit_result)


get_result()
#get_result_test()
#test()
    