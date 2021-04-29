### Import coordinates

[Python Decouple: Strict separation of settings from code](https://github.com/henriquebastos/python-decouple/)   
[Python Decouple: Strict separation of settings from code](https://pypi.org/project/python-decouple/)   
[How to Set and Get Environment Variables in Python](https://able.bio/rhett/how-to-set-and-get-environment-variables-in-python--274rgt5)   
[os — Miscellaneous operating system interfaces](https://docs.python.org/3/library/os.html)   
[Python | os.environ object](https://www.geeksforgeeks.org/python-os-environ-object/)    

```python
import os
#=======================================================
# Set environment variables
os.environ['API_USER'] = 'username'
os.environ['API_PASSWORD'] = 'secret'
#=======================================================
# Get environment variables
USER = os.getenv('API_USER')
PASSWORD = os.environ.get('API_PASSWORD')
#=======================================================
# Getting non-existent keys
FOO = os.getenv('FOO') # None
BAR = os.environ.get('BAR') # None
BAZ = os.environ['BAZ'] # KeyError: key does not exist.
#=======================================================
pip install python-decouple

touch .env   # create a new .env file
USER=alex
KEY=hfy92kadHgkk29fahjsu3j922v9sjwaucahf

from decouple import config

API_USERNAME = config('USER')
API_KEY = config('KEY')
#=======================================================
```

---
[Could not find a version that satisfies the requirement pkg-resources==0.0.0](https://stackoverflow.com/questions/40670602/could-not-find-a-version-that-satisfies-the-requirement-pkg-resources-0-0-0)   

```shell
pip uninstall pkg-resources==0.0.0
```

```shell
"row": [
[
"Period",
"Период",
""
],
[
"Fld325",
"ObjectID",
"РегистрСведений.Координаты.Измерение.ObjectID"
],
[
"Fld326",
"lon",
"РегистрСведений.Координаты.Ресурс.lon"
],
[
"Fld327",
"lat",
"РегистрСведений.Координаты.Ресурс.lat"
],
[
"Fld328",
"speed",
"РегистрСведений.Координаты.Ресурс.speed"
],
[
"Fld329",
"dir",
"РегистрСведений.Координаты.Ресурс.dir" - Азимут, направление
],
[
"Fld330",
"valid",
"РегистрСведений.Координаты.Ресурс.valid" - Валидные данные
],
[
"Fld331",
"motion",
"РегистрСведений.Координаты.Ресурс.motion" - Признак движения
],
[
"Fld332",
"online",
"РегистрСведений.Координаты.Ресурс.online"
],
[
"Fld333",
"mileage",
"РегистрСведений.Координаты.Ресурс.mileage" -Пробег
],
[
"Fld334",
"alarmButton",
"РегистрСведений.Координаты.Ресурс.alarmButton"
],
[
"Fld335",
"carId",
"РегистрСведений.Координаты.Ресурс.carId"
]
]
}
```

```shell
select * from raw_data order by id desc limit 1;

select count(*) from raw_data where time_str='2021-04-29T09:59:57Z' and id_car='81801'
```  
