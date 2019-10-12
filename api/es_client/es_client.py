from elasticsearch import Elasticsearch

es = Elasticsearch()
print(es.search(index='note'))
print(es.search(index='sentence'))