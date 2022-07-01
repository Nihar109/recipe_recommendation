try:
    import elasticsearch
    from elasticsearch import Elasticsearch
    from elasticsearch import helpers

    import numpy as np
    import pandas as pd
    import pickle
    from flask import Flask, render_template, request
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.metrics.pairwise import cosine_similarity

    print("Loaded ... ... ...")
except Exception as e:
    print("Some Modules are Missing{}".format(e))

app = Flask(__name__)

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


def recommends(recipe):
    """Creating recommendation function to
       recommend most five recipe_name from
       user input
    """
    recipe_index = recipe_data[recipe_data['recipe_name'] == recipe].index[0]
    recipe_list = sorted(list(enumerate(similarity[recipe_index])), reverse=True, key=lambda x: x[1])
    recommended_recipe_names = []

    for i in recipe_list[1:11]:
        recommended_recipe_names.append(recipe_data.iloc[i[0]].recipe_name)

    return recommended_recipe_names


@app.route('/')
def index():
    return render_template('input.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    user_input = str(request.form.get('recipename'))
    try:
        recipe_name = convert_elasticquery(user_input)
        query = "Similar product for {} are:".format(recipe_name)
        result = recommends(recipe_name)
    except Exception as e:
        result = ""
        query = "No recipe name found on this keyword"

    return render_template('input.html', query=query, result=result)


if __name__ == '__main__':
    app.run(debug=True)
