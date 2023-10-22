from brewparse import parse_program
from intbase import InterpreterBase
from enum import Enum

class ErrorType(Enum):
    TYPE_ERROR = 1
    NAME_ERROR = 2  # if a variable or function name can't be found
    FAULT_ERROR = 3  # used if an object reference is null and used to make a call

class Interpreter(InterpreterBase):
    def __init__(self, console_output = True, inp = None, trace_output = False):
        super().__init__(console_output, inp)
        self.int_dict = {} # for storing variable assignments
    
    def run(self, program):
        ast = parse_program(program)
        main_node = ast.dict['functions'][0]
        if (main_node.dict['name'] != 'main'):
            super().error(ErrorType.NAME_ERROR, 'No main() function was found')
        else: self.run_func(main_node) # run main func if it exists
        
    def run_func(self, func_node):
        # loops through all statements and runs each
        statement_list = func_node.dict['statements']
        for statement in statement_list:
            self.run_statement(statement)

    def run_statement(self, statement_node):
        if (self.is_assignment(statement_node)):
            self.do_assignment(statement_node)
        elif (self.is_func_call(statement_node)):
            self.do_func_call(statement_node)

    def is_assignment(self, statement_node):
        if (statement_node.elem_type == '='):
            return True
        else: return False

    def do_assignment(self, statement_node):
        var = statement_node.dict['name']
        expression = statement_node.dict['expression']
        expression_result = self.eval_expression(expression)
        self.int_dict[var] = expression_result # assigns value to var
    
    def eval_expression(self, expression_node): # returns value of expression
        if (self.is_value(expression_node) or self.is_var(expression_node)):
            return self.get_value(expression_node)
        elif (self.is_binary_op(expression_node)):
            return self.eval_binary_op(expression_node)
        elif (self.is_func_call(expression_node)):
            return self.do_func_call(expression_node)
    
    def is_value(self, expression_node):
        if (expression_node.elem_type == 'int' or expression_node.elem_type == 'string'):
            return True
        
    def get_value(self, node): # returns value of val or var
        if (self.is_value(node)):
            return(node.dict['val'])
        elif (self.is_var(node)):
            var = node.dict['name']
            if (var in self.int_dict):
                return self.int_dict.get(var)
            else:
                super().error(ErrorType.NAME_ERROR, 'Variable ' + var + ' not found')
        
    def is_var(self, expression_node):
        if (expression_node.elem_type == 'var'):
            return True
    
    def is_binary_op(self, expression_node):
        if (expression_node.elem_type == '+' or expression_node.elem_type == '-'):
            return True
    
    def eval_binary_op(self, expression_node):
        operation = expression_node.elem_type
        op1 = expression_node.dict["op1"]
        op2 = expression_node.dict["op2"]

        if (self.is_value(op1) or self.is_var(op1)):
            op1_val = self.get_value(op1)
        elif (self.is_binary_op(op1)):
            op1_val = self.eval_binary_op(op1)
        elif (self.is_func_call(op1)):
            if (op1.dict['name'] == 'print'):
                return super().error(ErrorType.TYPE_ERROR, 'Incompatible operation in expression')
            else:
                op1_val = self.do_func_call(op1)
            
        if (self.is_value(op2) or self.is_var(op2)):
                op2_val = self.get_value(op2)
                return self.do_operation(operation, op1_val, op2_val)
        elif (self.is_binary_op(op2)):
                op2_val = self.eval_binary_op(op2)
                return self.do_operation(operation, op1_val, op2_val)
        elif (self.is_func_call(op2)):
            if (op2.dict['name'] == 'print'):
                return super().error(ErrorType.TYPE_ERROR, 'Incompatible operation in expression')
            else:
                op2_val = self.do_func_call(op2)
                return self.do_operation(operation, op1_val, op2_val)
    
    def do_operation(self, operation, op1, op2):
        if (type(op1) != int or type(op2) != int):
            return super().error(ErrorType.TYPE_ERROR, 'Incompatible types for arithmetic operation')
        if (operation == '+'):
            return op1 + op2
        elif (operation == '-'):
            return op1 - op2
        else:
            return super().error(ErrorType.NAME_ERROR, 'Operation does not exist')
        
    def is_func_call(self, statement_node):
        if (statement_node.elem_type == 'fcall'):
            return True
        else: return False
    
    def do_func_call(self, statement_node):
        func = statement_node.dict['name']
        args = statement_node.dict['args']
        if (func == 'print'):
            output = ''
            for arg in args:
                if (self.is_value(arg)):
                    output = output + str(self.get_value(arg))
                elif (self.is_var(arg)):
                    output = output + str(self.get_value(arg))
                elif (self.is_binary_op(arg)):
                    output = output + str(self.eval_binary_op(arg))
                else:
                    return super().error(ErrorType.TYPE_ERROR, 'Invalid argument passed in')
            super().output(output)
        elif (func == 'inputi'):
            if (len(args) > 1):
                return super().error(ErrorType.NAME_ERROR, 'No inputi() function found that takes > 1 parameter')
            else:
                for arg in args:
                    if (self.is_value(arg)):
                        super().output(self.get_value(arg))
                user_input = super().get_input()
                return int(user_input)
        else:
            return super().error(ErrorType.NAME_ERROR, 'Function does not exist')

i = Interpreter()