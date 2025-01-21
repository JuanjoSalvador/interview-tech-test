import math

from app import settings
from api.exceptions import (DocumentDoesNotExist, NotAuthorizedException,
                            ValidationError)
from api import services
from api.permissions import user_has_roles
from api.firebase_client import db

class MovieService(services.APIService):
    @staticmethod
    def all(page: int = 1, page_size: int = 10, search: str = None):
        # Check if page or page_size are invalid and reset to default values
        page = 1 if page == 0 else page
        page_size = 10 if page_size == 0 else page_size

        document_offset: int = (page - 1) * page_size
        base_query = db.collection(settings.FIRESTORE_COLLECTION)

        if not search:
            # Return all movies paginated by deafult
            query = (
                base_query
                .select(['Type', 'Title', 'Year', 'Poster', 'imdbID'])
                .order_by('Title')
                .offset(document_offset)
                .limit(page_size)
                .get()
            )
        else:
            query = (
                base_query
                .select(['Type', 'Title', 'Year', 'Poster', 'imdbID'])
                .where('Title_tokens', 'array_contains', search.lower())
                .order_by('Title')
                .offset(document_offset)
                .limit(page_size)
                .get()
            )

        results = [result.to_dict() for result in query] 
        total_data = len(results)
        num_of_pages = math.ceil(total_data / page_size) if total_data > 0 else 1
        is_last_page = page == num_of_pages 
        
        results = {
            "results": results ,
            "total": total_data,
            "num_of_pages": num_of_pages,
            "page": page,
            "next-page": f"?page={page + 1}&page_size={page_size}" if not is_last_page else f"?page={page}&page_size={page_size}",
            "last-page": f"?page={num_of_pages}&page_size={page_size}"
        }

        return results
    
    @staticmethod
    def get(movie_id):
        query = (
            db.collection(settings.FIRESTORE_COLLECTION)
                .document(movie_id)
                .get()
        )

        results = query.to_dict()        

        if not results:
            raise DocumentDoesNotExist
        
        return results

    @staticmethod
    def create(data):
        json_is_valid = MovieService.validate_post(data)
        if not json_is_valid:
            raise ValidationError
        
        db.collection(settings.FIRESTORE_COLLECTION).document(data['imdbID']).set(data)

        return data
    
    @classmethod
    def validate_post(cls, data: dict):
        '''
        Check if all required values are in data
        '''
        required_fields = ['imdbID', 'Type', 'Title', 'Year']
        return all([field in data.keys() for field in required_fields])
    
    @staticmethod
    def delete(movie_id, token):
        is_staff = user_has_roles(token, required_roles=['staff'])
        
        if not is_staff:
            raise NotAuthorizedException
        
        document_ref = (
            db.collection(settings.FIRESTORE_COLLECTION)
                .document(movie_id)
        )

        if document_ref.get().to_dict():
            document_ref.delete()

        else:
            raise DocumentDoesNotExist
