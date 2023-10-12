# Quiz question collector

## Stack 

Python 3.8, FastApi 0.78.0, Docker, Docker-compose

### Описание

Проект запускается через Docker-Compose. Представляет собой интерфейс для загрузки вопросов для quiz игр.

### Установка, Как запустить проект:

https://github.com/Alex386386/quiz_questions_test
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Alex386386/quiz_questions_test
```

```
cd quiz_questions_test
```

Создайте файл .env со следующим содержанием:

```
APP_TITLE='Сборник вопросов для викторины'
DATABASE_DSN=postgresql+asyncpg://postgres:postgres@db:5432/postgres
DB_NAME=fastapipostgres
POSTGRES_USER=<your login>
POSTGRES_PASSWORD=<your password>
DB_HOST=db
DB_PORT=5432
```

Запуск приложения в фоновом режиме:

```
sudo docker compose up -d
```

Документация по работе с проектом будет доступна по следующему адресу:

```
http://localhost/docs
```

### После запуска приложения вам будут доступны следующие эндпоинты:
1.  Запрос на загрузку данных в БД и получение последнего загруженного вопроса.

    ```
    http://localhost/question/download_and_get_last
    ```
    
    Ответ:
    ```json
    {
      "id": id,
      "question_text": "text",
      "answer": "answer",
      "created_at": "datetime"
    }
    ```

2.  Запрос на получение всех вопросов находящихся в БД.

    ```
    http://localhost/question/all
    ```
    
    Ответ:
    ```json
    [
      {
        "id": id,
        "question_text": "text",
        "answer": "answer",
        "created_at": "datetime"  
      },
      {
        "id": id,
        "question_text": "text",
        "answer": "answer",
        "created_at": "datetime"
      }
    ]
    ```

3.  Запрос на получение случайного вопроса из БД.

    ```
    http://localhost/question/random
    ```
    
    Ответ:
    ```json
    {
      "id": id,
      "question_text": "text",
      "answer": "answer",
      "created_at": "datetime"
    }
    ```

4.  Получение вопроса по его id.

    ```
    http://localhost/question/<id>
    ```
    
    Ответ:
    ```json
    {
      "id": id,
      "question_text": "text",
      "answer": "answer",
      "created_at": "datetime"
    }
    ```

5.  Исключительно в тестовых целях в проект добавлен эндпоинт на очистку БД.

    ```
    http://localhost/question/delete_all
    ```
    
    Ответ:
    ```json
    {
      "answer": "all questions were deleted"
    }
    ```

6.  Документация.

    ```
    http://localhost/docs
    ```
    
Автор:
- [Александр Мамонов](https://github.com/Alex386386) 