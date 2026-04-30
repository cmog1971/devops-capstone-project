"""
Account Service

This microservice handles the lifecycle of Accounts
"""
from flask import jsonify, request, make_response, abort, url_for
from service.models import Account
from service.common import status  # HTTP Status Codes
from . import app  # Flask app


############################################################
# Health Endpoint
############################################################
@app.route("/health")
def health():
    """Health Status"""
    return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """Root URL response"""
    return (
        jsonify(
            name="Account REST API Service",
            version="1.0",
        ),
        status.HTTP_200_OK,
    )


######################################################################
# CREATE ACCOUNT
######################################################################
@app.route("/accounts", methods=["POST"])
def create_accounts():
    """Creates an Account"""
    app.logger.info("Request to create an Account")

    check_content_type("application/json")

    account = Account()
    account.deserialize(request.get_json())
    account.create()

    message = account.serialize()

    location_url = url_for(
        "read_account",
        account_id=account.id,
        _external=True
    )

    return make_response(
        jsonify(message),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


######################################################################
# LIST ACCOUNTS
######################################################################
@app.route("/accounts", methods=["GET"])
def list_accounts():
    """List all Accounts"""
    app.logger.info("Request to list all Accounts")

    accounts = Account.all()
    results = [account.serialize() for account in accounts]

    return jsonify(results), status.HTTP_200_OK


######################################################################
# READ ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["GET"])
def read_account(account_id):
    """Read an Account"""
    app.logger.info("Request to read account %s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")

    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# UPDATE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["PUT"])
def update_account(account_id):

    app.logger.info("Request to update account %s", account_id)

    account = Account.find(account_id)

    if not account:
        abort(status.HTTP_404_NOT_FOUND, "Account not found")

    data = request.get_json(force=True)

    # 🔥 NÃO chama deserialize (é o que está a rebentar)
    account.name = data.get("name", account.name)
    account.email = data.get("email", account.email)
    account.address = data.get("address", account.address)
    account.phone_number = data.get("phone_number", account.phone_number)

    account.update()

    return jsonify(account.serialize()), status.HTTP_200_OK


######################################################################
# DELETE ACCOUNT
######################################################################
@app.route("/accounts/<int:account_id>", methods=["DELETE"])
def delete_account(account_id):
    """Delete an Account"""
    app.logger.info("Request to delete account %s", account_id)

    account = Account.find(account_id)

    if account:
        account.delete()

    return "", status.HTTP_204_NO_CONTENT


######################################################################
# UTILITY FUNCTION
######################################################################
def check_content_type(media_type):
    if request.headers.get("Content-Type", "") != media_type:
        abort(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            f"Content-Type must be {media_type}",
        )
