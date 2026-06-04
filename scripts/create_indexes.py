from config.database import db 

db.movies.create_index("rating")
db.movies.create_index("language")
db.movies.create_index("release_date")
db.movies.create_index("rating")

print("indexes created")
