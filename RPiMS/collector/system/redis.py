import logging
import sys
import redis

logger = logging.getLogger(__name__)

def db_connect(dbhost, dbnum):
    try:
        redis_db = redis.StrictRedis(host=dbhost, port=6379, db=str(dbnum), decode_responses=True)
        redis_db.ping()
        return redis_db
    except Exception as err:
        logger.error(err)
        logger.error("Can't connect to RedisDB host: %s", dbhost)
        sys.exit(255)
