#!/usr/bin/env python3
import configparser
import importlib.util
import os
import pathlib
import shutil
import sys

# 目标workflow目录，可以先创建一个空的workflow，然后执行此脚本 复制相关代码
workflow_path = None

# workflow需要的python module
modules = []
# workflow 需要的用户代码，相对于当前脚本文件
files = [
    'icon', 'workflow',
    'clipboard.py', 'dotdict.py', 'lc_formatter.py', 'lc_struct.py',
    'main.py',
    'question_updater.py', 'web_query.py', ]
# 初始化会复制module相关内容
init = False

if __name__ == '__main__':
    bin_path = pathlib.Path(__file__).absolute().parent
    if not workflow_path:
        # 没有写在代码里面 就从配置里面获取（不想提交
        config_ini = bin_path / 'config.ini'
        if not os.path.exists(config_ini):
            raise FileNotFoundError("config.init not exists")
        config = configparser.ConfigParser()
        config.read(config_ini)
        workflow_path = config['DEFAULT']['workflow_path']
        if not workflow_path:
            raise Exception('[workflow_path] config not exists')

    workspace = bin_path.parent
    print("脚本目录: ", workspace)
    workflow_home = pathlib.Path(workflow_path)
    if not workflow_home.exists():
        raise FileNotFoundError(workflow_home)

    # 导入workflow 和 modules
    if init or (len(sys.argv) > 1 and sys.argv[1] == 'init'):
        # 导入本地py3版本的workflow
        wf_dir = workflow_home.joinpath("workflow")
        if not wf_dir.exists():
            module_spec = importlib.util.find_spec("workflow")
            module_src = pathlib.Path(module_spec.origin).parent
            shutil.copytree(module_src, wf_dir, dirs_exist_ok=True)

        # 安装modules到lib
        wf_lib = workflow_home.joinpath('lib')
        if not wf_lib.exists():
            wf_lib.mkdir()
        for module in modules:
            os.system(f"pip3 install --target='{wf_lib}' {module}")

    # 复制用户文件
    for file in files:
        source = workspace.joinpath(file)
        if source.is_file():
            print("复制文件:", file)
            shutil.copy2(source, workflow_home)
        elif source.is_dir():
            print("复制目录:", file)
            shutil.copytree(source, workflow_home.joinpath(source.name), dirs_exist_ok=True)
