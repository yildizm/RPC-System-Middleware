#!/usr/bin/env pyth
# -*- coding: utf-8 -*-

from __future__ import division
import numbers, json, jsonpickle, Pyro4, socket, select, exceptions, time, sys
import add_service_stub as stub

if __name__ == '__main__':
    if len(sys.argv) < 3 :
        sys.exit(0)

    stub = stub.add_service()
    print stub.add(int(sys.argv[1]), int(sys.argv[2]), 10)
    print stub.subtract(int(sys.argv[1]), int(sys.argv[2]), 10)