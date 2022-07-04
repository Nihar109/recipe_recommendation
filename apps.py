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
        result = sr.recommends(recipe_name)
    except Exception as e:
        recipe_name = None
        result = None

    return render_template('input.html', recipe_name=recipe_name, result=result)


if __name__ == '__main__':
    app.run(debug=True)
