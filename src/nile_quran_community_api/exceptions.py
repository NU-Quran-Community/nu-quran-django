from django.utils import translation
from rest_framework.views import exception_handler

from nile_quran_community_api.i18n import DynamicErrorTranslator

DYNAMIC_TRANSLATOR: DynamicErrorTranslator = DynamicErrorTranslator()


def translate_errors(data):
    if isinstance(data, dict):
        return {key: translate_errors(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [translate_errors(item) for item in data]
    elif isinstance(data, str):
        return DYNAMIC_TRANSLATOR.translate(data)
    return data


def custom_exception_handler(exc, context):
    """Custom DRF exception handler to translate error messages in response using Django primitives."""

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

    # Recursively translate all other error strings in the response
    response.data = translate_errors(response.data)

    return response
