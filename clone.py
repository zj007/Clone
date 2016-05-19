#!/usr/bin/env python
#author : zj007

import sys
import os
import re
import commands

def shell(cmd):
    status, output =  commands.getstatusoutput(cmd)
    return status >> 8, output

class Conf(object):
    def __init__(self, clone_file):
        self._clone_file = clone_file
        self._comment_flag = '#'
        self._assignment_flag = ':'
        self._regular_flag = '@'
        self._parse()

    def get_from_path(self):
        return self._conf_dict['from_dir']

    def get_to_path(self):
        return self._conf_dict['to_dir']

    def is_omit(self, flag, name):
        if flag == 'd':
            l = self._conf_dict['omit_dir']
        elif flag == 'f':
            l = self._conf_dict['omit_file']
        else:
            return False
        if name in l[0]:
            return True
        for e in l[1]:
            if e.match(name):
                return True
        return False
    
    def _parse(self):
        '''
        raise Exception
        '''
        self._conf_dict = {}
        with open(self._clone_file) as fr:
            line_num = 0
            for line in fr:
                line_num += 1
                expression = line.strip().split(self._comment_flag)[0]
                if expression == '':
                    continue
                if ':' not in expression:
                    print 'format error :%d %s (%s)'%(line_num, expression, self._clone_file)
                    raise Exception('parse Clone file failed')
                key, value = expression.split(self._assignment_flag)
                key = key.strip()
                value = value.strip()
                if key == '' or value == '':
                    print 'format error :%d %s (%s)'%(line_num, expression, self._clone_file)
                    raise Exception('parse Clone file failed')
                self._conf_dict[key] = value
        dir_list = ['from_dir', 'to_dir']
        for key in dir_list:
            if key not in self._conf_dict:
                print 'need %s (%s)'%(key, self._clone_file)
                raise Exception('parse Clone file failed')
            if not os.path.isdir(self._conf_dict[key]):
                print 'dir not exist : %s %s (%s)'%(key, self._conf_dict[key] , self._clone_file)
                raise Exception('parse Clone file failed')
        omit_key = ['omit_dir', 'omit_file']
        for key in omit_key:
            if key in self._conf_dict:
                try:
                    value_str = self._conf_dict[key]
                    self._conf_dict[key] = eval(value_str)
                    if not isinstance(self._conf_dict[key], list):
                        raise Exception()
                except:
                    print 'omit_dir value error : %s (%s)'%(self._conf_dict['omit_dir']. self._clone_file)
                    raise Exception('parse Clone file failed')
                tmp = self._conf_dict[key]
                self._conf_dict[key] = [[],[]]
                for e in tmp:
                    if e.startswith('@'):
                        self._conf_dict[key][1].append(re.compile(e[1:]))
                    else:
                        self._conf_dict[key][0].append(e)

def drop_rt_path(path, rt):
    return os.path.relpath(path, rt)

def join_rt_path(rt, path):
    return os.path.join(rt, path)

def clone(conf_file):
    if conf_file == '':
        conf_file = './Clone'
    if not os.path.isfile(conf_file):
        print '%s not exist'%conf_file
        return
    try:
        conf = Conf(conf_file)
    except Exception as e:
        print '%s'%e
        return
    from_dir = conf.get_from_path()
    to_dir = conf.get_to_path()
    for rt, dirname, filename in os.walk(from_dir):
        rel_path = drop_rt_path(rt, from_dir)
        to_path = join_rt_path(to_dir, rel_path)
        omit_dir = []
        omit_file = []
        #dir
        for d in dirname:
            if conf.is_omit('d', d):
                omit_dir.append(d)
                continue
            ret, output = shell("mkdir -p %s"%(join_rt_path(to_path, d)))
            if ret != 0:
                print 'shell error[%d]'%ret
                return
        for d in omit_dir:
            dirname.remove(d)
        
        #none-dir file
        for f in filename:
            if conf.is_omit('f', f):
                omit_file.append(f)
                continue
            ret, output = shell("cp %s %s"%(join_rt_path(rt, f), to_path))
            if ret != 0:
                print 'shell error[%d]'%ret
                return

    print 'clone success'

def gen_clone_file(root_path):
    file_name = os.path.join(root_path, 'Clone')
    with open(file_name, 'w') as fw:
        contents = [
                    '# gen by clone v0.1',
                    'from_dir : ',
                    'to_dir : ',
                    'omit_dir : []',
                    'omit_file : []'
                   ]
        fw.writelines([e+'\n' for e in contents])

def main():
    argv = sys.argv
    if len(argv) == 1:
        clone('')
        return
    if not argv[1].startswith('-'):
        clone(argv[1])
        return
    cmd = argv[1]

    if cmd == '-c':
        if len(argv) == 2:
            gen_clone_file('.')
        elif len(argv) > 2:
            gen_clone_file(argv[2])
        else:
            pass

if __name__ == '__main__':
    main()
