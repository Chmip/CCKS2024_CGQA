

import re
import json
import sys
import os
import numpy as np


relation = [['堂姐', '侄孙媳妇', '弟媳', '导师', '堂小舅子', '大爷爷', '师爷', '继母', '未婚夫', '前夫', '姑妈', '恋人',
             '第三任妻子', '师妹', '第一任妻子', '养父', '对手', '养母', '女儿', '原配', '挚爱', '义妹', '曾孙子',
             '侄孙子', '养女', '公公', '姨父', '堂侄', '丈夫', '第二任妻子', '岳父', '外祖父', '伯父', '学弟', '师父',
             '伴侣', '表哥', '学长', '妹夫', '姐姐', '师祖', '嫡母', '岳母', '男友', '曾外孙子', '舅母', '前女友',
             '堂兄', '老师', '爱人', '小叔子', '儿子', '女朋友', '奶奶', '恩师', '外孙', '侄子', '弟子', '师弟', '母亲',
             '堂哥', '前儿媳', '舅父', '妻子', '外孙女', '第二任丈夫', '生父', '旧爱', '朋友', '妻姐', '养子', '兄弟',
             '曾外祖父', '前男友', '外曾孙子', '堂弟', '继父', '大伯哥', '徒弟', '知己', '儿媳', '堂伯父', '女婿',
             '亲家公', '曾祖父', '叔父', '姑母', '继子', '师傅', '外甥', '姑父', '学妹', '小姑子', '第四任妻子', '偶像',
             '前任', '表姨', '亲家母', '战友', '生母', '外曾祖母', '祖父', '小舅子', '庶子', '表妹', '嫂子', '好友',
             '前公公', '义女', '师兄', '曾孙', '同学', '外曾祖父', '男朋友', '叔叔', '大姨子', '义子', '曾祖母',
             '未婚妻', '姨夫', '表姑父', '义兄', '表侄', '连襟', '姐夫', '学生', '弟弟', '同门', '师生', '先夫',
             '叔外公', '曾孙女', '教练', '侄孙', '妹妹', '前队友', '表兄', '孙子', '亡妻', '第六任妻子', '搭档', '伯母',
             '祖母', '表叔', '伯乐', '婶母', '婆婆', '外曾孙女', '表弟', '外甥女婿', '第五任妻子', '继女', '叔外祖父',
             '妾', '妯娌', '义弟', '哥哥', '大舅子', '义父', '伯伯', '父亲', '外祖母', '第一任丈夫', '外孙子', '玄孙',
             '姑姑', '师姐', '大舅哥', '队友', '外甥女', '小姨子', '堂妹', '曾外祖母', '学姐', '义母', '堂舅', '大姑子',
             '孙女', '表姐', '姨母', '前妻', '侄女'],
            ['主要配音', '主要演员', '主要角色', '歌曲原唱', '作者', '创始人', '历任领导', '领导', '现任领导', '法人'],
            ['连载平台', '合作人', '文学作品', '摄影作品', '办学性质', '其他关系', '发行专辑',
             '设立单位', '成员', '办学团体', '综艺节目', '创始人', '员工', '执导',
             '代表作品', '学校特色', '创办', '旗下艺人', '音乐视频', '助理', '院系设置', '云孙', '社长',
             '学校身份', '主要作品', '类别', '毕业院校', '知名人物', '所属机构', '制作', '登场作品', '配音',
             '相关国内联盟', '音乐作品', '简称', '经纪人', '为他人创作音乐', '出版社', '老板', '经纪公司', '代表',
             '继任', '参演', '编剧', '类型', '合作院校', '专职院士数', '主持', '学校类别']]

r_y = {'大舅': ['大舅子'], '爷爷': ['大爷爷'], '现任妻子': ['妻子'], '现任丈夫': ['丈夫'], '子女': ['儿子', '女儿'], '演员': ['主要演员'], '主演': ['主要演员'], '家庭成员': ['儿子','女儿', '妻子', '丈夫'], '祖先': ['祖父', '曾祖父'], '孩子': ['儿子', '女儿'], '直系亲属': ['父亲','外祖父', '妻子'], '堂兄弟': ['堂兄', '堂弟']}
r_t = {'老师': '学生', '作者': ['代表作品', '文学作品'], '祖父': '孙子', '儿子': ['父亲', '母亲'], '丈夫': '妻子', '孙子': '曾祖父'}


