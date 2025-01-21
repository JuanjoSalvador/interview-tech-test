import firebase_admin
from firebase_admin import firestore

from app import settings

def initialize_firebase(): # pragma: no cover
    """Inicializa Firebase y devuelve el cliente Firestore."""
    firebase_app = firebase_admin.initialize_app(name=settings.APP_NAME)
    db = firestore.client(app=firebase_app)
    
    return db, firebase_app

db, firebase_app = initialize_firebase()