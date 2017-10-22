import os

import nltk
from bs4 import BeautifulSoup
from nltk.parse.stanford import StanfordParser
from nltk.tree import ParentedTree


def get_page_documents_dict_tags():
    with open('Quantum Physics news.html', encoding='utf-8') as page:
        soup = BeautifulSoup(page, 'html.parser')
    tags = soup.find(id='dlpage').find('dl')
    document_tags = [*zip(tags.find_all('dd'), tags.find_all('dt'))]
    return [{'author': document[0].find(class_='list-authors'), 'title': document[0].find(class_='list-title mathjax'),
             'subjects': document[0].find(class_='list-subjects'), 'comments': document[0].find(class_='list-comments'),
             'link': document[1].find(class_='list-identifier'), 'content': document[0].find('p')}
            for document in document_tags]


# Breadth First Search the tree and take the first noun in the NP subtree.
def find_subject(t):
    for s in t.subtrees(lambda t: t.label() == 'NP'):
        for n in s.subtrees(lambda n: n.label().startswith('NN')):
            return (n[0], find_attrs(n))


# Depth First Search the tree and take the last verb in VP subtree.
def find_predicate(t):
    v = None

    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label().startswith('VB')):
            v = n
    return (v[0], find_attrs(v))


# Breadth First Search the siblings of VP subtree
# and take the first noun or adjective
def find_object(t):
    for s in t.subtrees(lambda t: t.label() == 'VP'):
        for n in s.subtrees(lambda n: n.label() in ['NP', 'PP', 'ADJP']):
            if n.label() in ['NP', 'PP']:
                for c in n.subtrees(lambda c: c.label().startswith('NN')):
                    return (c[0], find_attrs(c))
            else:
                for c in n.subtrees(lambda c: c.label().startswith('JJ')):
                    return (c[0], find_attrs(c))


def find_attrs(node):
    attrs = []
    p = node.parent()

    # Search siblings of adjective for adverbs
    if node.label().startswith('JJ'):
        for s in p:
            if s.label() == 'RB':
                attrs.append(s[0])

    elif node.label().startswith('NN'):
        for s in p:
            if s.label() in ['DT', 'PRP$', 'POS', 'JJ', 'CD', 'ADJP', 'QP', 'NP']:
                attrs.append(s[0])

    # Search siblings of verbs for adverb phrase
    elif node.label().startswith('VB'):
        for s in p:
            if s.label() == 'ADVP':
                attrs.append(' '.join(s.flatten()))

    # Search uncles
    # if the node is noun or adjective search for prepositional phrase
    if node.label().startswith('JJ') or node.label().startswith('NN'):
        for s in p.parent():
            if s != p and s.label() == 'PP':
                attrs.append(' '.join(s.flatten()))

    elif node.label().startswith('VB'):
        for s in p.parent():
            if s != p and s.label().startswith('VB'):
                attrs.append(' '.join(s.flatten()))

    return attrs


documents_dicts_tags = get_page_documents_dict_tags()[:20]

stanford_parser_jar = 'C:\\Users\\pedro\\Downloads\\stanford-corenlp\\stanford-corenlp-3.8.0.jar'
stanford_models_jar = 'C:\\Users\\pedro\\Downloads\\stanford-corenlp\\stanford-corenlp-3.8.0-models.jar'
os.environ['JAVAHOME'] = 'C:\\Program Files\\Java\\jdk-9.0.1\\bin'
parser = StanfordParser(path_to_jar=stanford_parser_jar, path_to_models_jar=stanford_models_jar)

for index, document_dict_tags in enumerate(documents_dicts_tags):
    print(index)
    for sentence in nltk.sent_tokenize(document_dict_tags['content'].text):
        sentence = sentence.replace('\n', ' ')
        print(sentence)
        for raw_sentence in parser.raw_parse(sentence):
            tree = ParentedTree.convert(raw_sentence)
            # tree.pretty_print()
            print(find_subject(tree))
            print(find_predicate(tree))
            print(find_object(tree))
            print()
            print()
