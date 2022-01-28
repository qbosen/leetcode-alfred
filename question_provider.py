"""
用于存储题目信息，加速关键词、题号等搜索
"""
import pickle
import typing
import os.path
from lc_struct import Question

dump_file = "dump_file"


def _load_questions() -> typing.List[Question]:
    if not os.path.exists(dump_file):
        return []
    questions = pickle.load(open(dump_file, 'r'))
    return questions


def _dump_questions(questions: typing.List[Question]):
    with open(dump_file, 'wr') as f:
        pickle.dump(questions, f)


def _reload_questions() -> typing.List[Question]:
    import web_query
    questions = web_query.query_all()
    _dump_questions(questions)
    return questions


def load_questions(force_reload=False) -> typing.List[Question]:
    questions = _load_questions()
    if force_reload or not questions:
        questions = _reload_questions()
    return questions


def today_question() -> Question:
    import web_query
    return web_query.question_of_today()
