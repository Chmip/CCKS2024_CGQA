from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os
r_t = {'老师': ['学生'], '作者': ['代表作品', '文学作品'], '祖父': ['孙子'], '儿子': ['父亲', '母亲'], '女儿': ['父亲', '母亲'], '丈夫': ['妻子'], '曾孙子': ['曾祖父']}
r_temp = {}
for r_index, r_list in r_t.items():
    for relation in r_list:
        if relation not in r_temp:
            r_temp[relation] = []
        r_temp[relation].append(r_index)
#print(r_temp)
#r_t.update(r_temp)
#print(r_t)
r_t = {'老师': ['学生'], '作者': ['代表作品', '文学作品'], '祖父': ['孙子'], '儿子': ['父亲', '母亲'], '女儿': ['父亲', '母亲'], '丈夫': ['妻子'], '曾孙子': ['曾祖父'], '学生': ['老师'], '代表作品': ['作者'], '文学作品': ['作者'], '孙子': ['祖父'], '妻子': ['丈夫'], '曾祖父': ['曾孙子'], '音乐作品': ['歌曲原唱'], '歌曲原唱': ['音乐作品']}
r_y = {'大舅': ['大舅子'], '爷爷': ['大爷爷'], '现任妻子': ['妻子'], '现任丈夫': ['丈夫'], '子女': ['儿子', '女儿'], '演员': ['主要演员'], '主演': ['主要演员'], '家庭成员': ['儿子','女儿', '妻子', '丈夫'], '祖先': ['祖父', '曾祖父'], '孩子': ['儿子', '女儿'], '直系亲属': ['父亲', '外祖父', '妻子'], '堂兄弟': ['堂兄', '堂弟'], '原唱': ['歌曲原唱'], '出版': ['出版社'], '作品': ['文学作品'], '下属机构': ['所属机构'], '出演': ['参演']}
#r_t = {'老师': '学生', '作者': ['代表作品', '文学作品'], '祖父': '孙子', '儿子': ['父亲', '母亲'], '丈夫': '妻子', '孙子': '曾祖父'}


