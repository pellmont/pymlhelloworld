from flask_restplus import Resource, Namespace


api = Namespace('healthcheck', description='Healthcheck operation')


@api.route('/healthcheck')
class Health(Resource):
    def get(self):
        print("Healthcheck called!")
