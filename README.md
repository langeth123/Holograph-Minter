# Holograph-Minter

**With love for : https://t.me/swiper_tools**

**Приобрести бота на ZkSync / LayerZero можно тут: https://t.me/swipersoft_bot**

**DEV           : https://t.me/lang_crypto**


# Features

- **Минт любых нфт во всех доступных сетях**


### Settings

Смотри settings.json file

~~~python
"""
ContractAddress - Адрес коллекции, можно менять на абсолютно любой другой
ThreadRunnerSleep - мин/макс время в секундах. Интервал между запуском потоков
UseNets - названия сетей в которых минтер будет работать

GWEI - настройка максимально возможного gwei для отправки транзы

"""

~~~

Чтобы начать работу:
 - Загрузи приватники в файл secrets.txt


### How to run script
1. Устанавливаем Python: https://www.python.org/downloads/, я использую версию 3.9.8
2. При установке ставим галочку на PATH при установке

>![ScreenShot](https://img2.teletype.in/files/19/03/19032fbe-1912-4bf4-aed6-0f304c9bf12e.png)

3. После установки скачиваем бота, переносим все файлы в одну папку (создаете сами, в названии и пути к папке не должно быть кириллицы и пробелов)
4. Запускаем консоль (win+r -> cmd)
5. Пишем в консоль:
cd /d Директория
* Директория - путь к папке, где лежит скрипт (само название скрипта писать не нужно)
6. Прописываем:
pip install -r requirements.txt
