from datetime import datetime
from dotenv import dotenv_values

import logging
import pytz
import redis
import serial
import sys


TIMEZONE = pytz.timezone('US/Central')

# Make the key application/specific so other apps won't modify
TEMP_KEY = "temp-cs-450"

# Create redis connection in the beginning/globally
# so that it needn't be handled at a function level
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# Also read the .env configuration once
config = dotenv_values("../.env")
redis_env_temp_key = "TEMP_KEY"



def get_data_to_save(temp : float):
    """"
    Returns the dictionary representing the data to be  
    saved to the Redis database
    """
    current_time = datetime.now(tz=TIMEZONE).timestamp()
    return { "time": current_time, "temperature": temp}



def handle_input(line : str):
    """
    Parses the input and if it is a valid float 
    write it to the Redis database as the new value
    of the temperature along with the current timestamp
    """
    if type(line) != str:
        return
    try:
        temp = float(line)
        data = get_data_to_save(temp)
        key = config[redis_env_temp_key]
        r.hset(key, mapping=data) # Save data to redis
        logging.info(f"Setting {data} to redis")
    except Exception as e:
        if not line.replace(".", "").isnumeric():
            logging.warning(f"Got non numberic temp value. {line}")
        logging.error(f"Encountered exception {e}")
        



def main():
    """
    Read the input from the ardunio serial monitor and
    call `handle_data` with the input
    """
    
    # Setup logger
    logging.basicConfig(filename='log_temp_input.log', level=logging.DEBUG, format='%(asctime)s %(message)s')
    # Add logging to std out as well
    # logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


    try:
        ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    except serial.serialutil.SerialException as e:
        # TODO
        # Handle exception
        raise e
          

    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8').rstrip()
            except:
                logging.warning(f"Could not parse input from serial monitor. Got {line}")
                continue
            else:
                handle_input(line)


if __name__ == "__main__" :
    main()
