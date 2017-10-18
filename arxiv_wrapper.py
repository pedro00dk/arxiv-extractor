import nltk
import requests
from bs4 import BeautifulSoup


def get_page_documents_grouped_tags(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup.find(id='dlpage').find('dl')
    document_tags = [*zip(tags.find_all('dd'), tags.find_all('dt'))]
    return [{'author': document[0].find(class_='list-authors'), 'title': document[0].find(class_='list-title mathjax'),
             'subjects': document[0].find(class_='list-subjects'), 'comments': document[0].find(class_='list-comments'),
             'link': document[1].find(class_='list-identifier'), 'content': document[0].find('p')}
            for document in document_tags]


def get_author_names(authors_div):
    return ', '.join([anchor.text for anchor in authors_div.find_all('a')]).strip()


def get_title(title_div):
    return title_div.text.strip()[7:]


def get_subjects(subject_div):
    return subject_div.text.strip()[10:]


def get_comments(comments_div):
    return comments_div.text.strip()[10:] if comments_div is not None else ''


def get_link(link_div):
    return link_div.find('a').text.strip()


def get_relations(abstract_div):
    text = abstract_div.text
    sentences = nltk.sent_tokenize(text)
    tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
    tagged_sentences = [nltk.pos_tag(sentence) for sentence in tokenized_sentences]
    comma_split_sentences = []
    for tagged_sentence in tagged_sentences:
        comma_split_sentences.append([])
        for word, clazz in tagged_sentence:
            if clazz is not ',':
                comma_split_sentences[len(comma_split_sentences) - 1].append((word, clazz))
            else:
                comma_split_sentences.append([])

    relations = []
    for sentence in comma_split_sentences:
        relation = None
        actors = ([], [])
        for word, clazz in sentence:
            if relation is None and clazz not in ['VBD', 'VBP', 'VBZ', 'VBZ']:
                actors[0].append(word)
            elif relation is None:
                relation = word
            else:
                actors[1].append(word)
        if relation is not None:
            relations.append((relation, actors))
    return relations


documents_tags = get_page_documents_grouped_tags('https://arxiv.org/list/quant-ph/new')

documents = []

for document_tags in documents_tags:
    documents.append({
        'author': get_author_names(document_tags['author']),
        'title': get_title(document_tags['title']),
        'subjects': get_subjects(document_tags['subjects']),
        'comments': get_comments(document_tags['comments']),
        'link': get_link(document_tags['link']),
        'content': get_relations(document_tags['content']),
    })

import pprint

pprint.PrettyPrinter(4).pprint(documents[0]['content'])
