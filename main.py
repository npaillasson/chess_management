#! /usr/bin/env python3
# coding: utf-8

import os
import sys
import signal
from controller import Browse


def program_closing(signal, frame):
    sys.exit(0)