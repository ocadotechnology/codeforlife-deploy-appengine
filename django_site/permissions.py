import logging
import os

from google.auth.transport import requests
from google.oauth2 import id_token

LOGGER = logging.getLogger(__name__)

CLOUD_SCHEDULER_SERVICE_ACCOUNT_NAME = (
    "cloud-scheduler@decent-digit-629.iam.gserviceaccount.com"
)
INACTIVE_USERS_AUDIENCE = f"https://{os.getenv('GAE_SERVICE')}-dot-{os.getenv('GOOGLE_CLOUD_PROJECT')}.appspot.com/users/inactive/"
INDY_CLEANUP_AUDIENCE = f"https://{os.getenv('GAE_SERVICE')}-dot-{os.getenv('GOOGLE_CLOUD_PROJECT')}.appspot.com/indycleanup/"

GOOGLE_ISSUER = "https://accounts.google.com"

# help
def is_cloud_scheduler(request):
    verify_request = requests.Request()
    auth_header = request.META.get("HTTP_AUTHORIZATION")
    if auth_header is None:
        # Cloud Scheduler uses authorization headers
        return False

    # auth_header is in the form of `Authorization: Bearer` token
    bearer, token = auth_header.split()
    if bearer.lower() != "bearer":
        LOGGER.warning(
            f"Authorization header is not of format `Authorization: Bearer` but: {auth_header}"
        )
        return False

    uri = request.build_absolute_uri()
    if uri.endswith("/indycleanup/"):
        audience = INDY_CLEANUP_AUDIENCE
    else:
        audience = INACTIVE_USERS_AUDIENCE

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            verify_request,
            audience,
        )
        is_correct_issuer = id_info["iss"] == GOOGLE_ISSUER
        is_cloud_scheduler_service_account = (
            id_info["email"] == CLOUD_SCHEDULER_SERVICE_ACCOUNT_NAME
        )
        return (
            is_correct_issuer
            and is_cloud_scheduler_service_account
            and id_info["email_verified"]
        )
    except Exception as e:
        LOGGER.warning(
            "Couldn't verify and authorize cloud scheduler request", exc_info=e
        )
        return False
