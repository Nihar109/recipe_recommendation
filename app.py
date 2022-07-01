import numpy as np
import pandas as pd
import pickle
from flask import Flask, render_template, request
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

recipe_data = pd.read_csv('recipe_data.csv')
similarity = pickle.load(open('similarity.pkl', 'rb'))


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
    return render_template('index.html',
                           recipename=list(recipe_data['recipe_name'].values))


@app.route('/recommend', methods=['POST'])
def recommend():
    recipe_name = str(request.form.get('recipename'))
    query = "Similar product for {} are:".format(recipe_name)
    try:
        result = recommends(recipe_name)
    except Exception as e:
        result = "Recommendation is not available for this search"
    return render_template('index.html', query=query, result=result)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5020)
