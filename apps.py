from flask import Flask, render_template, request
import search_recommendation as sr

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('input.html')


# real time api
@app.route('/recommend', methods=['POST'])
def recommend():
    """Whenever API is called, It will take user input search the recipe name
       using Elasticsearch and recommend Similar product."""

    user_input = str(request.form.get('recipename'))
    try:
        recipe_name = sr.convert_elasticquery(user_input)
        query = "Similar product for {} are:".format(recipe_name)
        result = sr.recommends(recipe_name)
    except Exception as e:
        query = "No recipe name found on this keyword"
        result = ""

    return render_template('input.html', query=query, result=result)


if __name__ == '__main__':
    app.run(debug=True)
