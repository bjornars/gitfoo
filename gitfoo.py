#! /usr/bin/env python3
import operator
import subprocess

from itertools import chain, product
from sys import stderr, exit

def error(s):
    print(s, file=stderr)
    exit(0)

GITFOO = 'gitfoo'
GITFOO_FILE = '.gitfoo'

hex = '0123456789abcdef'
numbers = list(map(lambda a: str().join(a), product(hex, hex)))
def name(number):
    return numbers[number % 256]

def git(*commands):
    command = ['git']
    command.extend(chain.from_iterable([each.split(' ') for each in commands]))
    data = subprocess.check_output(command)
    return data.decode('utf-8').strip()

revs = git('rev-list --reverse master').split()
branch = git('rev-parse --abbrev-ref HEAD')

if branch == GITFOO:
    error('cannot foo the foo branch')

git('branch -f', GITFOO)
git('checkout', GITFOO)

rev = revs
git('reset --hard', revs[0])

for num, rev in enumerate(revs):
    cruft = 0
    if num > 0:
        git('cherry-pick', rev)

    orig_rev = rev
    wanted = name(num)
    while 1:
        rev = git('rev-parse HEAD')
        if rev.startswith(wanted):
            print("{0}/{1} - {2}".format(num, len(revs), rev))
            break

        cruft += 1
        with open(GITFOO_FILE, 'w') as f:
            f.write(str(cruft))

        git('add', GITFOO_FILE)
        git('commit --amend -C HEAD')
