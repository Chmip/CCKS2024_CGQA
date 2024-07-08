from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"), name="neo4j")
        self.r_replace = {'大舅': ['大舅子'], '爷爷': ['祖父'], '现任妻子': ['妻子'], '现任丈夫': ['丈夫'],
                          '子女': ['儿子', '女儿'], '演员': ['主要演员'], '主演': ['主要演员'],
                          '家庭成员': ['儿子', '女儿', '妻子', '丈夫'], '祖先': ['祖父', '曾祖父'],
                          '孩子': ['儿子', '女儿'], '直系亲属': ['父亲', '外祖父', '妻子'], '堂兄弟': ['堂兄', '堂弟'],
                          '原唱': ['歌曲原唱'], '出版': ['出版社'], '作品': ['文学作品'], '下属机构': ['所属机构'],
                          '出演': ['参演'], '专辑': ['发行专辑'], '毕业': ['毕业院校'], '合作': ['搭档'],
                          '书': ['文学作品', '代表作品'], '为他人创作的音乐': ['为他人创作音乐'],
                          '创作': ['为他人创作音乐']}

        self.r_mapper = {'儿子': [['父亲', '孙子'], ['妻子', '儿子']], '祖父': [['父亲', '父亲']], '父亲': [['祖父', '儿子']], '曾祖父': [['祖父', '父亲']],}

        self.r_transform = {'老师': ['学生'], '作者': ['代表作品', '文学作品'], '祖父': ['孙子'], '爷爷': ['孙子'],'儿子': ['父亲', '母亲'], '女儿': ['父亲', '母亲'], '丈夫': ['妻子'], '曾孙子': ['曾祖父'], '音乐作品': ['歌曲原唱'],}
        self.initialize()

    def initialize(self):
        r_temp = {}
        for r_index, r_list in self.r_transform.items():
            for relation in r_list:
                if relation not in r_temp:
                    r_temp[relation] = []
                r_temp[relation].append(r_index)
        self.r_transform.update(r_temp)


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
        if R in self.r_replace:
            if len(self.r_replace[R]) == 1:
                return self.r_replace[R][0]
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

    def er_(self, E1name, R, E1=None, E2=None):
        last_result = []
        if R in self.r_replace:
            for item in self.r_replace[R]:
                result = self.er_mapper(E1name, item)
                for result_item in result:
                    last_result.append(result_item)
        else:
            last_result = self.er_mapper(E1name, R)
        return last_result


    def er_mapper(self,E1name, R, E1=None, E2=None):
        last_result = set(self.er_transform(E1name, R))
        if R in self.r_mapper:
            for mapper_list in self.r_mapper[R]:
                result = [E1name]
                for mapper_item in mapper_list:
                    if len(result) > 0:
                        print(result[0], mapper_item)
                        result = self.er_transform(result[0], mapper_item)

                    else:
                        break
                if len(result) > 0:
                    last_result.update(result)
        return list(last_result)



    def er_transform(self, E1name, R, E1=None, E2=None):
        R = self.default_R(R)
        last_result = set(self.er_0(E1name, R))
        if R in self.r_transform:
            for item in self.r_transform[R]:
                result = self._re(item, E1name)
                last_result.update(result)
        return list(last_result)

    def er_0(self, E1name, R, E1=None, E2=None):
        last_result = []
        E1, E2 = self.default(E1, E2)
        R = self.default_R(R)
        query = f'MATCH (p{E1})-[:`{R}`]->(m{E2}) where p.name="{E1name}" return m.name'
        results = self.g.run(query)
        for result in results.data():
            last_result.append(result['m.name'])
        if True:
            last_result = set(last_result)
        return list(last_result)

    def _re(self, R, E2name, E1=None, E2=None):
        E1, E2 = self.default(E1, E2)
        R = self.default_R(R)
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
            return self.er_transform(mapper[0], mapper[1])
        elif ref == '-':
            return self._re(mapper[0], mapper[1])

        elif ref == '+c':
            result = len(self.er_transform(mapper[0], mapper[1]))
            return [str(result)]

        elif ref == '+c+c':
            result1 = len(self.er_transform(mapper[0], mapper[1]))
            result2 = len(self.er_transform(mapper[2], mapper[3]))
            return [str(result1 + result2)]

        elif ref == '-c':
            result = len(self._re(mapper[0], mapper[1]))
            return [str(result)]

        elif ref == '+>+':
            result = self.er_transform(mapper[0], mapper[1])
            if len(result) == 0:
                return ["知识库未提及"]
            return self.er_transform(result[0], mapper[2])

        elif ref == '++&':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self.er_transform(mapper[2], mapper[3]))
            return list(result1 & result2)

        elif ref == '+l+':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self.er_transform(mapper[2], mapper[3]))
            return list(result1) + list(result2)

        elif ref == '++&c':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self.er_transform(mapper[2], mapper[3]))
            result = len(result1 & result2)
            if result == 0:
                return ["无"]
            return [str(result)]

        elif ref == '++|c':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self.er_transform(mapper[2], mapper[3]))
            result = len(result1 | result2)
            if result == 0:
                return ["无"]
            return [str(result)]

        elif ref == '+-&c':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            result = len(result1 & result2)
            if result == 0:
                return ["无"]
            return [str(result)]

        elif ref == '+-|c':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            result = len(result1 | result2)
            if result == 0:
                return ["无"]
            return [str(result)]

        elif ref == '++&j':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self.er_transform(mapper[2], mapper[3]))
            result = len(result1 & result2)
            if result == 0:
                return ["无"]
            return ['有']



        elif ref == '+-&':
            result1 = set(self.er_transform(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            return list(result1 & result2)





        elif ref == '--&':
            result1 = set(self._re(mapper[0], mapper[1]))
            result2 = set(self._re(mapper[2], mapper[3]))
            return list(result1 & result2)



        elif ref == '+l+-':
            result1 = self.er_transform(mapper[0], mapper[1])
            if len(result1) == 0:
                return ["知识库未提及"]
            result2 = self.er_transform(result1[0], mapper[2])
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

        elif ref == '<>j':
            result = set(self.e_e(mapper[0], mapper[1]))
            if len(result) == 0:
                return ["否"]
            elif len(result) > 0:
                return ["是"]


        elif ref == '<><>':
            result1 = self.get_result('<>', mapper[0:2])
            result2 = self.get_result('<>', mapper[2:4])
            return result1 + result2



        else:
            print('不存在：', ref)




def test():
    searcher = AnswerSearcher()
    '''print(searcher.er_transform("纽约纽约", "主要演员"))#		欧阳靖
    mapper = ['朴叙俊', '搭档', '寄生虫', '主要演员']
    result1 = set(searcher.er_transform(mapper[0], mapper[1]))
    result2 = set(searcher.er_transform(mapper[2], mapper[3]))
    print(result1)
    print(result2)

    print(result1 & result2)

    mapper = ['狼殿下', '主要演员']
    result1 = set(searcher.er_transform(mapper[0], mapper[1]))
    result2 = set(searcher._re('参演', mapper[0]))
    print(len(result1))
    print(result2)
    result3 = result2 | result1
    print(result3)
    print(len(result3))'''




    '''result1 = searcher.get_result('+-&c', ['狼殿下', '主要演员', '参演', '狼殿下'])
    print(result1)
    result1 = searcher.get_result('+-|c', ['狼殿下', '主要演员', '参演', '狼殿下'])
    print(result1)

    result1 = searcher.get_result('+c', ['白虹', '参演'])
    print(result1)
    result1 = searcher.get_result('+', ['灵笼', '主要配音'])
    print(1,result1)
    result1 = searcher.get_result('-', ['毕业','上海戏剧学院'])
    print(2, result1)
    result1 = searcher.get_result('++&c',['李建复', '音乐作品', '李建复', '代表作品'])
    print(3,result1)
    result1 = searcher.get_result('++&j', ['厄尔·巴隆', '毕业', '杰伦·杜伦', '毕业', '同一所大学'])
    print(4,result1)'''



    result = searcher.er_('七侠五义', '作者')
    print(result)


    #searcher.ER_(None, "岭表纪年/所知录/天南逸史", "作者", None)

test()