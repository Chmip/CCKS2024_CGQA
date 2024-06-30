

from neo4j import AnswerSearcher
from classify import QuestionPaser
import json


r_y = {'大舅': ['大舅子'], '爷爷': ['大爷爷'], '现任妻子': ['妻子'], '现任丈夫': ['丈夫'], '子女': ['儿子', '女儿'], '演员': ['主要演员'], '主演': ['主要演员'], '家庭成员': ['儿子','女儿', '妻子', '丈夫'], '祖先': ['祖父', '曾祖父'], '孩子': ['儿子', '女儿'], '直系亲属': ['父亲','外祖父', '妻子'], '堂兄弟': ['堂兄', '堂弟'], '原唱': ['歌曲原唱']}
#r_t = {'老师': '学生', '作者': ['代表作品', '文学作品'], '祖父': '孙子', '儿子': ['父亲', '母亲'], '丈夫': '妻子', '孙子': '曾祖父'}


def get_result():
    searcher = AnswerSearcher()
    P = QuestionPaser()
    dict = []
    code_index = {}
    cont = 0
    last_result = {}
    with open('./data/test_qa.json', 'r', encoding='utf-8') as f:
        qa_data = json.loads(f.read())
        for index, _ in qa_data.items():
            question = qa_data[index]['question']
            response = P.parser(question)
            last_result[str(index)] = []
            if response:
                if response['code'] == '01100000000000011000000000000000000000000000000000000':
                    cont += 1
                    print(index, end='')
                    print(question)
                    '''for i, j in result.items():
                                            if i == 'code':
                                                pass
                                            print(i, end=' ')
                                            for item in j:
                                                print(item, end=' ')
                                            print('\n')
                                        print('\n')'''  #
                    token = response[1]
                    print(token[0], token[1])

                    if token[1] in r_y:
                        for token_1 in r_y[token[1]]:
                            result = searcher.er_0(None, token[0], token_1, None)
                            last_result[str(index)] += result
                    else:
                        last_result[str(index)] = searcher.er_0(None, token[0], token[1], None)
                    '''print(last_result[str(index)])
                    if last_result[str(index)] != qa_data[str(index)]["answer"]:
                        cont += 1
                        print(qa_data[str(index)]["answer"])
                        print("\n", question, "\n")'''
            if last_result[str(index)] == []:
                last_result[str(index)] = ['无']
    with open('data2.json', 'w', encoding='utf-8') as f:
        json.dump(last_result, f, ensure_ascii=False, indent=4)


    print(cont)








get_result()
    