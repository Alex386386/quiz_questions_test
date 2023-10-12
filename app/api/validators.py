from typing import List, Union

from fastapi import HTTPException

from app.schemas.question import QuestionDB


async def error_if_not_exist(object: Union[QuestionDB, List[QuestionDB], None]) -> None:
    if not object:
        raise HTTPException(status_code=404, detail='No questions or question.')
