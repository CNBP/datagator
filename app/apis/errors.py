from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES


def error_response(status_code, message=None):
    """
    Generate the response using the status code given.
    :param status_code:
    :param message:
    :return:
    """
    # Craft payload error
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}

    # If customized message is provided, include it.
    if message:
        payload["message"] = message

    # JSONified the payload and update its status code to be returned.
    response = jsonify(payload)
    response.status_code = status_code

    return response


def bad_request(message):
    """
    Call to generate the payload.
    :param message:
    :return:
    """
    return error_response(400, message)