r_mapping = {'儿子': [['妻子', '儿子']]}
r_mapper = {'儿子': [['父亲', '孙子']], '爷爷': [['父亲', '父亲']]}
class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"), name="neo4j")

    def default(self, E1, E2):
        if E1 == None:
            E1 = ''
        else:
            E1 = f':`{E1}`'
        if E2 == None:
            E2 = ''
        else:
            E2 = f':`{E2}`'
        return E1, E2

    def default_R(self, R):
        if R in r_y:
            if len(r_y[R]) == 1:
                return r_y[R][0]
        return R

    def e(self, E, Ename):
        if E == None:
            E1 = ''
        else:
            E1 = f':`{E}`'
        query = f'MATCH (p{E1}) where p.name="{Ename}" return p'
        print(query)
        results = self.g.run(query)
        results = results.data()
        for result in results:
            print(str(result['p'].labels)[1:])


    def er_mapper(self,E1name, R, E1=None, E2=None):
        last_result = set()
        if R in r_mapping:
            for mapper_list in r_mapping[R]:
                result = [E1name]
                for mapper_item in mapper_list:
                    if len(result) > 0:
                        result = self.er_0(E1, result[0], mapper_item, E2)
                    else:
                        break
                if len(result) > 0:
                    last_result.update(result)
        last_result.update(self.er_0(E1, E1name, R, E2))
        return list(last_result)

    def er_(self, E1name, R, E1=None, E2=None):
        last_result = set(self.er_0(E1, E1name, R, E2))
        if len(last_result) == 0:
            if R in r_mapping:
                for mapper_list in r_mapping[R]:
                    result = [E1name]
                    for mapper_item in mapper_list:
                        if len(result) > 0:
                            result = self.er_0(E1, result[0], mapper_item, E2)
                        else:
                            break
                    if len(result) > 0:
                        last_result.update(result)
        return list(last_result)

    def er_0(self, E1name, R, E1=None, E2=None):
        last_result = []
        R = self.default_R(R)
        if R in r_t:
            for item in r_t[R]:
                result = self._re(item, E1name)
                for result_item in result:
                    last_result.append(result_item)

        E1, E2 = self.default(E1, E2)
        query = f'MATCH (p{E1})-[:`{R}`]->(m{E2}) where p.name="{E1name}" return m.name'
        #print(query)
        results = self.g.run(query)
        for result in results.data():
            last_result.append(result['m.name'])
        if True:
            last_result = set(last_result)
        return list(last_result)

    def _re(self, R, E2name, E1=None, E2=None):
        E1, E2 = self.default(E1, E2)
        query = f'MATCH (p{E1})-[:`{R}`]->(m{E2}) where m.name="{E2name}" return p.name'
        #print(query)
        results = self.g.run(query)
        r = []
        for result in results.data():
            r.append(result['p.name'])
        return r

    def e_e(self, E1name, E2name, E1=None, E2=None):
        E1, E2 = self.default(E1, E2)
        query = f'MATCH (p{E1})-[r]-(m{E2}) where p.name="{E1name}" and m.name="{E2name}" return r'
        #print(query)
        results = self.g.run(query)
        r = []
        for result in results.data():
            r.append(type(result['r']).__name__)
        return r

    def e_E(self, E1, E1name, E2, E2name):
        E1, E2 = self.default(E1, E2)

        query = f'MATCH (p{E1})-[r]->(m{E2}) where p.name="{E1name}" and m.name="{E2name}" return r'
        print(query)
        result = self.g.run(query)
        print(result.data())



    def get_result(self, ref, mapper):
        if ref == '+':
            return self.er_0(mapper[0], mapper[1])
        elif ref == '-':
            return self._re(mapper[0], mapper[1])

        elif ref == '+c':
            result = len(self.er_0(mapper[0], mapper[1]))
            return [str(result)]

        elif ref == '++':
            result = self.er_0(mapper[0], mapper[1])
            if len(result) == 0:
                return ["知识库未提及"]
            return self.er_0(result[0], mapper[2])

        elif ref == '+++':
            result1 = set(self.er_0(mapper[0], mapper[1]))
            result2 = set(self.er_0(mapper[2], mapper[3]))
            return list(result1 & result2)

        elif ref == '+++c':
            result1 = set(self.er_0(mapper[0], mapper[1]))
            result2 = set(self.er_0(mapper[2], mapper[3]))
            result = len(result1 & result2)
            if result == 0:
                return ["无"]
            return [str(result)]

        elif ref == '+++j':
            result1 = set(self.er_0(mapper[0], mapper[1]))
            result2 = set(self.er_0(mapper[2], mapper[3]))
            result = len(result1 & result2)
            if result == 0:
                return ["没有"]
            return ['有']



        elif ref == '+-':
            result1 = set(self.er_0(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            return list(result1 & result2)






        elif ref == '--':
            result1 = set(self._re(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            return list(result1 & result2)



        elif ref == '+l+-':
            result1 = self.er_0(mapper[0], mapper[1])
            if len(result1) == 0:
                return ["知识库未提及"]
            result2 = self.er_0(result1[0], mapper[2])
            if mapper[0] in result2:
                result2.remove(mapper[0])
            return [result1[0]] + result2


        elif ref == '<>':
            result = set(self.e_e(mapper[0], mapper[1]))
            if len(result) == 0:
                return ["知识库未提及"]
            rl = {'表姐弟': {'表弟', '表姐'}, '搭档': {'搭档'}, '曾祖父': {'曾祖父'}, '师生关系': {'学生', '老师'}}
            for r_name, r_set in rl.items():
                if result.issubset(r_set):
                    return [r_name]
            if len(result) == 1:
                return list(result)
            return ["知识库未提及"]


        elif ref == '<><>':
            result1 = self.get_result('<>', mapper[0:2])
            result2 = self.get_result('<>', mapper[2:4])
            return result1 + result2




def test():
    searcher = AnswerSearcher()
    '''print(searcher.er_0("纽约纽约", "主要演员"))#		欧阳靖
    mapper = ['朴叙俊', '搭档', '寄生虫', '主要演员']
    result1 = set(searcher.er_0(mapper[0], mapper[1]))
    result2 = set(searcher.er_0(mapper[2], mapper[3]))
    print(result1)
    print(result2)

    print(result1 & result2)

    mapper = ['狼殿下', '主要演员']
    result1 = set(searcher.er_0(mapper[0], mapper[1]))
    result2 = set(searcher._re('参演', mapper[0]))
    print(len(result1))
    print(result2)
    result3 = result2 | result1
    print(result3)
    print(len(result3))'''




    result1 = searcher.get_result('<><>', ['小池澈平', '玉置成实', '高明', '赋幽慵斋'])
    print(result1)




    #searcher.ER_(None, "岭表纪年/所知录/天南逸史", "作者", None)

#test()
