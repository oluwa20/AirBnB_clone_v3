#!/usr/bin/python3
""" View for Amenity objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    all_amenities = storage.all(Amenity)
    return jsonify([amenity.to_dict() for amenity in all_amenities.values()])

@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """ Retrieves a Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>', methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """ Deletes an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Creates an Amenity object """
    new_amenity_data = request.get_json()
    if not new_amenity_data:
        abort(400, "Not a JSON")
    if "name" not in new_amenity_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**new_amenity_data)
    storage.new(new_amenity)
    storage.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    update_data = request.get_json()
    if not update_data:
        abort(400, "Not a JSON")

    for key, value in update_data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
