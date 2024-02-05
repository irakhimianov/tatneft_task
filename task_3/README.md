# Установка

* Склонировать проект
* Установить зависимости:
  * Без библиотек для тестов и линтеров
    * ```shell
      poetry install --without dev,test
      ```
  * Все зависимости:
    * ```shell
      poetry install
      ```
  * Установка с использованием `pip` (без библиотек для тестов и линтеров)
    * ```shell
      python -m pip install -r requirements.txt
      ```
* Установить `pre-commit`
  * ```shell
    pre-commit install
    ```
* Применить миграции БД:
  * ```shell
    make migrate
    ```
* Изменить файл `env.example` и сохранить как `.env`:
* Создать суперпользователя:
  * ```shell
    make su
    ```
* Запустить:
  * ```shell
    make run
    ```
* Задать в админке `crontab` и создать периодическую задачу на синхронизацию с сервисами.