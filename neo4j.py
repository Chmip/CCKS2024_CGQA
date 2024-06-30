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
r_t = {'老师': ['学生'], '作者': ['代表作品', '文学作品'], '祖父': ['孙子'], '儿子': ['父亲', '母亲'], '女儿': ['父亲', '母亲'], '丈夫': ['妻子'], '曾孙子': ['曾祖父'], '学生': ['老师'], '代表作品': ['作者'], '文学作品': ['作者'], '孙子': ['祖父'], '妻子': ['丈夫'], '曾祖父': ['曾孙子']}


r_mapping = {'儿子': [['妻子', '儿子']]}
r_mapper = {'儿子': [['父亲', '孙子']], '爷爷': [['父亲', '父亲']]}
class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"), name="neo4j")

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


    def er_mapper(self, E1, E1name, R, E2):
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

    def er_(self, E1, E1name, R, E2):
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

    def er_0(self, E1, E1name, R, E2):
        last_result = []
        if R in r_t:
            for item in r_t[R]:
                result = self._re(None, item, E1, E1name)
                for result_item in result:
                    last_result.append(result_item)
        if E1 == None:
            E1 = ''
        else:
            E1 = f':`{E1}`'
        if E2 == None:
            E2 = ''
        else:
            E2 = f':`{E2}`'
        query = f'MATCH (p{E1})-[:`{R}`]->(m{E2}) where p.name="{E1name}" return m.name'
        #print(query)
        results = self.g.run(query)
        for result in results.data():
            last_result.append(result['m.name'])
        if True:
            last_result = set(last_result)
        return list(last_result)

    def _re(self, E1, R, E2, E2name):
        if E1 == None:
            E1 = ''
        else:
            E1 = f':`{E1}`'
        if E2 == None:
            E2 = ''
        else:
            E2 = f':`{E2}`'
        query = f'MATCH (p{E1})-[:`{R}`]->(m{E2}) where m.name="{E2name}" return p.name'
        #print(query)
        results = self.g.run(query)
        r = []
        for result in results.data():
            r.append(result['p.name'])
        return r

    def e_e(self, E1, E1name, E2, E2name):
        if E1 == None:
            E1 = ''
        else:
            E1 = f':`{E1}`'
        if E2 == None:
            E2 = ''
        else:
            E2 = f':`{E2}`'

        query = f'MATCH (p{E1})-[r]-(m{E2}) where p.name="{E1name}" and m.name="{E2name}" return r'
        print(query)
        result = self.g.run(query)
        print(result.data())

    def e_E(self, E1, E1name, E2, E2name):
        if E1 == None:
            E1 = ''
        else:
            E1 = f':`{E1}`'
        if E2 == None:
            E2 = ''
        else:
            E2 = f':`{E2}`'

        query = f'MATCH (p{E1})-[r]->(m{E2}) where p.name="{E1name}" and m.name="{E2name}" return r'
        print(query)
        result = self.g.run(query)
        print(result.data())



def test():
    searcher = AnswerSearcher()
    searcher.er_(None, "元晔", "儿子", None)
    #searcher.ER_(None, "岭表纪年/所知录/天南逸史", "作者", None)

#test()