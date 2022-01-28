import argparse
import sys

import web_query
import workflow
from lc_struct import Question, Difficulty
from workflow.background import run_in_background, is_running


def main(wf: workflow.Workflow3):
    parser = argparse.ArgumentParser(prog='leetcode', description='查询/搜索leetcode题目，复制为笔记，导航至网页')
    parser.add_argument('query', action='store', nargs='*', help='搜索关键字')
    parser.add_argument('--today', action='store_true', help='获取每日一题')
    args = parser.parse_args(wf3.args)
    wf.logger.debug("args: %s", args)

    def add_item(q: Question):
        """
        加载返回结果
        """
        import lc_formatter
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
            copytext=lc_formatter.logseq_question_note(q, cn=True),
            quicklookurl=lc_formatter.leetcode_url(q.titleSlug)
        )

    # 每日一题
    if args.today:
        add_item(web_query.question_of_today())
    # 关键字查询
    elif args.query:
        # 从缓存终获取结果
        query_words = ' '.join(args.query)
        items = wf.cached_data(f'q::{query_words}',
                               lambda: web_query.query_keyword(query_words),
                               max_age=7 * 24 * 60 * 60)
        for item in items:
            add_item(item)

    wf.warn_empty('No result found!', 'Try other inputs...', icon='icon/wrong.png')
    wf.send_feedback()


if __name__ == '__main__':
    wf3 = workflow.Workflow3()
    sys.exit(wf3.run(main))
