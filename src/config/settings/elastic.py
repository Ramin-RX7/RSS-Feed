import elasticsearch

from .base import BASE_ENV


__all__ = ("ES_CONNECTION",)


ES_CONNECTION = elasticsearch.Elasticsearch(BASE_ENV("ELASTIC_URL"))
