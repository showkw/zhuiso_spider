# -*- coding: utf-8 -*-
import time
import os
from Config.Config import RUNTIME_DIR

sleepTime = 10
slist = []
slist.append(dict(
    key='core',
    fileName=RUNTIME_DIR + 'core_worker.txt',
    runFile='./core/run.py',
))
# slist.append(dict(
#     key='fc',
#     fileName=RUNTIME_DIR+'fc_worker.txt',
#     runFile='runFc.py',
# ))

print(os.getcwd())


def main():
    for sp in slist:
        print(sp['key'] + 'Spider--运行--' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        os.system("python " + sp['runFile'] + ' ' + os.getcwd())
    while True:
        workNum = {}
        lastNum = {}
        for sp in slist:
            print(sp['key'] + 'Spider--运行--' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
            os.system("python " + sp['runFile'])
            if os.path.exists(sp['fileName']):
                file = open(sp['fileName'], 'r')
                workNum[sp['key']] = int(file.read())
                file.close()
            else:
                file = open(sp['fileName'], 'w')
                file.write('1')
                workNum[sp['key']] = 1
                lastNum[sp['key']] = 1
                file.close()
        time.sleep(sleepTime)
        for sp in slist:
            file = open(sp['fileName'], 'r')
            lastNum[sp['key']] = int(file.read())
            file.close()
            if lastNum[sp['key']] == workNum[sp['key']]:
                print(sp['key'] + 'Spider--运行--' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                os.system("python " + sp['runFile'])


if __name__ == '__main__':
    main()
