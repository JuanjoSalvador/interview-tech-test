[![Python application](https://github.com/JuanjoSalvador/interview-tech-test/actions/workflows/python-app.yml/badge.svg)](https://github.com/JuanjoSalvador/interview-tech-test/actions/workflows/python-app.yml)

# Movies API

Python API RESTful built on top of WSGI and Firebase. No frameworks used.

* Firestore
* Firebase Authentication
* Gunicorn

## Deployment

### Live versions

Live version (Google App Engine and Google Cloud Run) availables here:

* [API REST](https://test-movie-api.ew.r.appspot.com/api/v1/movies/)
* [Alpha] [Cloud Functions](https://europe-west2-test-movie-api.cloudfunctions.net/movies-view)

### REST Endpoints

* `GET /api/v1/movies/` - Returns all movies
* `GET /api/v1/movies/{imdbID}/` - Returns movie with specified ID
* `POST /api/v1/movies/` - Creates a new movie into database
* `DELETE /api/v1/movies/{imdbID}/` - Deletes movie with specified ID

### Cloud endpoints

* `GET /` - Returns all movies
* `GET /{imdbID}` - Returns movie with specified ID
* `POST /` - Creates a new movie into database
* `DELETE /{imdbID}` - Deletes movie with specified ID


