from data_base import DataBase

db = DataBase()

# Шаг 5
print(db.get_search_cast('Rose McIver', 'Ben Lamb'))
print(db.get_search_cast('Jack Black', 'Dustin Hoffman'))

# Шаг 6
print(db.get_title('Movie', 1980, 'Dramas'))
print(type(db.get_title('Movie', 1980, 'Dramas')))
