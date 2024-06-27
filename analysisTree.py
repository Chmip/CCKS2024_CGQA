

class Node(object):
    def __init__(self, item):
        self.word = item
        self.words = []
        self.lchild = None
        self.rchild = None


class Tree(object):
    def __init__(self):
        self.root = None

    def generate(self, tok, dep):
        index = 0
        dep = self.format(dep)

        node = Node(tok[index])
        if index in dep:
            for dep_item in dep[index]:
                node = Node(tok)

    def format(self, dep):
        format_dep = {}
        for index, value in enumerate(dep):
            x = value[0] - 1
            if x not in format_dep:
                format_dep[x] = []
            format_dep[x].append([index, value[1]])
        return format_dep




def test():
    doctok = ['陈沆', '的', '哥哥', '是', '谁', '？']
    value = [[3, 'nmod:assmod'], [1, 'case'], [5, 'nsubj'], [5, 'cop'], [0, 'root'], [5, 'punct']]

    tree = Tree()
    dep = tree.format(value)
    print(dep)
    ing = 0
    while value[ing][0] != 0:
        print(doctok[ing])
        ing = value[ing][0] - 1
        print(ing)
