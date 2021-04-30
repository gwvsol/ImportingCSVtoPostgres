import os
# from decouple import config
import logging
from csv import DictReader
from datetime import datetime
import psycopg2
# from psycopg2.extras import LoggingConnection
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
        self._host = os.environ.get('POSTGRES_HOST')
        self._port = os.environ.get('POSTGRES_PORT')
        self._user = os.environ.get('POSTGRES_USER')
        self._password = os.environ.get('POSTGRES_PASSWORD')
        self._dbname = os.environ.get('POSTGRES_DBNAME')
        # self._dbtable = os.environ.get('POSTGRES_DBTABLE')
        self._timezone = os.environ.get('POSTGRES_TIMEZONE')
        self._idregion = os.environ.get('POSTGRES_IDREGION')
        self._dbconf = dict()
        self._csv = os.environ.get('POSTGRES_DUMP_CSV')
        # ===================================================
        self.time_str = os.environ.get('TIME_STR')
        self.car_number = os.environ.get('CAR_NUMBER')
        self.longitude = os.environ.get('LONGITUDE')
        self.latitude = os.environ.get('LATITUDE')
        self.speed = os.environ.get('SPEED')
        self.direction = os.environ.get('DIRECTION')
        self.valid = os.environ.get('VALID')
        self.moving = os.environ.get('MOVING')
        self.actual = os.environ.get('ACTUAL')
        self.odometer = os.environ.get('ODOMETER')
        self.alarmbutton = os.environ.get('ALARMBUTTON')
        self.id_car = os.environ.get('ID_CAR')
        if self._host and self._port and \
           self._user and self._password and self._dbname:
            self._dbconf = {"user":     self._user,
                            "password": self._password,
                            "host":     self._host,
                            "port":     self._port,
                            "database": self._dbname,
                            }
        self.log = logging
        self.log.basicConfig(level=logging.DEBUG,
                             format='%(asctime)s:%(levelname)s:%(message)s',
                             datefmt='%Y-%m-%d %H:%M:%S')

    def convertDataForPostgre(self, data: dict) -> list:
        """Метод для преобразования данных для отправки в Postgre"""
        time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        time_str = f'{data.pop(self.time_str)}{self._timezone}'
        time_unix = datetime.strptime(
            time_str, f"%Y-%m-%d %H:%M:%S{self._timezone}").timestamp()
        if self._timezone.isalpha():
            timezone = 0
        else:
            timezone = 3600 * int(self._timezone)
        time_unix -= timezone
        time_unix = round(time_unix)
        time_str = datetime.fromtimestamp(time_unix).\
            strftime("%Y-%m-%d %H:%M:%SZ")
        car_number = data.pop(self.car_number)
        longitude = data.pop(self.longitude)
        latitude = data.pop(self.latitude)
        speed = round(float(data.pop(self.speed)))
        direction = data.pop(self.direction)
        if data.pop(self.valid) == 't':
            valid = True
        else:
            valid = False
        if data.pop(self.moving) == 't':
            moving = True
        else:
            moving = False
        if data.pop(self.actual) == 't':
            actual = True
        else:
            actual = False
        odometer = data.pop(self.odometer)
        if data.pop(self.alarmbutton) == 't':
            alarmbutton = True
        else:
            alarmbutton = False
        id_car = data.pop(self.id_car)
        altitude = 0
        id_region = self._idregion
        return [time, id_car, latitude, longitude, altitude, direction, speed,
                odometer, id_region, car_number, time_str, time_unix, valid,
                actual, moving, alarmbutton]

    def writeToDb(self, cursor, data: list):
        """Метод для записи данных в базу данных"""
        cursor.execute(
            """INSERT INTO raw_data
            (time, id_car, latitude, longitude, altitude, direction, speed,
            odometer, id_region, car_numder, time_str, time_unix, valid,
            actual, moving, alarmbutton)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", data)

    def checkRowData(self, cursor, row: dict):
        """Метод для проверки наличия данных в базе данных"""
        time_str = f'{row.get(self.time_str)}{self._timezone}'
        id_car = row.get(self.id_car)
        self.log.info(f'[DUMP IMPORT] ReadRowCSV <= {time_str} | {id_car}')
        cursor.execute(
            'SELECT COUNT(*) FROM raw_data WHERE time_str=%s and id_car=%s',
            (time_str, id_car,))
        # если данных нет, записываем их
        if not cursor.fetchone()[0]:
            data = self.convertDataForPostgre(data=row)
            self.writeToDb(cursor=cursor, data=data)
            self.log.info(f'[DUMP IMPORT] WriteRowData => {data}')

    def readCSVfile(self, cursor):
        """Метод для чтения данных из CSV файла дампа базы данных"""
        try:
            with open(self._csv, 'r') as read_obj:
                csv_dict_reader = DictReader(read_obj)
                for row in csv_dict_reader:
                    self.checkRowData(cursor=cursor, row=row)
        except FileNotFoundError as err:
            self.log.error(f'[DUMP IMPORT] readCSVfile => {err}')

    def insertData(self):
        """Метод для вставки данных в Postgre"""
        try:
            connect = psycopg2.connect(**self._dbconf)
            with closing(connect) as conn:
                with conn.cursor() as cursor:
                    conn.autocommit = True
                    self.readCSVfile(cursor=cursor)
        except (OperationalError, TypeError, KeyboardInterrupt) as err:
            self.log.error(f'[DUMP IMPORT] insertData => {err}')


def run_import():
    """Метод для запуска процесса импротра данных из CSV файла в базу данных"""
    db = PostgreDB()

    try:
        logging.info("[DUMP IMPORT] Start import CSV Dump")
        db.insertData()
    except (KeyboardInterrupt, OSError) as err:
        logging.exception(f'[DUMP IMPORT] Unexpected exception {err}')
    finally:
        logging.info("[DUMP IMPORT] Done import CSV Dump")
