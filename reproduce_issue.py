from app.services.post_service import PostService
from app.schemas.post_schema import PostCreate
import pytest
from bson.errors import InvalidId

def test_invalid_id():
    service = PostService()
    try:
        service.get_post_by_id("org_123", "invalid-id")
    except Exception as e:
        print(f"Caught exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    test_invalid_id()
