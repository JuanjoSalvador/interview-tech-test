import json

from api.exceptions import (DocumentDoesNotExist, NotAuthorizedException,
                            ValidationError)
from api.views import ModelView
from app.movies.services import MovieService


class MoviesView(ModelView):
    def get(self, req, resp, **kwargs):
        params = req.GET
        page = params.get('page', 1)
        page_size = params.get('page_size', 10)
        search = params.get('search', None)

        page, page_size = int(page), int(page_size)

        movie_id: str | None = kwargs.get('movie_id', None)
        try:
            data = (
                MovieService.get(movie_id) 
                if movie_id 
                else MovieService.all(
                    page=page, 
                    page_size=page_size,
                    search=search
                )
            )

            resp.json = data

        except DocumentDoesNotExist:
            resp.status_code = 404

        except (ValueError, TypeError): # pragma: no cover
            resp.status_code = 500
                  
        return resp

    def post(self, req, resp, **kwargs):
        try:
            data = json.loads(req.body)
            response = MovieService.create(data)

        except ValidationError:
            resp.status_code = 400
            response = {
                "error": 400, 
                "message": "Missing required fields. Make sure 'imdbID', 'Title', 'Type' and 'Year' are defined."
            }

        except json.decoder.JSONDecodeError: # pragma: no cover
            resp.status_code = 400
            response = {
                "error": 400, 
                "message": "Wrong JSON format."
            }
        
        finally:
            resp.json = response

        return resp
    
    #@permissions([IsAuthenticated, IsStaff])
    def delete(self, req, resp, **kwargs):
        try:
            if req.authorization is None:
                raise NotAuthorizedException

            movie_id: str | None = kwargs.get('movie_id', None)
            auth_token = req.authorization.params

            MovieService.delete(movie_id, auth_token)
            resp.status_code = 200

        except NotAuthorizedException:
            resp.status_code = 401

        except DocumentDoesNotExist as not_exist:
            resp.status_code = 400
            resp.json = {"error": { "message": not_exist.message } }
        
        return resp
    
    def put(self, *args, **kwargs):
        raise NotImplementedError
