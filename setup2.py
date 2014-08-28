#!/usr/bin/env python
# -*- coding: utf8 -*-
from distutils.core import setup

setup(name='SampleRPC',
      version='1.0',
      description=u'Класс сервера и слиента для организации rpc на базе tcpip сокетов',
      author='AlexLexx',
      author_email='AlexLexx1@gmail.com',
      url='https://github.com/AlexLexx706',
      packages=['tcp_rpc', 'tcp_rpc.test']
     )