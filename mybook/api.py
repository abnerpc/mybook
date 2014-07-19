# coding: utf-8

import json
import requests
from flask import Blueprint, request, current_app
from mybookapp import people

api_blueprint = Blueprint('api', __name__)
GRAPH_API = "https://graph.facebook.com/%s"


@api_blueprint.route("/person/", methods=["POST"])
def post_person():
    facebookId = request.values.get('facebookId')
    if not facebookId:
        current_app.logger.error('post_person without facebookId')
        return 'parameter *facebookId* not found', 400
    r = requests.get(GRAPH_API % facebookId)
    if not r.ok:
        current_app.logger.error('post_person with invalid facebookId')
        return 'facebookId invalid', 403
    person = people.find_one(username=facebookId)
    if not person:
        person = people.find_one(facebookId=facebookId)
    if person:
        current_app.logger.error('post_person with existent facebookId')
        return 'facebookId exists', 403
    _data = r.json()
    new_person = {}
    new_person['username'] = _data.get('username')
    new_person['facebookId'] = _data.get('id')
    new_person['name'] = _data.get('name')
    new_person['gender'] = _data.get('gender')
    people.insert(new_person)
    current_app.logger.info('success post_person request')
    return '', 201


@api_blueprint.route("/person/", methods=["GET"])
def get_people():
    _limit = request.args.get('limit')
    if _limit:
        try:
            _limit = int(_limit)
        except:
            current_app.logger.error('bad get_people request')
            return '', 404
    result = [row for row in people.find(_limit=_limit)]
    result.append({"count": len(list(people.all()))})
    current_app.logger.info('success get_people request')
    return json.dumps(result), 200


@api_blueprint.route("/person/<facebookId>", methods=["DELETE"])
def delete_person(facebookId):
    deleted = people.delete(username=facebookId)
    if not deleted:
        deleted = people.delete(facebookId=facebookId)
    if not deleted:
        current_app.logger.info('delete_person with not-existent facebookId')
        return 'facebookId not found', 403
    current_app.logger.info('success delete_person request')
    return 'facebookId deleted', 204
