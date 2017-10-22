import requests
from bs4 import BeautifulSoup


def get_page_documents_dict_tags(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    tags = soup.find(id='dlpage').find('dl')
    document_tags = [*zip(tags.find_all('dd'), tags.find_all('dt'))]
    return [{'author': document[0].find(class_='list-authors'), 'title': document[0].find(class_='list-title mathjax'),
             'subjects': document[0].find(class_='list-subjects'), 'comments': document[0].find(class_='list-comments'),
             'link': document[1].find(class_='list-identifier'), 'content': document[0].find('p')}
            for document in document_tags]


def page_document_to_str(document_dict_tags):
    return '%s\n%s\n%s\n%s\n\n%s\n\n%s' % \
           (document_dict_tags['title'].text.strip(), document_dict_tags['author'].text.strip(),
            document_dict_tags['subjects'].text.strip(),
            document_dict_tags['comments'].text.strip() if document_dict_tags['comments'] is not None else '',
            document_dict_tags['content'].text.strip(), document_dict_tags['link'].text.strip())


documents_dicts_tags = get_page_documents_dict_tags('https://arxiv.org/list/quant-ph/new')
documents_raw_texts = [page_document_to_str(document_dict_tags) for document_dict_tags in documents_dicts_tags]
