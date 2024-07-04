

from neo4j import AnswerSearcher

from classify2 import QuestionFeature
import json
import re



class AnswerGet:
    def __init__(self):
        self.qf = QuestionFeature()
        self.asr = AnswerSearcher()
        self.represent = []

        ss = [['陈沆的哥哥是谁？', ['陈沆', '哥哥'], '+'],
              ['以史为鉴：中华文明的演进与选择的作者是谁？', ['以史为鉴：中华文明的演进与选择', '作者'], '+'],
              ['赵翼的文学作品陔余丛考的出版社是哪家？', ['陔余丛考', '出版社'], '+'],
              ['顾亭林诗集汇注是由哪个出版社出版的？', ['顾亭林诗集汇注', '出版社'], '+'],
              ['中山大学是哪个机构的下属机构？', ['中山大学', '下属机构'], '+'],
              ['朝鲜半岛：地缘环境的挑战与应战的出版社是哪家？',
               ['朝鲜半岛：地缘环境的挑战与应战', '出版社'], '+'],
              ['韩愈的父亲有哪些？', ['韩愈', '父亲'], '+'],
              ['段成式的代表作品是什么？', ['段成式', '代表作品'], '+'],





              ['杜并是谁的曾祖父？', ['曾祖父', '杜并'], '-'],
              ['谁的曾祖父是杜并？', ['曾祖父', '杜并'], '-'],

              ['狼殿下的主要演员有多少个？', ['狼殿下', '主要演员'], '+c'],


              ['韩愈的父亲的母亲是谁？', ['韩愈', '父亲', '母亲'], '++'],
              ['廖四平的作品是由哪个出版社出版的？', ['廖四平', '作品', '出版社'], '++'],

              ['岭表纪年/所知录/天南逸史这些作品的作者是谁？他还写过哪些作品？',
               ['岭表纪年/所知录/天南逸史', '作者', '作品', '作品'], '+l+-'],



              ['湘潭大学的现任领导中，有哪些人也是该校的知名人物？', ['湘潭大学', '现任领导', '湘潭大学', '知名人物'], '+++'],
              ['暮白首的主要演员中，有哪些人同时也是主要配音？', ['暮白首', '主要演员', '暮白首', '主要配音'], '+++'],
              ['汤非的音乐作品中，哪些歌曲的原唱是他自己？', ['汤非', '音乐作品', '汤非', '原唱'], '+++'],
              ['切斯·克劳福的搭档中，谁同时也是灵魂冲浪的主要演员？', ['切斯·克劳福', '搭档', '灵魂冲浪', '主要演员'], '+++'],

              ['朴叙俊的搭档中，有多少人也是寄生虫的主要演员？', ['朴叙俊', '搭档', '寄生虫', '主要演员'], '+++c'],





              ['写不出来~编剧吉丸圭佑的没有条理的生活∼的演员中，有哪些人的代表作品是穿越时空的少女？',
               ['写不出来~编剧吉丸圭佑的没有条理的生活∼', '演员', '代表作品', '穿越时空的少女'], '+-'],
              ['林贤治的作品中，哪本书的出版社是中国社会科学出版社？', ['林贤治', '作品', '出版社', '中国社会科学出版社'],
               '+-'],
              ['徐光兴的作品中，哪一本是由山东文艺出版社出版的？', ['徐光兴', '作品', '出版', '山东文艺出版社'], '+-'],




              ['参演过顶楼的演员中，有哪些人的代表作品是顺风妇产科"？', ['参演', '顶楼', '代表作品', '顺风妇产科"'], '--'],



              ['王遵古和王庭筠是什么关系？', ['王遵古', '王庭筠'], '<>']]


        s = [['丹尼·伯恩和吉约姆·卡内共同制作过哪些电影？', ['丹尼·伯恩', '制作', '吉约姆·卡内', '制作'], '+++'],
              ['皮尔斯·布鲁斯南和卡雅·斯考达里奥共同出演过哪部电影或电视剧？', ['皮尔斯·布鲁斯南', '出演', '卡雅·斯考达里奥', '出演'], '+++'],
              ['高明在三年和赋幽慵斋中分别担任了什么角色？', ['高明', '三年', '高明', '赋幽慵斋'], '<><>'],

                ['周彦辰和陈哲远有没有共同的搭档？', ['周彦辰', '搭档', '陈哲远', '搭档'], '+++j'],


              ['马克·沃尔伯格和安东尼奥·班德拉斯都有过哪些共同的搭档？', ['马克·沃尔伯格', '搭档', '安东尼奥·班德拉斯', '搭档'], '+++'],


              ['凯拉·奈特莉和本尼迪克特·康伯巴奇共同参演过哪些电影或电视剧？'],
             ['徐良和林子琪有过哪些合作？'],
              ['黄旭熙和中本悠太有共同发行过专辑吗？'], ['朱宏嘉和柳云龙分别毕业于哪所学校？'],
              ['宋康昊和朴叙俊有没有共同的搭档？'], ['伊丽莎白·奥尔森和凯瑟琳·哈恩共同参演过哪些电影或电视剧？'],
              ['伊丽莎白·奥尔森和兰道尔·朴共同参演过哪些电影或电视剧？'],
              ['克莱尔·丹尼斯和休·丹西有没有共同出演自闭历程？'],
              ['阿米尔·汗和赫里尼克·罗斯汉有共同出演的电影吗？'],
              ['伊丽莎白·奥尔森和保罗·贝坦尼共同参演过哪些电影或电视剧？'],
              ['黄旭熙和黄仁俊有共同发行过专辑吗？'], ['徐良和郑国锋共同合作过哪些歌曲？'],
              ['丹尼·伯恩和吉约姆·卡内共同参演过哪些电影？'], ['杰米·李·柯蒂斯和西格妮·韦弗共同参演过哪些电影？'],
              ['布莱恩·丹内利和小弗雷迪·普林兹共同参演过哪些电影？'], ['清水翔太和加藤米莉亚共同创作过哪些音乐作品？'],
              ['陈瑞和梦然分别毕业于哪所学校？'], ['伊尔凡·可汗与奥米·瓦依达共同参演过哪些电影？'],
              ['余恕诚和刘学锴共同创作过哪些作品？'], ['黄莺和徐翔共同参演过哪些作品？'],
              ['李玉玺和朴所罗门有没有共同出演过的电影或电视剧？答案'],
              ['克里斯汀·贝尔和西格妮·韦弗共同参演过哪些电影？'],
              ['丹尼·伯恩和黛安·克鲁格共同参演过哪些电影？'], ['朱研和丁勇岱有没有共同的搭档？'],
              ['杰西卡·贝尔和布鲁斯·戴维森共同参演过哪些电影？'], ['柯俊雄和白虹共同参演过哪些影片？'],
              ['巴勃罗·施瑞博尔和塞斯·盖贝尔共同出演过哪部电影或电视剧？'], ['高明和贾伟分别参与了哪些作品？'],
              ['小池澈平和山下智久分别和哪些人合作过？'], ['白虹和刘琼一共参演过几部作品？'],
              ['迪丽热巴和陈若轩有没有共同的作品？'], ['山下智久和小池澈平共同参演过哪些作品？'],
              ['李栋旭和孔刘共同出演过哪部作品？'], ['赵毅和阿米尔·汗有共同参与的作品吗？'],
              ['莉·汤普森和Madelyn Deutch有没有共同出演过回到未来？'], ['雨果·维文和巴里·基奥汉有没有共同的搭档？'],
              ['杰瑞德·莱托和莉·汤普森有没有共同出演过的电影？'], ['刘多仁和景收真共同参演过哪些作品？'],
              ['细田善彦和酒井彩名共同参演过哪些作品？'], ['陈志朋和张立威有没有共同的搭档？'],
              ['道恩·强森和西格妮·韦弗共同参演过哪些电影？'], ['丹尼·伯恩和丹尼尔·布鲁赫共同参演过哪些电影？'],
              ['上坂堇和佐仓绫音有什么共同点？'], ['西尔维斯特·史泰龙和詹姆斯·布朗共同参演了哪些电影？'],
              ['陈晓和杨子姗共同参演过哪些作品？'], ['吉约姆·卡内和黛安·克鲁格共同参演过哪些电影？']]

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
            if sorted_dict[0][1] < 0.3:
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
        print('\n', index, question)
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

    with open('data5.json', 'w', encoding='utf-8') as f:
        json.dump(last_result, f, ensure_ascii=False, indent=4)


def test():
    ag = AnswerGet()
    print(ag.represent)
    fit_result = ag.fit('张说的侄子的父亲是谁？')
    print(fit_result)


get_result()
#get_result_test()
#test()
    
