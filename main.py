"""
leetcode 操作

Usage:
  leetcode.py -h | --help
  leetcode.py today [--copy --quiet --cn-tag] [--format=<fmt>]

Options:
  -h --help         Show this screen.
  --format=<fmt>    输出数据格式 [default: note].
                    note: logseq 中定义的笔记格式，也是默认输出
  --copy            复制结果到粘贴板
  --quiet           不进行标准输出
  --cn-tag           题目标签使用中文标签输出
"""

import sys

from workflow import Workflow3


def main(wf):
    pass


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))
