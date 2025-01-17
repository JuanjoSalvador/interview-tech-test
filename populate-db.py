import dotenv
import json
import urllib.request as request

'''
OMDb  API (Open Movie Database) URL uses at least the following parameters:
* Search query: s
* API key: apikey
* Page number: page

We can use the search query parameter to search for movies with a specific title, or just look
for movies which a specific word in the title, since there is no endpoint to get all movies at once.

Example: https://www.omdbapi.com/?s=<query parameter>&apikey=<omdb api key>&page=<page number>
'''

def populate_db():
    search: str = "star"
    apiKey: str = dotenv.get_key('.env', 'OMDB_API_KEY')

    for page in range(1, 11):
        queryUrl: str = f"https://www.omdbapi.com/?s={search}&apikey={apiKey}&page={page}"
        with request.urlopen(queryUrl) as response:
            response = response.read().decode('utf-8')
            response_json = json.loads(response['Search'])

            # TODO: Replace this with a database insert into GCP Datastore
            # Check this link for more info https://medium.com/@ilanyashuk/firestore-database-cheat-sheet-python-dcd54de02a4d

def check_db():
    return True

if check_db():
    print("Database already populated")
else:
    populate_db()
    print("Database populated")
