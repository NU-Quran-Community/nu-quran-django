from django.utils import translation
from django.utils.translation import gettext as _
from rest_framework.views import exception_handler


def translate_errors(data):
    if isinstance(data, dict):
        return {key: translate_errors(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [translate_errors(item) for item in data]
    elif isinstance(data, str):
        return _(data)
    return data


def custom_exception_handler(exc, context):
    # Activate language from the incoming request
    request = context.get("request")
    if request is not None:
        lang = translation.get_language_from_request(request)
        translation.activate(lang)

    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return response

    # Custom translation for Django ORM 404: "No <Model> matches the given query."
    detail = response.data.get("detail", "")
    if isinstance(detail, str) and detail.startswith("No ") and "matches the given query" in detail:
        model_name = detail.split(" ")[1]
        response.data["detail"] = _(
            "No %(name)s matches the given query."
        ) % {"name": _(model_name)}
        return response

    # Recursively translate all other error strings in the response
    response.data = translate_errors(response.data)

    return response
