#!/usr/bin/python

import os
import sys
import re
import subprocess


devnull = open(os.devnull, 'w')


def call(cmd):
    p = subprocess.Popen(cmd.split(),
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return out.decode('utf-8'), err.decode('utf-8'), p.returncode


def execute(cmd, silent=False):
    if silent:
        params = {
            'stdout': devnull,
            'stderr': devnull,
        }
    else:
        params = {}

    retcode = subprocess.call(cmd.split(), **params)
    return retcode


def exists(cmd):
    return execute('which %s' % cmd, silent=True) == 0


def get_modified(ext):
    modified = re.compile(r'^(?:M|A).(?P<name>.*\.%s)' % ext)
    out, _, _ = call('git status --porcelain')
    modifieds = []
    for line in out.splitlines():
        match = modified.match(line.strip())
        if match:
            modifieds.append(match.group('name'))
    return modifieds


def get_project_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def output(prg, out, err):
    print(' * %s:\n%s\n%s' % (prg, out, err))


def die(msg):
    print(msg)
    sys.exit(1)


def check_python():

    modifieds = get_modified('py')
    if not modifieds:
        return

    has_pep8 = exists('pep8')
    has_pylint = exists('pylint')
    has_pyflakes = exists('pyflakes')
    if not (has_pep8 or has_pylint or has_pyflakes):
        die('Install PEP8, PyLint and PyFlakes!')

    rrcode = 0
    for f in modifieds:
        if has_pep8:
            out, err, _ = call('pep8 %s' % f)
            if out or err:
                output('pep8', out, err)
                rrcode = rrcode | 1
        if has_pylint:
            retcode = execute('pylint -f parseable -E -d E0213,E1101,E1002,E1121,E0211,E0611,E0602,E1103 %s' % f)
            rrcode = retcode | rrcode
        if has_pyflakes:
            retcode = execute('pyflakes %s' % f)
            rrcode = retcode | rrcode

    if rrcode != 0:
        sys.exit(rrcode)


def check_javascript():

    modifieds = get_modified('js') + get_modified('jsx')
    if not modifieds:
        return

    has_jsl = exists('eslint')
    if not has_jsl:
        die('Install eslint!')

    rrcode = 0
    for f in modifieds:
        conf = os.path.join(get_project_path(), 'luckybreak', 'static', 'js', 'apps', '.eslintrc')
        out, err, retcode = call('eslint -c {} {}'.format(conf, f))
        if out or err:
            output('eslint', out, err)
            rrcode = rrcode | retcode

    if rrcode != 0:
        sys.exit(rrcode)


def django_tests():
    rrcode = 0
    out, err, retcode = call('python manage.py test --settings config.settings.test --keepdb')
    if err:
        output('django', out, err)
        rrcode = rrcode | retcode

    if rrcode != 0:
        sys.exit(rrcode)


def main():
    check_python()
    check_javascript()
    django_tests()


if __name__ == '__main__':
    main()
