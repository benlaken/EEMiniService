from flask import Flask
from flask_restplus import Api, Resource, fields
import sys
import os
import ee

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)
print("Starting Flask Microservice. Running on ", sys.platform)
if sys.platform == 'darwin':
    # If using a local mac, assume you can initilise using the below
    ee.Initialize()
else:
    # assume you have an EE_private_key env. variable with authorisation
    service_account = os.environ['EE_USER']
    print(service_account)
    credentials = ee.ServiceAccountCredentials(service_account,BASE_DIR +'/privatekey.pem')
    ee.Initialize(credentials, 'https://earthengine.googleapis.com')

app = Flask(__name__)
api = Api(app, version='1.0', title='Minimum API example',
    description='A simple start point to build a microservice in flask, using '\
    'Earth Engine, with automatic Swagger UI',)

ns = api.namespace('Endpoints',
                   description='Operations and supporting information')

todo = api.model('Todo', {
    'id': fields.Integer(readOnly=True, description='The task unique identifier'),
    'task': fields.String(required=True, description='The task details')})


class TodoDAO(object):
    def __init__(self):
        self.counter = 0
        self.todos = []

    def get(self, id):
        for todo in self.todos:
            if todo['id'] == id:
                return todo
        api.abort(404, "Todo {} doesn't exist".format(id))

    def create(self, data):
        todo = data
        todo['id'] = self.counter = self.counter + 1
        self.todos.append(todo)
        return todo

    def update(self, id, data):
        todo = self.get(id)
        todo.update(data)
        return todo

    def delete(self, id):
        todo = self.get(id)
        self.todos.remove(todo)


# Create an instance of the object which uses app methods
DAO = TodoDAO()
DAO.create({'task': 'Build an API'})
DAO.create({'task': 'Workin in the Code mine'})
DAO.create({'task': 'Connect API to EE for fun'})


@ns.route('/')
class TodoList(Resource):
    '''Shows a list of all todos, and lets you POST to add new tasks'''
    @ns.doc('list_todos')
    @ns.marshal_list_with(todo)
    def get(self):
        '''List all tasks'''
        return DAO.todos

    @ns.doc('create_todo')
    @ns.expect(todo)
    @ns.marshal_with(todo, code=201)
    def post(self):
        '''Create a new task'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'Todo not found')
@ns.param('id', 'The task identifier')
class Todo(Resource):
    '''Show a single todo item and lets you delete them'''
    @ns.doc('get_todo')
    @ns.marshal_with(todo)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)

    @ns.doc('delete_todo')
    @ns.response(204, 'Todo deleted')
    def delete(self, id):
        '''Delete a task given its identifier'''
        DAO.delete(id)
        return '', 204

    @ns.expect(todo)
    @ns.marshal_with(todo)
    def put(self, id):
        '''Update a task given its identifier'''
        return DAO.update(id, api.payload)


if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=int(os.getenv('PORT')), debug=True)
