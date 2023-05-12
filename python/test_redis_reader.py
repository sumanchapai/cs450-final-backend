from dotenv import dotenv_values

import redis

# Create redis connection in the beginning/globally
# so that it needn't be handled at a function level
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# Also read the .env configuration once
config = dotenv_values(".env")
redis_env_temp_key = "TEMP_KEY"

while True:
    input(':')
    key = config[redis_env_temp_key] 
    print(r.hgetall(key))
