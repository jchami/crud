from datetime import datetime, timedelta
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import User, ActivationRequest


JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=60)


class Login(Resource):
    def post(self):
        """Route behavior for user authentication."""

        if not request.is_json:
            return {"message": "Missing data."}, 400

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        if not email:
            return {"message": "Missing required email data."}, 400
        if not password:
            return {"message": "Missing required password data."}, 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.password_is_valid(password):
            return {"message": "Incorrect user or password."}, 401

        access_token = user.generate_token(JWT_ACCESS_TOKEN_EXPIRES)
        return {"token": access_token,
                "userEmail": user.email,
                "tokenExpiresIn": JWT_ACCESS_TOKEN_EXPIRES.total_seconds()}, 200


class ActivationRequests(Resource):
    @jwt_required
    def get(self):
        """Route behavior for the retrieval of a single activation request."""
        
        activation_request_id = request.args.get('request_id', None)
        if not activation_request_id:
            return {"message": "Missing required ID parameter."}, 400

        activation_request = ActivationRequest.query.filter_by(id=activation_request_id).first()
        if not activation_request:
            return {'message': 'No activation request found for informed parameters.'}, 404

        return {
            'id': activation_request_id,
            'user': activation_request.user_id,
            'company_name': activation_request.company_name,
            'request_status': activation_request.approved
        }, 200


    @jwt_required
    def post(self):
        """Route behavior for the creation of a new activation request."""

        if not request.is_json:
            return {"message": "Missing data."}, 400

        company_name = request.json.get('company_name', None)
        if not company_name:
            return {"message": "Missing required company data."}, 400

        active_user = get_jwt_identity()

        activation_request = ActivationRequest.query.filter_by(user_id=active_user['id'], company_name=company_name).first()
        if activation_request:
            return {'message': 'Activation request already exists'}, 400
        activation_request = ActivationRequest(user_id=active_user['id'], company_name=company_name)
        try:
            activation_request.save()
        except Exception as e:
            return {'message': 'Failed to create activation request'}, 500

        return {
            'id': activation_request.id,
            'user': activation_request.user_id,
            'company_name': company_name,
            'request_status': activation_request.approved
        }, 200

    @jwt_required
    def put(self):
        """Route behavior for the approval/refusal of an existing activation request."""

        if not request.is_json:
            return {"message": "Missing data."}, 400

        activation_request_id = request.json.get('request_id', None)
        if not activation_request_id:
            return {"message": "Missing required ID data."}, 400
        approved = request.json.get('approved', None)
        if approved == None:
            return {"message": "Missing required approval data."}, 400

        activation_request = ActivationRequest.query.filter_by(id=activation_request_id).first()
        if not activation_request:
            return {'message': 'No activation request found for informed data.'}, 404

        activation_request.approved = approved
        try:
            activation_request.save()
        except Exception as e:
            return {'message': 'Failed to update activation request approval status.'}, 500

        return {
            'id': activation_request_id,
            'user': activation_request.user_id,
            'company_name': activation_request.company_name,
            'request_status': approved
        }, 200

    @jwt_required
    def delete(self):
        """Route behavior for the cancellation of an existing activation request."""

        if not request.is_json:
            return {"message": "Missing data."}, 400

        activation_request_id = request.json.get('request_id', None)
        if not activation_request_id:
            return {"message": "Missing required ID data."}, 400

        activation_request = ActivationRequest.query.filter_by(id=activation_request_id).first()
        if not activation_request:
            return {'message': 'No activation request found for informed data.'}, 404

        user_id = activation_request.user_id
        company_name = activation_request.company_name

        try:
            activation_request.delete()
        except Exception as e:
            return {'message': 'Failed to cancel activation request'}, 500

        return {
            'id': activation_request_id,
            'user': activation_request.user_id,
            'company_name': activation_request.company_name
        }, 200
