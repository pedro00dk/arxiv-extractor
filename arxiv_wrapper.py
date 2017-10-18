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
    return comments_div.text.strip()[10:]


def get_link(link_div):
    return link_div.find('a').text.strip()


def get_relations(abstract_div):
    return abstract_div.text


documents_tags = get_page_documents_grouped_tags('https://arxiv.org/list/quant-ph/new')
