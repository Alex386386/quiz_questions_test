from datetime import datetime
from typing import List, Union

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import error_if_not_exist
from app.core.db import get_async_session
from app.core.utils import (
    fetch_questions_from_jservice,
    main_url,
    MAX_RETRIES,
)
from app.crud.question import question_crud
from app.schemas.question import QuestionDB

router = APIRouter()


@router.post(
    '/download_and_get_last',
    response_model=QuestionDB,
)
async def create_question(
        questions_num: int = Query(1, ge=1, le=100000),
        session: AsyncSession = Depends(get_async_session)
) -> Union[QuestionDB, dict]:
    questions = fetch_questions_from_jservice(main_url, questions_num)

    existing_question_ids = await question_crud.get_all_ids(session)

    new_questions = []

    for question in questions:
        if question['id'] not in existing_question_ids:
            new_questions.append(question)
        else:
            retry_count = 0
            while retry_count < MAX_RETRIES:
                try:
                    new_question = fetch_questions_from_jservice(main_url)[0]
                    if new_question['id'] not in existing_question_ids:
                        new_questions.append(new_question)
                        break
                    retry_count += 1
                except HTTPException:
                    break

    objs_to_insert = [{
        'id': question['id'],
        'question_text': question['question'],
        'answer': question['answer'],
        'created_at': datetime.fromisoformat(question['created_at'].replace('Z', '')),
        'downloaded_at': datetime.now()
    } for question in new_questions]

    await question_crud.bulk_create(objs_to_insert, session)

    last_question = await question_crud.get_last_downloaded_question(session)
    if last_question:
        return last_question
    return {}


@router.get(
    '/all',
    response_model=List[QuestionDB],
)
async def get_all_questions(
        session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:
    questions = await question_crud.get_multi(session)
    await error_if_not_exist(questions)
    return questions


@router.get(
    '/random',
    response_model=QuestionDB,
)
async def get_random_question(
        session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:
    question = await question_crud.get_random_question(session)
    await error_if_not_exist(question)
    return question


@router.get(
    '/{question_id}',
    response_model=QuestionDB,
)
async def get_by_id(
        question_id: int,
        session: AsyncSession = Depends(get_async_session),
) -> QuestionDB:
    question = await question_crud.get_by_id(question_id, session)
    await error_if_not_exist(question)
    return question


@router.delete('/delete_all')
async def delete_all_questions(session: AsyncSession = Depends(get_async_session)) -> dict:
    await question_crud.delete_all(session)
    return {'answer': 'all questions were deleted'}
