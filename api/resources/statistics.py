from flask_restful import Resource


class StatisticResource(Resource):
    def get(self, statistic_id):
        return [], 200

    def put(self, statistic_id):
        return [], 200

    def delete(self, statistic_id):
        return [], 200


class StatisticResourceList(Resource):
    def get(self):
        return [], 200

    def post(self):
        return [], 201
