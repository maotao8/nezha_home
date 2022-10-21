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

__author__ = "maotao8"

import os
import sys
import logging

from airtest.core.api import *

logger = logging.getLogger("airtest")
logger.setLevel(logging.DEBUG)

def main(args=None):
    if not args:
        if len(sys.argv) < 2:
            print("no cmdline args")
            return False
        args = sys.argv
    elif len(args) < 2:
        print("less main args")
        return False
    print(args)

    serialno = args[1]
    device = "Android:///%s" % serialno

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

    print("m8tdbg +++++++++++++++++++++++++++++++++")
    print("m8tdbg orientation %d width %d height %d" % (orientation, width, height))
    print("m8tdbg =================================")
    print("go back HOME!")
    
    home()
    return True

if __name__ == '__main__':
    main(sys.argv)