relation2 = [['大舅', '爷爷', '现任妻子', '现任丈夫', '子女', '演员', '主演', '家庭成员', '祖先', '孩子', '直系亲属', '堂兄弟', '表兄弟', '儿女'],
            ['原唱'],
            ['主演', '作品', '同事', '连载', '校友', '为他人创作的音乐', '毕业学校', '毕业', '专辑', '出演', '出版', '主要角色', '合作', '写', '下属机构', '编写', '角色', '属于', '出演', '母校', '唱', '性质', '创作', '演出', '毕业生', '下属机构']]


class QuestionFeature():
    def __init__(self):
        self.r = "|".join(relation[0] + relation[1] + relation2[0] + relation2[1])
        self.r2 = "|".join(relation[2] + relation[1] + relation2[2])
        self.r_all = "|".join(relation[0] + relation[1] + relation[2] + relation2[0] + relation2[1] + relation2[2])


        self.structure1 = [f'在(.*?)({self.r_all})的',f'于(.*?)参与了({self.r_all})？',f'的({self.r_all})曾经是(.*?)？','(.*?)和(.*?)共',f'同({self.r_all})过({self.r_all})吗',f'(.*?)的({self.r_all})是','(.*?)是否出演过(.*?)？',f'为(.*?)({self.r_all})了','(.*?)在(.*?)',f'(.*?)有哪些({self.r_all})？',f'的({self.r_all})中，有多少人的({self.r_all})是',f'(.*?)是哪个机构的({self.r_all})？',f'过(.*?)的演员中，有哪些人的({self.r_all})是','(.*?)在(.*?)和',f'(.*?)是由哪个({self.r_all})出',f'些({self.r_all})于(.*?)参',f'(.*?)({self.r_all})于','(.*?)和(.*?)都',f'些({self.r_all})的({self.r_all})是',f'(.*?)的({self.r_all})中',f'和(.*?)的({self.r_all})有',f'的({self.r_all})的({self.r_all})是',f'({self.r_all})过(.*?)的','(.*?)和(.*?)一',f'和(.*?)有没有共同的({self.r_all})？','(.*?)和(.*?)是',f'的({self.r_all})中，哪一本是由(.*?)',f'({self.r_all})的(.*?)是',f'(.*?)的({self.r_all})总',f'的(.*?)中，有多少人也是该学院的({self.r_all})？',f'(.*?)({self.r_all})是',f'的({self.r_all})是由哪个({self.r_all})出',f'(.*?)的({self.r_all})有','(.*?)的(.*?)中',f'的(.*?)中，有哪些人同时也是({self.r_all})？','和(.*?)是否是(.*?)',f'过(.*?)的哪些({self.r_all})？','(.*?)和(.*?)有',f'(.*?)在哪些作品中担任了({self.r_all})工',f'在(.*?)中，有哪些({self.r_all})的',f'和(.*?)一共({self.r_all})过',f'为(.*?)({self.r_all})过',f'的({self.r_all})中，哪本书的({self.r_all})是',f'(.*?)的({self.r_all})',f'的(.*?)中，有哪些人也是该校的({self.r_all})？',f'是(.*?)的({self.r_all})？',f'(.*?)这些({self.r_all})的',f'和(.*?)分别({self.r_all})于','(.*?)为(.*?)',f'是(.*?)({self.r_all})的',f'的({self.r_all})和(.*?)的',f'的(.*?)中，有几首是他的({self.r_all})？',f'和(.*?)共同({self.r_all})过',f'品(.*?)的({self.r_all})是',f'和(.*?)有共同({self.r_all})过',f'的({self.r_all})({self.r_all})过','(.*?)写过哪些(.*?)？',f'(.*?)的({self.r_all})的',f'同({self.r_all})过哪些({self.r_all})？',f'和(.*?)都有过哪些共同的({self.r_all})？',f'(.*?)这部作品中，有哪些({self.r_all})于',f'由(.*?)({self.r_all})的',f'的({self.r_all})中，谁同时也是(.*?)的',f'的({self.r_all})是谁？他还写过哪些({self.r_all})？',f'的(.*?)和({self.r_all})一','在(.*?)和(.*?)中',f'的({self.r_all})中，有多少人也是(.*?)的',f'的({self.r_all})是(.*?)？','(.*?)一共出版过几本(.*?)？','(.*?)和(.*?)分',f'(.*?)是谁的({self.r_all})？',f'的(.*?)中，哪些歌曲的({self.r_all})是',f'的(.*?)和({self.r_all})总','(.*?)的(.*?)和',f'(.*?)({self.r_all})过',f'的({self.r_all})中，有哪些人的({self.r_all})是',f'些({self.r_all})的({self.r_all})曾',f'({self.r_all})了哪些({self.r_all})？',f'(.*?)的({self.r_all})和',f'和(.*?)分别和哪些人({self.r_all})过',f'({self.r_all})过多少首({self.r_all})？']

        self.structure = [
f'在(.*?)({self.r_all})的',f'于(.*?)参与了({self.r_all})？',f'的({self.r_all})曾经是(.*?)？','(.*?)和(.*?)共',f'同({self.r_all})过({self.r_all})吗',f'(.*?)的({self.r_all})是','(.*?)是否出演过(.*?)？',f'为(.*?)({self.r_all})了','(.*?)在(.*?)',f'(.*?)有哪些({self.r_all})？',f'的({self.r_all})中，有多少人的({self.r_all})是',f'(.*?)是哪个机构的({self.r_all})？',f'过(.*?)的演员中，有哪些人的({self.r_all})是','(.*?)在(.*?)和',f'(.*?)是由哪个({self.r_all})出',f'些({self.r_all})于(.*?)参',f'(.*?)({self.r_all})于','(.*?)和(.*?)都',f'些({self.r_all})的({self.r_all})是',f'(.*?)的({self.r_all})中',f'和(.*?)的({self.r_all})有',f'的({self.r_all})的({self.r_all})是',f'({self.r_all})过(.*?)的','(.*?)和(.*?)一',f'和(.*?)有没有共同的({self.r_all})？','(.*?)和(.*?)是',f'的({self.r_all})中，哪一本是由(.*?)',f'({self.r_all})的(.*?)是',f'(.*?)的({self.r_all})总',f'的(.*?)中，有多少人也是该学院的({self.r_all})？',f'(.*?)({self.r_all})是',f'的({self.r_all})是由哪个({self.r_all})出',f'(.*?)的({self.r_all})有','(.*?)的(.*?)中',f'的(.*?)中，有哪些人同时也是({self.r_all})？','和(.*?)是否是(.*?)',f'过(.*?)的哪些({self.r_all})？','(.*?)和(.*?)有',f'(.*?)在哪些作品中担任了({self.r_all})工',f'在(.*?)中，有哪些({self.r_all})的',f'和(.*?)一共({self.r_all})过',f'为(.*?)({self.r_all})过',f'的({self.r_all})中，哪本书的({self.r_all})是',f'(.*?)的({self.r_all})',f'的(.*?)中，有哪些人也是该校的({self.r_all})？',f'是(.*?)的({self.r_all})？',f'(.*?)这些({self.r_all})的',f'和(.*?)分别({self.r_all})于','(.*?)为(.*?)',f'是(.*?)({self.r_all})的',f'的({self.r_all})和(.*?)的',f'的(.*?)中，有几首是他的({self.r_all})？',f'和(.*?)共同({self.r_all})过',f'品(.*?)的({self.r_all})是',f'和(.*?)有共同({self.r_all})过',f'的({self.r_all})({self.r_all})过','(.*?)写过哪些(.*?)？',f'(.*?)的({self.r_all})的',f'同({self.r_all})过哪些({self.r_all})？',f'和(.*?)都有过哪些共同的({self.r_all})？',f'(.*?)这部作品中，有哪些({self.r_all})于',f'由(.*?)({self.r_all})的',f'的({self.r_all})中，谁同时也是(.*?)的',f'的({self.r_all})是谁？他还写过哪些({self.r_all})？',f'的(.*?)和({self.r_all})一','在(.*?)和(.*?)中',f'的({self.r_all})中，有多少人也是(.*?)的',f'的({self.r_all})是(.*?)？','(.*?)一共出版过几本(.*?)？','(.*?)和(.*?)分',f'(.*?)是谁的({self.r_all})？',f'的(.*?)中，哪些歌曲的({self.r_all})是',f'的(.*?)和({self.r_all})总','(.*?)的(.*?)和',f'(.*?)({self.r_all})过',f'的({self.r_all})中，有哪些人的({self.r_all})是',f'些({self.r_all})的({self.r_all})曾',f'({self.r_all})了哪些({self.r_all})？',f'(.*?)的({self.r_all})和',f'和(.*?)分别和哪些人({self.r_all})过',f'({self.r_all})过多少首({self.r_all})？',

            f"(.*?)的({self.r_all})",
                           f"(.*?)({self.r_all})",
                           f"({self.r_all})是(.*?)？",

                           "的(.*?)的(.*?)是",
                           f"的({self.r_all})是(.*?)？",
                           "的([^？，]*?)和(.*?)总",
                           "的(.*?)和(.*?)中",
                           "的(.*?)和(.*?)分别",
                           f"的({self.r_all})和({self.r_all})的",

                           "(.*?)的(.*?)的",
                           "(.*?)的(.*?)有",
                           "(.*?)的(.*?)中",
                           "(.*?)的(.*?)和",
                           "({.*?})的(.*?)总",
                           "(.*?)的(.*?)的(.*?)是",
                           f"(.*?)的?({self.r_all})分别是",
                           f"(.*?)的({self.r_all})(.*?)还",
                           f"({self.r_all})(.*?)的({self.r_all})",

                           "(.*?)是",

                           "(.*?)这.*?的(.*?)是",



                           "和(.*?)的(.*?)是",
                           "和(.*?)的(.*?)分别",
                           "和(.*?)共",
                           "和(.*?)中",
                           "和(.*?)的",
                           "和(.*?)的(.*?)中",


                           "(.*?)和(.*?)分别",
                           "(.*?)和(.*?)的",
                           "(.*?)和(.*?)是",
                           "(.*?)和(.*?)有",
                           "(.*?)和(.*?)的",

                           "(.*?)在(.*?)的",
                           f"({self.r_all})过(.*?)的",
                           f"由(.*?)({self.r_all})的",
                           "在(.*?)的(.*?)有",
                           "在(.*?)这个(.*?)上",
                           "于(.*?)或(.*?)的",

                           "多少",
                           "是否",
                           "，(?:.*?)？",
                           "？(?:.*?)？"
                           '是(?:否|不)',

                           f"是(.*?)的({self.r_all})？",
                           f"是(.*?)或({self.r_all})的",
        f"是(.*?)或(.*?)？",






                           "共同",
                           "什么",
                           "总共",
                           "分别",
                           '是谁',
                           "有哪些",

                           "关系",

                           '有没',
                           '没有'
                           "有没有",
                           "最多",
                           "是哪",
                           "是该",
                           "哪一"

                            f"(.*?)的?({self.r_all})？",
                           f"(.*?)的?({self.r_all})是",
                           f"([^？，]*?)的?({self.r_all})是",
                           f"(.*?)的?({self.r_all})的",
                           f"(.*?)的?({self.r_all})又是",

                           "在?(.*?)中",
                           "在电影(.*?)中",

                           f"([^？，]*?)和(.*?)的({self.r_all})中",
                           f"电视剧(.*?)的({self.r_all})有",
                           f"在?(.*?)的({self.r_all})中",
                           f"在(.*?)({self.r_all})的",
                           f"有.*?过(.*?)的({self.r_all})",
                           f"有({self.r_all})过(.*?)的({self.r_all})中",
                           f"(.*?)({self.r_all})过(.*?)的",
                           f'({self.r_all})过"(.*?)"',
                           f"([^？，]*?)有哪些({self.r_all})？",

                           f"(.*?)和(.*?)共同的?({self.r_all})有？",
                           f"(.*?)和(.*?)共同.*?的({self.r_all})有",
                           f"(.*?)和(.*?)共同({self.r_all})的",
                           f"和(.*?)的({self.r_all})相同",

                           f"(?:[^？，]*?)有哪些({self.r_all})的",
                           f"(?:[^？，]*?)有哪些.*?的({self.r_all})",
                           f"(?:[^？，]*?)有哪些.*?是?({self.r_all})？",
                           f"([^？，]*?)的?({self.r_all})有哪些人?",
                           f"(?:[^？，]*?)有哪些人的({self.r_all})是(.*?)？",
                           f"([^？，]*?)在(.*?)的({self.r_all})有",
                           f".*?毕业于(.*?)参与了({self.r_all})",
                           f"(.*?)参与的电影中，他既是({self.r_all})同时是({self.r_all})的",
                           f"(.*?)是.*?学校({self.r_all})的",
                           f"的({self.r_all})有",
                           f"({self.r_all})是哪",
                           f'({self.r_all})"(.*?)"',
                           f'({self.r_all})是"(.*?)"',
                           f"([^？，]*?)写过的(.*?)有哪些",
                           f"的(?:{self.r_all})(.*?)一起",
                           f"同时({self.r_all})了?(.*?)？",

                           f"是(.*?)为他创作的",
                           f"有哪些人({self.r_all})过",


                           ]


    def parser(self, question):
        result = {}
        result['code'] = []
        for index, structure_item in enumerate(self.structure):
            result_item = self.search(structure_item, question)
            if result_item != False:
                result[index] = result_item
                result['code'].append(1)
            else:
                result['code'].append(0)
        return result

    def search(self, target_structure, question):
        match = re.search(target_structure, question, re.DOTALL)
        if match:
            found_subtree = match.groups()

            return found_subtree
        else:
            return False

    def get_simcos(self, question1, question2):
        result1 = self.parser(question1)
        result2 = self.parser(question2)
        similarity = self.cosine_similarity(result1['code'], result2['code'])
        return similarity


    def cosine_similarity(self, vector1, vector2):
        vector1 = np.array(vector1)
        vector2 = np.array(vector2)

        dot_product = np.dot(vector1, vector2)
        norm_vector1 = np.linalg.norm(vector1)
        norm_vector2 = np.linalg.norm(vector2)

        if norm_vector1 == 0 or norm_vector2 == 0:
            return 0

        similarity = dot_product / (norm_vector1 * norm_vector2)

        return similarity
















def test():
    P = QuestionFeature()
    dict = []
    code_index = {}
    with open('./data/train_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
        for key, _ in qa_data.items():
            q = qa_data[key]['question']
            result = P.parser(q)
            if result:
                if str(result['code']) not in code_index:
                    code_index[str(result['code']) ] = []
                code_index[str(result['code']) ].append(key)
                #print(q, "------------>", result)
                for i,j in result.items():
                    if i == 'code':
                        pass
                    #print(i, end=' ')
                    for item in j:
                        pass
                        #print(item, end=' ')
                    #print('\n')
                #print('\n')

            else:
                dict.append(key)
                #print("\n", q, "\n")



    #print("有",len(dict),'个没有匹配到;')



    #print(len(code_index))


    sorted_dict = sorted(code_index.items(), key=lambda x: len(x[1]), reverse=True)
    return sorted_dict








def resd_qa():
    with open('./data/train_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
    return qa_data


def main():
    qa_data = resd_qa()
    codes_dict = test()
    for key, index_list in codes_dict:
        print('key:', key)
        for index in index_list:
            print(qa_data[index]['question'])
        print('\n\n\n')


main()


