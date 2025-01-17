import dotenv
import json
import urllib.request as request

from google.api_core.exceptions import AlreadyExists, RetryError
from google.cloud import firestore

'''
OMDb  API (Open Movie Database) URL uses at least the following parameters:
* Search query: s
* API key: apikey
* Page number: page

We can use the search query parameter to search for movies with a specific title, or just look
for movies which a specific word in the title, since there is no endpoint to get all movies at once.

Example: https://www.omdbapi.com/?s=<query parameter>&apikey=<omdb api key>&page=<page number>
'''

search: str = dotenv.get_key('.env', 'OMDB_SEARCH')
apiKey: str = dotenv.get_key('.env', 'OMDB_API_KEY')
fsCollection: str = dotenv.get_key('.env', 'FIRESTORE_COLLECTION')

db: firestore.Client = firestore.Client()

def populate_db():
    for page in range(1, 11):
        queryUrl: str = f"https://www.omdbapi.com/?s={search}&apikey={apiKey}&page={page}"
        
        with request.urlopen(queryUrl) as response:
            response = response.read().decode('utf-8')
            response_json = json.loads(response)['Search']

            for movie in response_json:
                try:
                    print(f"Adding {movie['Title']} to the database")
                    doc_ref = db.collection(fsCollection).document(movie['imdbID'])
                    doc_ref.create(movie)
                except AlreadyExists:
                    print(f"Error: {movie['Title']} already exists in the database. Skipping...")
                except RetryError as re:
                    print(f"Failed to add {movie['Title']} to the database. Original error was: {re.with_traceback()}")

'''
Check if database is already populated. If it is, this script won't do anything.
'''
def check_db():
    db_count = db.collection(fsCollection).count().get()[0][0].value 
    return db_count == 0

if check_db():
    print("Database already populated. No need to add new data.")
else:
    print("Database is empty! Populating...")

    populate_db()
    print("Database populated")
