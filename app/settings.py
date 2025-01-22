import dotenv
import os

ENVIRONMENT: str = os.environ.get("ENVIRONMENT", "development")
APP_NAME: str = "MoviesAPI"

FIRESTORE_COLLECTION: str = (
    dotenv.get_key(".env", "FIRESTORE_COLLECTION")
    if ENVIRONMENT == "development"
    else os.environ.get("FIRESTORE_COLLECTION", None)
)

FIREBASE_WEB_API_KEY: str = (
    dotenv.get_key(".env", "FIREBASE_WEB_API_KEY")
    if ENVIRONMENT == "development"
    else os.environ.get("FIREBASE_WEB_API_KEY", None)
)
