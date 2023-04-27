# Микросервис USER-Service проекта A-Geld

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)

A-Geld - это WEB и мобильное приложение дистанционного банковского обслуживания клиентов A-Geld - Банка. Система позволяет клиентам получить информацию о банковских продуктах (кредиты, депозиты, карты), совершать платежи, к примеру, оплачивать услуги интернет-связи и цифрового телевидения, коммунальные услуги. С помощью СДБО можно будет пополнять счета электронных кошельков, совершать платежи по произвольным реквизитам, переводы между вкладами и банковскими картами, а также осуществлять переводы средств клиентам Банка и других банков, обмен валюты, а также оформлять новые банковские продукты.


## Описание микросервиса USER-Service

Микросервис предназначен для создания, хранения, изменения персональных данных пользователей СДБО.

## Функционал

* Регистрация пользователей;
* Восстановление доступа пользователей;
* Просмотр настроек уведомлений;
* Изменение настроек уведомлений;
* Изменение пароля, секретного вопроса/ответа, номера телефона;
* Добавление/изменение e-mail.

## Структура

* Сервис вызывается продуктовым микросервисом по протоколу HTTPS, архитектурный стиль REST;
* C данным сервисом взаимодействуют микросервисом "Кредиты";
* Данный сервис взаимодействует с АБС банка для обмена данными о пользователях.

## Роли пользователей

### Авторизованный верифицированный пользователь (АВП)
Пользователь, авторизованный в СДБО, данные которого прошли проверку подлинности. Имеет полный набор прав, которые могут быть доступны клиенту банка.

### Не авторизованный пользователь (НАВП)
Имеет возможность пройти регистрацию.

## Установка

1. Клонировать репозиторий:

```
git clone https://git.astondevs.ru/aston/a-geld
```

2. Перейти в локальную папку проекта и установить зависимости:

```
poetry install
```

3. Настроить БД Postgres.

