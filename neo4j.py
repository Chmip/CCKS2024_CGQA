from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"), name="neo4j")

    def cx(self, E1, E1name, R, E2):
        query = f'MATCH (p:`{E1}`)-[:`{R}`]->(m:`{E2}`) where p.name="{E1name}" return m.name'
        print(query)
        result = self.g.run(query)
        print(result.data())



def test():
    searcher = AnswerSearcher()
    searcher.cx("人物", "梁棠", "侄子", "人物")

test()
