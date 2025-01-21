import dotenv

APP_NAME: str = "MoviesAPI"

FIRESTORE_COLLECTION: str = dotenv.get_key('.env', 'FIRESTORE_COLLECTION')
FIREBASE_WEB_API_KEY: str = dotenv.get_key('.env', 'FIREBASE_WEB_API_KEY')