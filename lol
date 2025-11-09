(venv) PS C:\Users\PC\Desktop\корниенко\WLbackend> & C:/Users/PC/Desktop/корниенко/WLbackend/venv/Scripts/python.exe c:/Users/PC/Desktop/корниенко/WLbackend/main.py
Traceback (most recent call last):
  File "c:\Users\PC\Desktop\корниенко\WLbackend\main.py", line 2, in <module>
    from interface import DataBaseInterface, config, securuty
  File "c:\Users\PC\Desktop\корниенко\WLbackend\interface.py", line 5, in <module>
    from authx import AuthX, AuthXConfig
  File "C:\Users\PC\Desktop\корниенко\WLbackend\venv\lib\site-packages\authx\__init__.py", line 5, in <module>
    from authx.config import AuthXConfig
  File "C:\Users\PC\Desktop\корниенко\WLbackend\venv\lib\site-packages\authx\config.py", line 7, in <module>
    from jwt.algorithms import get_default_algorithms, requires_cryptography
  File "C:\Users\PC\Desktop\корниенко\WLbackend\venv\lib\site-packages\jwt\algorithms.py", line 10, in <module>
    from .exceptions import InvalidKeyError
ImportError: cannot import name 'InvalidKeyError' from 'jwt.exceptions' (C:\Users\PC\Desktop\корниенко\WLbackend\venv\lib\site-packages\jwt\exceptions.py
