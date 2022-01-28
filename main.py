import sys
import argparse

import workflow.workflow3
from workflow import Workflow3
from lc_struct import Question, Difficulty

parser = argparse.ArgumentParser(prog='leetcode', description='查询/搜索leetcode题目，复制为笔记，导航至网页')
parser.add_argument('today', action='store_true', help='获取每日一题')
parser.add_argument('query', action='store', nargs='*', help='搜索关键字')
parser.add_argument('reload', action='store_true', help='更新题目列表缓存')


def main(_):
    import question_provider as provider
    if args.today:
        add_item(provider.today_question())
    elif args.query:
        items = provider.load_questions()
        query_words = ' '.join(args.query)
        # 按 题号，英文标题，中文标题 组合搜索关键字
        for filtered in wf.filter(
                query_words, items,
                key=lambda q: q.frontendQuestionId + q.title + q.titleCn,
                max_results=20):
            add_item(filtered)
    elif args.reload:
        provider.load_questions(force_reload=True)

    wf.warn_empty('No result found!', 'Try other inputs...', icon='icon/wrong.png')
    wf.send_feedback()


def add_item(q: Question) -> workflow.workflow3.Item3:
    import lc_formater
    icon_dic = {
        Difficulty.Easy: 'icon/easy.png',
        Difficulty.Medium: 'icon/medium.png',
        Difficulty.Hard: 'icon/hard.png',
    }
    return wf.add_item(
        title=f'[{q.frontendQuestionId}] {q.titleCn}',
        subtitle=f'[{round(q.acRate, 2)}] {q.title}',
        arg=q.titleSlug,
        valid=True,
        icon=icon_dic[q.difficulty],
        copytext=lc_formater.logseq_note(q, cn=True),
        quicklookurl=lc_formater.leetcode_url(q.titleSlug)
    )


if __name__ == '__main__':
    wf = Workflow3()
    args = parser.parse_args(wf.args)
    log = wf.logger
    sys.exit(wf.run(main))
