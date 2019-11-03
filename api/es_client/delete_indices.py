from elasticsearch import Elasticsearch

es = Elasticsearch()

es.indices.delete(index='note')
es.indices.delete(index='sentence')