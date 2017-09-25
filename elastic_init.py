from elasticsearch import Elasticsearch
import json
import logging

log = logging.getLogger('elastic_log')

client = Elasticsearch('127.0.0.1')

mapping = {
    'mappings': {
        'talk': {
            'properties': {
                'id': {'type': 'string', 'index': 'not_analyzed'},
                'title': {'type': 'string', 'analyzer': 'english'},
                'job': {'type': 'string'},
                'speaker': {'type': 'string'},
                'description': {'type': 'string', 'analyzer': 'english'},
                'language': {'type': 'string', 'index': 'not_analyzed'},
                'level': {'type': 'string', 'analyzer': 'english'},
            }
        }
    }
}

client.indices.delete(index='codemotion')
client.indices.create(index='codemotion', body=mapping)

n = 1

with open('codemotion_info.json', 'r') as my_file:
    a = json.load(my_file)
    for doc in a['speaker_list']:
        log.info('Modify {}'.format(doc['title']))
        doc['id'] = str(n)
        log.info('Adding {} with id {}'.format(doc['title'], doc['id']))
        client.create(index='codemotion', doc_type='talk', id=n, body=doc)
        n += 1


