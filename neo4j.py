from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher
import os


class AnswerSearcher:
    def __init__(self):
        self.g = Graph("http://localhost:7474", auth=("neo4j", "123456"), name="neo4j")

    def cx(self, people, rex):
        query = 'MATCH (p:`人物`)-[:`{0}`]->(m:`人物`) where p.name="{1}" return m.name'.format(rex, people)
        print(query)
        result = self.g.run(query)
        print(result.data())



def test():
    searcher = AnswerSearcher()
    searcher.cx("梁棠", "侄子")