# -*- encoding=utf8 -*-
#
# Copyright 2022 by maotao8. All Rights Reserved.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation for any purpose and without fee is hereby granted,
# provided that the above copyright notice appear in all copies and that
# both that copyright notice and this permission notice appear in
# supporting documentation, and that the name of maotao8 not be used
# in advertising or publicity pertaining to distribution
# of the software without specific, written prior permission.
# MAOTAO8 DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE, INCLUDING
# ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# MAOTAO8 BE LIABLE FOR ANY SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES OR
# ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER
# IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT
# OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

import os
import re
import sys
import logging
import configparser
import platform

from airtest.core.api import *

__author__ = "maotao8"

TASK_CONF_FILE = "task.conf"
MAS_VER = "0.1.0.0"
TASK_NAME = "home"
if platform.system() == 'Windows':
    TASK_EXEC = 'home.exe'
else:
    TASK_EXEC = 'home'

logger = logging.getLogger(TASK_NAME)
#logger.setLevel(logging.DEBUG)
#logger.warning('__name__ : %s', __name__)
logger.warning(platform.system())

def write_task_conf(fileName,config=None):
    if not config:
        cfg = configparser.ConfigParser()
        cfg['task'] = {
            'name':TASK_NAME,
            'exec':TASK_EXEC,
            'enable':'yes',
            'mas_version':MAS_VER,
            'run_timestamp':'0',
            'start_time':'01:02:03',
            'run_seconds':'10',
            'wait_seconds':'3'
            }
    else:
        cfg=config
    with open(fileName, 'w') as configfile:
        cfg.write(configfile)
    return cfg


def read_task_conf(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)
    write_to_file = False

    # verify [task] section
    if not config.has_section("task"):
        config.add_section('task')
        write_to_file = True
    if not config.has_option('task', 'name'):
        config.set('task', 'name', TASK_NAME)
        write_to_file = True
    if not config.has_option('task', 'exec'):
        config.set('task', 'exec', TASK_EXEC)
        write_to_file = True
    if not config.has_option('task', 'enable'):
        config.set('task', 'enable', 'yes')
        write_to_file = True
    if not config.has_option('task', 'mas_version'):
        config.set('task', 'mas_version', MAS_VER)
        write_to_file = True
    if not config.has_option('task', 'run_timestamp'):
        config.set('task', 'run_timestamp', '0')
        write_to_file = True
    if not config.has_option('task', 'start_time'):
        config.set('task', 'start_time', '01:02:03')
        write_to_file = True
    if not config.has_option('task', 'run_seconds'):
        config.set('task', 'run_seconds', '10')
        write_to_file = True
    if not config.has_option('task', 'wait_seconds'):
        config.set('task', 'wait_seconds', '3')
        write_to_file = True
    if write_to_file:
        write_task_conf(fileName, config)
    return config


def verify_task_conf(fileName):
    config = configparser.ConfigParser()
    config.read(fileName)
    if not config.has_section("task"):
        return None
    if not config.has_option("task", "name"):
        return None
    if not config.has_option("task", "exec"):
        return None
    if not config.has_option("task", "enable"):
        return None
    if not config.has_option("task", "mas_version"):
        return None
    if not config.has_option("task", "run_timestamp"):
        return None
    if not config.has_option("task", "start_time"):
        return None
    if not config.has_option("task", "run_seconds"):
        return None
    if not config.has_option("task", "wait_seconds"):
        return None

    mas_version = config.get("task", "mas_version")
    name = config.get("task", "name")
    exec = config.get("task", "exec")
    en = config.get("task", "enable")
    run_timestamp = config.get("task", "run_timestamp")
    start_time = config.get("task", "start_time")
    run_seconds = config.get("task", "run_seconds")
    wait_seconds = config.get("task", "wait_seconds")

    return {
        'mas_version':mas_version,
        'name':name,
        'exec':exec,
        'enable':en,
        'run_timestamp':run_timestamp,
        'start_time':start_time,
        'run_seconds':run_seconds,
        'wait_seconds':wait_seconds
        }


def update_task_conf(fileName, config):
    run_timestamp = time.time().__int__()
    last_timestamp = config.getint('task', 'run_timestamp')
    if last_timestamp > run_timestamp:
        return config

    task = verify_task_conf(fileName)
    if not task:
        cfg = write_task_conf(fileName)
    else:
        cfg = configparser.ConfigParser()
        cfg['task'] = task
        write_task_conf(fileName, cfg)
    return cfg


def main(args=None):
    if not args:
        if len(sys.argv) < 3:
            logger.warning("no cmdline args")
            return False
        args = sys.argv
    elif len(args) < 3:
        logger.warning("less main args")
        return False

    for i in range(len(args)):
        logger.warning("m8tdbg: args[%d]=%s", i, args[i])

    pattern = re.compile(r'android://', re.IGNORECASE)
    if pattern.match(args[2]):
        head = args[2].find('/', 10)
        tail = -1
        if head > 0:
            tail = args[2].find('?', head)
            if tail > 0:
                serialno = args[2][head+1:tail]
            else:
                serialno = args[2][head+1:]
        else:
            serialno = args[2][10:]
        logger.warning("m8tdbg: head=%d", head)
        logger.warning("m8tdbg: tail=%d", tail)
        device = args[2]
    else:
        serialno = args[2]
        device = "android:///%s" % serialno

    logger.warning("m8tdbg: serialno=%s", serialno)
    logger.warning("m8tdbg: device=%s", device)

    # auto_setup(__file__,devices=[device],logdir=True,compress=90)
    auto_setup(basedir=os.path.dirname(os.path.abspath(__file__)),
               devices=[device],logdir=True,compress=90)

    # 获取当前手机的分辨率
    orientation = G.DEVICE.display_info['orientation']
    if orientation in [1,3]:  # 竖屏时
        height = G.DEVICE.display_info['width']
        width = G.DEVICE.display_info['height']
    else:  # 横屏时
        height = G.DEVICE.display_info['height']
        width = G.DEVICE.display_info['width']

    logger.warning("m8tdbg: +++++++++++++++++++++++++++++++++")
    logger.warning("m8tdbg: orientation %d width %d height %d" % (orientation, width, height))
    logger.warning("m8tdbg: =================================")
    logger.warning("go back HOME!")

    home()
    return True


if __name__ == '__main__':
    root_dir = os.path.dirname(os.path.abspath(__file__))
    conf_file = os.path.join(root_dir, TASK_CONF_FILE)
    if not os.path.exists(conf_file):
        write_task_conf(conf_file)

    config = read_task_conf(conf_file)
    config = update_task_conf(conf_file, config)

    args = []
    args.append(__file__)
    for i in range(len(sys.argv)):
        logger.warning("m8tdbg: argv[%d]=%s", i, sys.argv[i])
        if sys.argv[i] == "--device":
            if (i+1) < len(sys.argv):
                args.append(sys.argv[i])
                args.append(sys.argv[i+1])
                break

    if len(args) < 3:
        logger.warning("m8tdbg: less cmd args")
    else:
        main(args)
