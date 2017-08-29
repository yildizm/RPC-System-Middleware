import sys
import StringIO
from numbers import Number
from string import Template
import json
def test():
	codeblock = """
print 'huh'
if 2 != 3:\n\tprint 'Client invalid parameter marshalling from server'
	"""
	exec(codeblock)
	#return result

if __name__ == '__main__':
	'''test()'''
	code = """
def f(x):
	x = x + 1
	return x

print 'This is my output.'
	"""
	expression = 'def test():\n\tif 2 != 3: print\n\t\'Client invalid parameter marshalling from server\''
	exp = "print 4"
	codeblock = """
print 'huhuh'
if 2 != 3:
	print 'Client invalid parameter marshalling from server'
	"""
	#exec(codeblock)
	#exec(expression)
	#exec(exp)
	#test()
	#test()
	#exec(code)
	#print f(5)
	#codeX = """
#if isinstance(2, Number):\n\tprint str(2) + " is a fucking number"
	#"""
	#exec(codeX)

	# TypeCheckTemplate = Template('if isinstance($input, $type):\n\tprint str($input) + " is a fucking number"')
	# runSegment = 'message = TypeCheckTemplate.substitute(input=2, type="Number")'
	# exec(runSegment)
	# exec(message)
	with open ('add_service.json') as f:
		json_object = json.load(f)
	json_functions = json_object['functions']
	number_of_functions = len(json_functions)
	i = 0
	type_check = ""
	param_list = ['id']
	while i < number_of_functions:
		json_parameters = json_functions[i]["parameters"]
		for j in json_parameters:
			type_check_template = Template(' not isinstance($param, $type) ')
			type_check += type_check_template.substitute(param = j.items()[0][0],type=j.items()[0][1]) + 'or'
			param_list.append(j.items()[0][0])
			#print j,type(json_parameters[j])
			#index += 1
		i += 1
	print param_list
	type_check = type_check[:len(type_check)-3] +":\n\treturn None, 'Invalid input arguments''"
	print type_check
	#final_template = Template('if')
	#exec(type_check)


