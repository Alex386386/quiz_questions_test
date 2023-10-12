from typing import Optional

import requests
from fastapi import HTTPException

main_url: str = 'https://jservice.io/api/random'
MAX_RETRIES: int = 10


def fetch_questions_from_jservice(url: str, count: Optional[int] = None) -> list:
    finish_url = f'{url}?count={count}' if count else url
    response = requests.get(finish_url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail='jService API not reachable')
    return response.json()
