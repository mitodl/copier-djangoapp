import dj_database_url
from mitol.common.envs import get_string, get_int, get_bool

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases
DEFAULT_DATABASE_CONFIG = dj_database_url.parse(
    get_string(
        name="DATABASE_URL",
        description="The connection url to the Postgres database",
        required=True,
        write_app_json=False,
    )
)
DEFAULT_DATABASE_CONFIG["CONN_MAX_AGE"] = get_int(
    name="DATABASE_CONN_MAX_AGE",
    default=0,
    description="Maximum age of connection to Postgres in seconds",
)
# If True, disables server-side database cursors to prevent invalid cursor errors when using pgbouncer
DEFAULT_DATABASE_CONFIG["DISABLE_SERVER_SIDE_CURSORS"] = get_bool(
    name="DATABASE_DISABLE_SERVER_SIDE_CURSORS",
    default=True,
    description="Disables Postgres server side cursors",
)

if get_bool(
    name="DB_DISABLE_SSL",
    default=False,
    description="Disables SSL to postgres if set to True",
):
    DEFAULT_DATABASE_CONFIG["OPTIONS"] = {}
else:
    DEFAULT_DATABASE_CONFIG["OPTIONS"] = {"sslmode": "require"}

DATABASES = {
    "default": DEFAULT_DATABASE_CONFIG,
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"