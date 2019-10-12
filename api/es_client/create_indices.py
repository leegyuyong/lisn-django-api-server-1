from elasticsearch import Elasticsearch

es = Elasticsearch()

es.indices.create(
    index='note',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "korean_nori": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "note_datas": {
                "properties": {
                    "note_id": {
                        "type": "long"
                    },
                    "user_id": {
                        "type": "long"
                    },
                    "title": {
                        "type": "text",
                        "analyzer": "korean_nori"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "korean_nori"
                    }
                }
            }
        }
    }
)

es.indices.create(
    index='sentence',
    body={
        "settings": {
            "index": {
                "analysis": {
                    "analyzer": {
                        "korean_nori": {
                            "type": "custom",
                            "tokenizer": "nori_tokenizer"
                        }
                    }
                }
            }
        },
        "mappings": {
            "sentence_datas": {
                "properties": {
                    "sentence_id": {
                        "type": "long"
                    },
                    "note_id": {
                        "type": "long"
                    },
                    "content": {
                        "type": "text",
                        "analyzer": "korean_nori"
                    }
                }
            }
        }
    }
)