from decouple import config

TOMTOM_API_KEY = config('TOMTOM_API_KEY')
OPENWEATHER_API_KEY = config('OPENWEATHER_API_KEY')

DIR_REAL_TIME_DATA = config('DIR_REAL_TIME_DATA')

#DATABASE_HOST = config('DATABASE_HOST')
#DATABASE_USER = config('DATABASE_USER')
#DATABASE_PASSWORD = config('DATABASE_PASSWORD')


MLFLOW_PROJECT = config('MLFLOW_PROJECT')