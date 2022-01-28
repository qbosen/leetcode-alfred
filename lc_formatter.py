import textwrap
import typing
from datetime import date

from lc_struct import TopicTag, Question


def logseq_note(title: str, slug: str, front_id: str, difficulty: str, tags: typing.List[str],
                date_str: str = None) -> str:
    """
    按 logseq 的笔记格式 输出 leetcode 题目笔记
    @param title: 标题
    @param slug: 标题槽，用于唯一确定一个题目
    @param front_id: 前台展示题目id, eg: "1601", "剑指 Offer II 088"
    @param difficulty: 题目难易程度, eg: "easy", "medium", "hard"
    @param tags: 题目标签
    @param date_str: 日期字符串, 不传则为今天。默认格式为 "%Y-%m-%d", eg: "2021-08-17"
    @return: 格式化后的笔记内容
    """
    if not date_str:
        date_str = date.today().strftime("%Y-%m-%d")

    return textwrap.dedent(f"""\
    - Leetcode/[{front_id}] {title}
        - url:: [{title}]({leetcode_url(slug)})
          lc-no:: {front_id}
          lc-difficulty:: {difficulty.capitalize()}
          lc-tags:: {' '.join([f"[[{tag}]]" for tag in tags])}
        - [[{date_str}]]
        """)


def logseq_question_note(question: Question, cn=True) -> str:
    get_tag_name: typing.Callable[[TopicTag], str] = lambda t: t.nameTranslated if cn else t.name
    note = logseq_note(
        title=question.titleCn if cn else question.title,
        slug=question.titleSlug,
        front_id=question.frontendQuestionId,
        difficulty=question.difficulty.name,
        tags=list(map(get_tag_name, question.topicTags)),
        date_str=None
    )
    return note


def leetcode_url(slug: str) -> str:
    return f'https://leetcode-cn.com/problems/{slug}/description/'
