import json
import sqlite3

DATA_PATH = "netflix.db"
name_table = "netflix"


class DataBase:
    def __init__(self, path=DATA_PATH, name=name_table):
        self.path = path
        self.name = name

    def create_cursor(self):
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            return cursor

    def get_search_title(self, title):
        cursor = self.create_cursor()
        cursor.execute(f"""
        SELECT title, country, release_year, listed_in, description
        FROM {self.name}
        WHERE title = '{title}'
        ORDER BY release_year DESC 
        """)
        data = cursor.fetchone()
        return dict(zip(("title", "country", "release_year", "genre", "description"), data))

    def get_search_years(self, year1, year2):
        cursor = self.create_cursor()
        cursor.execute(f"""
        SELECT title, release_year
        FROM {self.name}
        WHERE release_year BETWEEN {year1} AND {year2}
        ORDER BY release_year DESC 
        LIMIT 100
        """)
        data = cursor.fetchall()
        return [dict(zip(("title", "release_year"), d)) for d in data]

    def get_search_rating(self, rating):
        rating_dict = {
            "children": ("G", "G"),
            "family": ("G", "PG", "PG-13"),
            "adult": ("R", "NC-17")
        }
        cursor = self.create_cursor()
        cursor.execute(f"""
            SELECT title, rating, description
            FROM {self.name}
            WHERE rating in {rating_dict.get(rating)}
            ORDER BY release_year DESC 
            """)
        data = cursor.fetchall()
        return [dict(zip(("title", "rating", "description"), d)) for d in data]

    def get_search_genre(self, genre):
        cursor = self.create_cursor()
        cursor.execute(f"""
        SELECT title, description
        FROM {self.name}
        WHERE listed_in LIKE '%{genre}%'
        ORDER BY release_year DESC 
        """)
        data = cursor.fetchall()
        return [dict(zip(("title", "description"), d)) for d in data]

    def get_search_cast(self, name1, name2):
        cursor = self.create_cursor()
        cursor.execute(f"""
        SELECT "cast"
        FROM {self.name}
        WHERE "cast" LIKE '%{name1}%'
        AND "cast" LIKE '%{name2}%'
        ORDER BY release_year DESC 
        """)
        data = cursor.fetchall()
        casting_names = []
        for d in data:
            names = set(d[0].split(", ")) - {name1, name2}
            casting_names += list(names)
        return set(name for name in casting_names if casting_names.count(name) > 2)

    def get_title(self, type_title, year, genre):
        cursor = self.create_cursor()
        cursor.execute(f"""
        SELECT title, description
        FROM {self.name}
        WHERE "type" LIKE '%{type_title}%'
        AND release_year = {year}
        AND listed_in LIKE '%{genre}%'
        """)
        data = cursor.fetchall()
        return json.dumps([list(d) for d in data])
