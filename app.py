from api import API

app = API()

@app.route('/')
def home(request, response):
    response.text = 'Hello World'

@app.route('/about')
def about(request, response):
    response.text = 'About Page'