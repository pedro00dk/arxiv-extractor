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

