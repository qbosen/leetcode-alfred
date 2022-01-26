import http.client
import json
import typing
from pprint import pprint

import dotdict
from lc_struct import Question, Difficulty, TopicTag


def _parse_question(quest) -> Question:
    return Question(
        title=quest.title,
        titleCn=quest.titleCn,
        titleSlug=quest.titleSlug,
        frontendQuestionId=quest.frontendQuestionId,
        difficulty=Difficulty.of(quest.difficulty),
        topicTags=list(map(lambda t: TopicTag(t.name, t.nameTranslated), quest.topicTags)),
        acRate=quest.acRate
    )


def question_of_today() -> Question:
    raw_dict = _question_of_today()
    question_dot_dict = dotdict.DotDict(raw_dict)
    today_question = question_dot_dict.data.todayRecord[0].question
    return _parse_question(today_question)


def query_keyword(keyword: str) -> typing.List[Question]:
    if not keyword:
        return []
    raw_dict = _slice_query(keyword)
    data = dotdict.DotDict(raw_dict)
    questions = data.data.problemsetQuestionList.questions

    return list(map(_parse_question, questions))


def query_all() -> typing.List[Question]:
    skip = 0
    limit = 100
    has_more = True
    res = []
    while has_more:
        raw_dict = _slice_query(skip=skip, limit=limit)
        data = dotdict.DotDict(raw_dict)
        has_more = data.data.problemsetQuestionList.hasMore
        questions = data.data.problemsetQuestionList.questions
        skip = skip + limit
        res += map(_parse_question, questions)
    return res


def _slice_query(keyword: str = '', skip: int = 0, limit: int = 50) -> dict:
    conn = http.client.HTTPSConnection("leetcode-cn.com")
    conn.request("POST", "/graphql/", headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                 body=json.dumps({
                     "variables": {
                         "categorySlug": "", "skip": skip, "limit": limit,
                         "filters": {"searchKeywords": f"{keyword}"}
                     },
                     "operationName": "problemsetQuestionList",
                     "query": """
    query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
      problemsetQuestionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
      ) {
        hasMore
        total
        questions {
          acRate
          difficulty
          frontendQuestionId
          solutionNum
          title
          titleCn
          titleSlug
          topicTags {
            name
            nameTranslated
            id
            slug
          }
        }
      }
    }"""}))
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


def _question_of_today() -> dict:
    conn = http.client.HTTPSConnection("leetcode-cn.com")
    conn.request("POST", "/graphql/", headers={'Accept': 'application/json', 'Content-Type': 'application/json'},
                 body=json.dumps({
                     "variables": {},
                     "operationName": "questionOfToday",
                     "query": """
    query questionOfToday {
      todayRecord {
        date
        question {
          questionId
          frontendQuestionId: questionFrontendId
          difficulty
          title
          titleCn: translatedTitle
          titleSlug
          acRate
          solutionNum
          topicTags {
            name
            nameTranslated: translatedName
            id
          }
        }
      }
    }"""}))
    res = conn.getresponse()
    data = res.read()
    return json.loads(data.decode("utf-8"))


if __name__ == '__main__':
    pprint(_question_of_today())
