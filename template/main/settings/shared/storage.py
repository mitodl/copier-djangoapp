from mitol.common.envs import get_string, get_bool

MEDIA_ROOT = get_string(
    name="MEDIA_ROOT",
    default="/var/media/",
    description="The root directory for locally stored media. Typically not used.",
)

MEDIA_URL = "/media/"

STORAGE_USE_S3 = get_bool(
    name="STORAGE_USE_S3",
    default=False,
    description="Use S3 for storage backend (required on Heroku)",
)

AWS_ACCESS_KEY_ID = get_string(
    name="AWS_ACCESS_KEY_ID", default=None, description="AWS Access Key for S3 storage."
)
AWS_SECRET_ACCESS_KEY = get_string(
    name="AWS_SECRET_ACCESS_KEY",
    default=None,
    description="AWS Secret Key for S3 storage.",
)
AWS_STORAGE_BUCKET_NAME = get_string(
    name="AWS_STORAGE_BUCKET_NAME", default=None, description="S3 Bucket name."
)
AWS_QUERYSTRING_AUTH = get_bool(
    name="AWS_QUERYSTRING_AUTH",
    default=False,
    description="Enables querystring auth for S3 urls",
)
AWS_S3_FILE_OVERWRITE = get_bool(
    name="AWS_S3_FILE_OVERWRITE",
    # Django Storages defaults this setting to True, but our desired default is False to avoid name collisions in
    # files uploaded in the CMS.
    default=False,
    description=(
        "Django Storages setting. By default files with the same name will overwrite each other. "
        "Set this to False to have extra characters appended."
    ),
)
# Provide nice validation of the configuration
if STORAGE_USE_S3 and (
    not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not AWS_STORAGE_BUCKET_NAME
):
    raise ImproperlyConfigured(
        "You have enabled S3 support, but are missing one of "
        "AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, or "
        "AWS_STORAGE_BUCKET_NAME"
    )
if STORAGE_USE_S3:
    if CLOUDFRONT_DIST:
        AWS_S3_CUSTOM_DOMAIN = "{dist}.cloudfront.net".format(dist=CLOUDFRONT_DIST)
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
