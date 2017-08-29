#!/usr/bin/env pyth
# -*- coding: utf-8 -*-

from __future__ import division
import numbers, json, jsonpickle, Pyro4, socket, select, exceptions, sys, threading
import add_service_skeleton as skeleton

class A(object):
    def __init__(self, name):
        self.name = name

    def add(self, a, b):
        return a+b, 'addition'

    def subtract(self, a, b):
        return a-b, 'subtraction'

if __name__ == '__main__':
    a = A('test')
    server_skeleton = skeleton.add_service(a)
    print 'Running the server'
    server_skeleton.run()
