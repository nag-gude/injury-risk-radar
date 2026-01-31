import firebase_admin
from firebase_admin import credentials, firestore

from .config import settings

_app = None
_client = None


def get_client() -> firestore.Client:
    global _app, _client
    if _client is not None:
        return _client

    if not firebase_admin._apps:
        if settings.firestore_project:
            _app = firebase_admin.initialize_app(
                options={"projectId": settings.firestore_project}
            )
        else:
            # Uses GOOGLE_APPLICATION_CREDENTIALS or default credentials.
            cred = credentials.ApplicationDefault()
            _app = firebase_admin.initialize_app(cred)

    _client = firestore.client()
    return _client
