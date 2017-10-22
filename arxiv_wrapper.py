import nltk
from bs4 import BeautifulSoup


def get_page_documents_dict_tags():
    with open('Quantum Physics news.html', encoding='utf-8') as page:
        soup = BeautifulSoup(page, 'html.parser')
    dl_tags = soup.find(id='dlpage').find_all('dl')[:2]
    documents = []
    for dl_tag in dl_tags:
        document_tags = [*zip(dl_tag.find_all('dd'), dl_tag.find_all('dt'))]
        documents.extend(
            [{'author': document[0].find(class_='list-authors'), 'title': document[0].find(class_='list-title mathjax'),
              'subjects': document[0].find(class_='list-subjects'),
              'comments': document[0].find(class_='list-comments'),
              'link': document[1].find(class_='list-identifier'), 'content': document[0].find('p')}
             for document in document_tags])
    return documents


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


def get_relations(content_div):
    text = content_div.text
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
        for index, (word, clazz) in enumerate(sentence):
            if len(actors[0]) == 0 and clazz in ['IN', 'CC']:
                continue
            if relation is None and clazz not in ['VBD', 'VBP', 'VBZ']:
                actors[0].append(word)
            elif relation is None:
                relation = word
            else:
                if clazz == 'CC':
                    found_verb = False
                    for i in range(index + 1, len(sentence)):
                        found_verb = sentence[i][1] in ['VBD', 'VBP', 'VBZ']
                        if found_verb:
                            break
                    if found_verb:
                        relations.append((relation, actors))
                        relation = None
                        actors = ([], [])
                    else:
                        actors[1].append(word)
                else:
                    actors[1].append(word)
        if relation is not None:
            relations.append((relation, actors))
    return relations


documents_dicts_tags = get_page_documents_dict_tags()[:20]
documents_templates = []
for document_dicts_tags in documents_dicts_tags:
    documents_templates.append({
        'author': get_author_names(document_dicts_tags['author']),
        'title': get_title(document_dicts_tags['title']),
        'subjects': get_subjects(document_dicts_tags['subjects']),
        'comments': get_comments(document_dicts_tags['comments']),
        'link': get_link(document_dicts_tags['link']),
        'relations': get_relations(document_dicts_tags['content']),
    })

print('wrapper result')
for index, document_template in enumerate(documents_templates):
    print(index)
    print('title: %s' % document_template['title'])
    print('\tauthor: %s' % document_template['author'])
    print('\tsubjects: %s' % document_template['subjects'])
    print('\tcomments: %s' % document_template['comments'])
    print('\tlink: %s' % document_template['link'])
    print('\trelations: (%d)' % len(document_template['relations']))
    for (relation, (actor1, actor2)) in document_template['relations']:
        print('%s (%s -> %s)' % (relation, ' '.join(actor1), ' '.join(actor2)))
    print()
