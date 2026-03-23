# Translation and Localization Guide

This project follows standard Django internationalization (i18n) and localization (l10n) practices.

## Overview
- **Middlewares**: `LocaleMiddleware` is enabled to detect the user's language from the `Accept-Language` header.
- **Translatable Strings**: All user-facing strings in models, serializers, and views are wrapped with `gettext_lazy` (as `_`) or `gettext`.
- **Database Content**: Model fields like `Category.name` are translated dynamically in serializers using `gettext` to allow for scalable multi-language support without hardcoded fields (e.g., `name_ar` is deprecated). This is achieved by using a `SerializerMethodField` in the serializer.

## Workflow for Adding Translations

1.  **Mark Strings for Translation**:
    In Python files, use `django.utils.translation.gettext_lazy` for models/serializers and `gettext` for dynamic content.
    ```python
    from django.utils.translation import gettext_lazy as _
    name = models.CharField(_("name"), max_length=255)
    ```

2.  **Extract Messages**:
    Run the following command to create or update the `.po` files:
    ```bash
    python manage.py makemessages -l ar
    ```
    *Note: This requires GNU gettext tools installed on your system.*

3.  **Provide Translations**:
    Edit the `.po` file located at `src/nu_quran_api/locale/<lang>/LC_MESSAGES/django.po`.
    ```po
    msgid "Attending thought session"
    msgstr "حضور جلسة الخاطرة"
    ```

4.  **Compile Messages**:
    Run the following command to generate the `.mo` files used by Django at runtime:
    ```bash
    python manage.py compilemessages
    ```

## Adding a New Language

1.  **Update Settings**:
    Add the language code to `LANGUAGES` in `src/nu_quran_api/settings/base.py`:
    ```python
    LANGUAGES = [
        ("en", "English"),
        ("ar", "Arabic"),
        ("fr", "French"),  # Example
    ]
    ```

2.  **Generate PO File**:
    ```bash
    python manage.py makemessages -l fr
    ```

3.  **Translate and Compile**:
    Follow the workflow steps 3 and 4 above.

## Testing Translations
Use the `Accept-Language` header in your requests:
- `Accept-Language: ar` for Arabic
- `Accept-Language: en` for English

Example Test Case:
```python
def test_arabic_response(client):
    response = client.get("/api/v1/...", HTTP_ACCEPT_LANGUAGE="ar")
    assert "..." in response.data["..."]
```
