import os
# from decouple import config
import logging
from csv import DictReader
from datetime import datetime
import psycopg2
from psycopg2.extras import LoggingConnection
from psycopg2 import OperationalError
from contextlib import closing

# file_csv = config('POSTGRES_DUMP_CSV')

class PostgreDB(object):
    """Класс для записи данных из дампа csv файла в PostgreDB
    _period - time_str
    _fld325 - car_numder
    _fld326 - longitude
    _fld327 - latitude
    _fld328 - speed
    _fld329 - direction (Азимут)
    _fld330 - valid (True/False)
    _fld331 - moving (True/False)
    _fld332 - actual (True/False)
    _fld333 - odometer
    _fld334 - alarmbutton (True/False)
    _fld335 - id_car
    """
    def __init__(self):
        self._host       = os.environ.get('POSTGRES_HOST')
        self._port       = os.environ.get('POSTGRES_PORT')
        self._user       = os.environ.get('POSTGRES_USER')
        self._password   = os.environ.get('POSTGRES_PASSWORD')
        self._dbname     = os.environ.get('POSTGRES_DBNAME')
        self._dbtable    = os.environ.get('POSTGRES_DBTABLE')
        self._timezone   = os.environ.get('POSTGRES_TIMEZONE')
        self._idregion  = os.environ.get('POSTGRES_IDREGION')
        self._dbconf     = dict()
        self._csv        = os.environ.get('POSTGRES_DUMP_CSV')
        if self._host and self._port and self._user and self._password and self._dbname:
            self._dbconf = {"user":     self._user,
                            "password": self._password,
                            "host":     self._host,
                            "port":     self._port,
                            "database": self._dbname,
                            }
        self.log         = logging
        self.log.basicConfig(level=logging.DEBUG,
                             format='%(asctime)s:%(levelname)s:%(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')

    def convertDataForPostgre(self, data: dict) -> list:
        """Метод для преобразования данных для отправки в Postgre"""
        time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        time_str = f'{data.pop("_period")}{self._timezone}'
        time_unix = datetime.strptime(time_str, f"%Y-%m-%d %H:%M:%S{self._timezone}").timestamp()
        if self._timezone.isalpha():
            timezone = 0
        else: 
            timezone = 3600 * int(self._timezone)
        time_unix -= timezone
        time_unix = round(time_unix)
        time_str = datetime.fromtimestamp(time_unix).strftime("%Y-%m-%d %H:%M:%SZ")
        car_numder = data.pop('_fld325')
        longitude = data.pop('_fld326')
        latitude = data.pop('_fld327')
        speed = round(float(data.pop('_fld328')))
        direction = data.pop('_fld329')
        if data.pop('_fld330') == 't':
            valid = True
        else:
            valid = False
        if data.pop('_fld331') == 't':
            moving = True
        else:
            moving = False
        if data.pop('_fld332') == 't':
            actual = True
        else:
            actual = False
        odometer = data.pop('_fld333')
        if data.pop('_fld334') == 't':
            alarmbutton = True
        else:
            alarmbutton = False
        id_car = data.pop('_fld335')
        altitude = 0
        id_region = self._idregion
        return [time, id_car, latitude, longitude, altitude, direction, speed, \
                odometer, id_region, car_numder, time_str, time_unix, valid, \
                actual, moving, alarmbutton]

    def insertData(self):
        """Метод для вставки данных в Postgre"""
        try:
            connect = psycopg2.connect(**self._dbconf)
            with closing(connect) as conn:
                with conn.cursor() as cursor:
                    conn.autocommit = True
                    with open(self._csv, 'r') as read_obj:
                        csv_dict_reader = DictReader(read_obj)
                        for row in csv_dict_reader:
                            time_str = f'{row.get("_period")}{self._timezone}'
                            id_car = row.get('_fld335')
                            self.log.info(f'[DUMP IMPORT] ReadRowCSV <= {time_str} | {id_car}')
                            cursor.execute('SELECT COUNT(*) FROM %s WHERE time_str = %s and id_car = %s', (self._dbtable, time_str, id_car,))
                            if not cursor.fetchone()[0]:
                                data = self.convertDataForPostgre(data=row)
                                self.log.info(f'[DUMP IMPORT] RowData => {data}')
                                cursor.execute("""INSERT INTO raw_data
                                                (time, id_car, latitude, longitude, altitude, direction, speed,
                                                odometer, id_region, car_numder, time_str, time_unix, valid,
                                                actual, moving, alarmbutton)
                                                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)
        except (OperationalError, TypeError, KeyboardInterrupt) as err:
            self.log.error(f'[DUMP IMPORT] insertData => {err}')


db = PostgreDB()

try:
    logging.info("[DUMP IMPORT] Start import CSV Dump")
    db.insertData()
except (KeyboardInterrupt, OSError) as err:
    logging.exception(f'[DUMP IMPORT] Unexpected exception {err}')
finally:
    logging.info("[DUMP IMPORT] Done import CSV Dump")
    