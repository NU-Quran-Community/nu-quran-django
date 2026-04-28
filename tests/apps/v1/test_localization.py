import pytest
from rest_framework import status

@pytest.mark.django_db
def test_arabic_localization_no_user_found(api_client):
    # Set Accept-Language header to Arabic
    api_client.credentials(HTTP_ACCEPT_LANGUAGE='ar')
    
    # Try fetching a non-existent user
    response = api_client.get('/api/v1/users/99999/')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    # Should translation of "No User matches the given query." in Arabic
    assert 'تفاصيل' in response.data or 'detail' in response.data
    
    # Let's inspect the actual content of 'detail' if present
    detail = response.data.get('detail')
    assert 'يتم العثور' in detail or 'لم يتم العثور على المستخدم' in detail, f"Actual response was: {detail}"

@pytest.mark.django_db
def test_english_localization_default(api_client):
    # By default, English should be used when not specified or Accept-Language is 'en'
    api_client.credentials(HTTP_ACCEPT_LANGUAGE='en')
    
    # Try fetching a non-existent user
    response = api_client.get('/api/v1/users/99999/')
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    detail = response.data.get('detail')
    assert "No User matches the given query" in str(detail), f"Actual response was: {detail}"
