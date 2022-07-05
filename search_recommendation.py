import elasticsearch
from elasticsearch import Elasticsearch
import pandas as pd
import pickle

recipe_data = pd.read_csv('recipe_data.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))


def convert_elasticquery(text):
    """ Creating  function to take user input
        give output as similar recipe name using
        elastic search engine.
    """
    es = Elasticsearch(timeout=600, hosts="http://localhost:9200/")
    query = {
        "_source": ["recipe_name"]
        , "size": 1
        , "query": {
            "match": {
                "recipe_name": text
            }
        }
    }

    elastic_search = es.search(index='recipe', body=query)

    title = [x['_source'] for x in elastic_search['hits']['hits']]
    return title[0]['recipe_name']


def find_recipe_name(text):
    recipe_name_data = []
    for name in recipe_data['recipe_name']:
        if (text.lower() or text.capitlize() or text.upper()) in name:
            recipe_name_data.append(name)

    return recipe_name_data[0]


def recommends(recipe):
    """Creating recommendation function to
       recommend most five recipe_name from
       user input.
    """
    recipe_index = recipe_data[recipe_data['recipe_name'] == recipe].index[0]
    recipe_list = sorted(list(enumerate(similarity[recipe_index])), reverse=True, key=lambda x: x[1])
    recommended_recipe_names = []

    for i in recipe_list[1:11]:
        recommended_recipe_names.append(recipe_data.iloc[i[0]].recipe_name)

    return recommended_recipe_names
