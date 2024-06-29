from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os


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

    def er_(self, E1, E1name, R, E2):
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
        r = []
        for result in results.data():
            r.append(result['m.name'])
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


    searcher.er_(None, "钱澄之", "文学作品", None)




    #searcher.ER_(None, "岭表纪年/所知录/天南逸史", "作者", None)

#test()