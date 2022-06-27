from flask import Flask, jsonify

from data_base import DataBase

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["JSON_SORT_KEYS"] = False
db = DataBase()


@app.route("/")
def main_page():
    return "Hello World"


@app.route("/movie/<title>/")
def title_page(title):
    try:
        search_title = db.get_search_title(title)
    except:
        return "NotFound"
    return jsonify(search_title)


@app.route("/movie/<int:year1>/to/<int:year2>/")
def years_page(year1, year2):
    try:
        search_years = db.get_search_years(year1, year2)
    except:
        return "NotFound"
    return jsonify(search_years)


@app.route("/rating/<rating>/")
def rating_page(rating):
    try:
        search_rating = db.get_search_rating(rating)
    except:
        return "NotFound"
    return jsonify(search_rating)


@app.route("/genre/<genre>/")
def genre_page(genre):
    try:
        search_rating = db.get_search_genre(genre)
    except:
        return "NotFound"
    return jsonify(search_rating)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
