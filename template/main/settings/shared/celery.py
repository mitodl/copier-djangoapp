from mitol.common.envs import get_string, get_bool
from redbeat import RedBeatScheduler

# Redis
REDISCLOUD_URL = get_string(
    name="REDISCLOUD_URL", default=None, description="RedisCloud connection url"
)
if REDISCLOUD_URL is not None:
    _redis_url = REDISCLOUD_URL
else:
    _redis_url = get_string(
        name="REDIS_URL", default=None, description="Redis URL for non-production use"
    )

# Celery
USE_CELERY = True
CELERY_BROKER_URL = get_string(
    name="CELERY_BROKER_URL",
    default=_redis_url,
    description="Where celery should get tasks, default is Redis URL",
)
CELERY_RESULT_BACKEND = get_string(
    name="CELERY_RESULT_BACKEND",
    default=_redis_url,
    description="Where celery should put task results, default is Redis URL",
)
CELERY_BEAT_SCHEDULER = RedBeatScheduler
CELERY_REDBEAT_REDIS_URL = _redis_url
CELERY_TASK_ALWAYS_EAGER = get_bool(
    name="CELERY_TASK_ALWAYS_EAGER",
    default=False,
    dev_only=True,
    description="Enables eager execution of celery tasks, development only",
)
CELERY_TASK_EAGER_PROPAGATES = get_bool(
    name="CELERY_TASK_EAGER_PROPAGATES",
    default=True,
    description="Early executed tasks propagate exceptions",
)