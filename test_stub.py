#!/usr/bin/env pyth
# -*- coding: utf-8 -*-

from __future__ import division
import numbers, json, jsonpickle, Pyro4, socket, select, exceptions, inspect, sys

'''Automatically generated client stub script.
   Please do not edit this file by any means'''

MSGLEN = 4096
SERVERNAME = 'test_service'

class test_stub:
    def __init__(self, timeout=10000, retry_count=5):
        self.server = SERVERNAME
        self.timeout = timeout
        self.retry_count = retry_count

    def send_request(self, func_name, serialized_data, soc):
        param_length = len(serialized_data)
        data = json.dumps({"size" : param_length, "func" : func_name, "param" : serialized_data})
        msg_len = len(data)
        sent_amount = 0
        while sent_amount < msg_len:
            temp = soc.send(data[sent_amount:])
            if temp == 0:
                raise IOError(0, 'Remote server socket disconnected')
            sent_amount += temp

        return 1

    def receive_response(self, soc, timeout):
        data = ''
        try:
            check = select.select([soc], [], [], timeout)
            if check[0]:
                data = soc.recv(MSGLEN)
                if data == '':
                    raise IOError(0, 'Remote server socket disconnected')
            else:
                raise IOError(1, 'Error while waiting response from remote server')
        except select.error as err:
            raise err

        return data

    def func1(self, a, b, id):
        # apply necessary type checkings
        if not isinstance(a, numbers.Number) or not isinstance(b, numbers.Number):
            return None, 'Invalid input arguments'

        # locate the server and retrieve connection information
        # Pyro is used only for getting remote server ip and port, from a dummy proxy object
        Pyro4.config.REQUIRE_EXPOSE = False
        try:
            name_server = Pyro4.locateNS()
        except NamingError:
            print 'Client Name Server Error:'
            print ''.join(Pyro4.util.getPyroTraceback())
            return None, 'Failed to locate name server'

        # locate the server and retrieve its address
        uri = name_server.lookup(self.server)
        remote_server = Pyro4.Proxy(uri)
        server_ip = remote_server.get_host()
        server_port = remote_server.get_port()
        print 'Located remote server at ' + server_ip + ':' + str(server_port)

        # marshall parameters, first parameter is the function call id
        param_list = [id, a, b]
        marshalled_param = jsonpickle.encode(param_list)
        func_name = inspect.stack()[0][3]

        # try to initiate a conection witht the server
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            soc.connect((server_ip, int(server_port)))
        except socket.error as err:
            print 'Client Socket Connection Error:\n {0}: {1}'.format(err.no, err.strerror)
            soc.shutdown()
            soc.close()
            return None, 'Failed to connect to the remote server'

        count = -1
        status = 0
        while count < self.retry_count and status == 0:
            count += 1
            # send the function name and its parameters to remote server
            try:
                status = self.send_request(func_name, marshalled_param, soc)
            except IOError as err:
                print 'Client Remote Server Connection Error\n: {0}: {1}'.format(err[0], err[1])
                soc.shutdown(1)
                soc.close()
                #return None, 'Problem while communicating with the remote server'

        if count == self.retry_count:
            return None, 'Client retry count reached'

        # wait for a response from the server in a proper json format
        count -= 1
        response = ''
        while count < self.retry_count and response == '':
            try:
                response = self.receive_response(soc, self.timeout/1000)
            except (IOError, select.error) as err:
                print 'Client Remote Server Response Error\n{0}: {1}'.format(err[0], err[1])
                #return None, 'No valid response received from remote server'

        if count == self.retry_count:
            return None, 'Client retry count reached'

        print response

        json_obj = json.loads(response)
        if json_obj['status'] == 'OK' or json_obj['status'] == 'SUCCESS':
            if json_obj['size'] != len(json_obj['param']):
                print 'Client invalid parameter marshalling from server'
                return None, 'Return parameter checksum failure'

            ret_param_list = jsonpickle.decode(json_obj['param'])

            # return
            if isinstance(ret_param_list[0], numbers.Number) and (isinstance(ret_param_list[1], str) or isinstance(ret_param_list[1], unicode)):
                return ret_param_list, json_obj['status']
            else:
                return None, 'Invalid return value types'
        else:
            return None, '' + json_obj['status'] + ': An error occurred at the remote server'
