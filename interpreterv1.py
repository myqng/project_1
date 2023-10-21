from brewparse import parse_program
from intbase import InterpreterBase

class Interpreter(InterpreterBase):
    def __init__(self, console_output = True, inp = None, trace_output = False):
        super().__init__(console_output, inp)
        self.int_dict = {} # for storing variable assignments
    
    def run(self, program):
        ast = parse_program(program)
        main_node = ast.dict['functions'][0]
        print(main_node)
        if (main_node.dict['name'] != 'main'):
            super().error(2, 'No main() function was found')
        else: self.run_func(main_node)
        print(self.int_dict)

    def run_func(self, func_node):
        # create a function that loops through all statements
        statement_list = func_node.dict['statements']
        for statement in statement_list:
            self.run_statement(statement)
        #return statement_list

    def run_statement(self, statement_node):
        if (self.is_assignment(statement_node)):
            self.do_assignment(statement_node)
        else:
            self.do_func_call(statement_node)

    def is_assignment(self, statement_node):
        if (statement_node.elem_type == '='):
            return True
        else: return False

    def do_assignment(self, statement_node):
        var = statement_node.dict['name']
        # print(var)
        expression = statement_node.dict['expression']
        expression_result = self.eval_expression(expression)
        self.int_dict[var] = expression_result
        # put function here on handling expression
        # assign result of expression to var
    
    def eval_expression(self, expression_node):
        # print(expression_node.elem_type)
        if (self.is_value(expression_node) or self.is_var(expression_node)):
            return self.get_value(expression_node) # returns value
        elif (self.is_binary_op(expression_node)):
            return self.eval_binary_op(expression_node)
    
    def is_value(self, expression_node):
        if (expression_node.elem_type == 'int' or expression_node.elem_type == 'string'):
            return True
        
    def get_value(self, node):
        if (self.is_value(node)):
            return(node.dict['val'])
        elif (self.is_var(node)):
            var = node.dict['name']
            if (var in self.int_dict):
                return self.int_dict.get(var)
            else:
                super().error(2, 'Variable ' + var + ' not found')
    
    def get_value_of_var(self, variable):
        if (variable in self.int_dict):
            return self.int_dict.get(variable)
        else:
            super().error(2, 'Variable ' + variable + ' not found')
        
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

        # print('op1: ' + str(op1))
        op1_val = self.get_value(op1)

        # if (self.is_value(op1) or self.is_var(op1)):
        #     op1_val = self.get_value(op1)
        #     if (self.is_value(op2) or self.is_var(op2)):
        #         op2_val = self.get_value(op2)
        #         print('operation reveal! : ' + str(self.do_operation(operation, op1_val, op2_val)))
        #         return self.do_operation(operation, op1_val, op2_val)
        #     elif (self.is_binary_op(op2)):
        #         op2_val = self.eval_binary_op(op2)
        #         return self.do_operation(operation, op1_val, op2_val)
        # elif (self.is_binary_op(op1)): 
        #     op1_val = self.eval_binary_op(op1)
        #     if (self.is_value(op2) or self.is_var(op2)):
        #         op2_val = self.get_value(op2)
        #         print('operation reveal! : ' + str(self.do_operation(operation, op1_val, op2_val)))
        #         return self.do_operation(operation, op1_val, op2_val)
        #     elif (self.is_binary_op(op2)):
        #         op2_val = self.eval_binary_op(op2)
        #         return self.do_operation(operation, op1_val, op2_val)
        
        if (self.is_value(op1) or self.is_var(op1)):
            op1_val = self.get_value(op1)
        elif (self.is_binary_op(op1)):
            op1_val = self.eval_binary_op(op1)
            
        if (self.is_value(op2) or self.is_var(op2)):
                op2_val = self.get_value(op2)
                print('operation reveal! : ' + str(self.do_operation(operation, op1_val, op2_val)))
                return self.do_operation(operation, op1_val, op2_val)
        elif (self.is_binary_op(op2)):
                op2_val = self.eval_binary_op(op2)
                return self.do_operation(operation, op1_val, op2_val)

        # print(op1_val)
        # print('op2: ' + str(op2))
    
    def do_operation(self, operation, op1, op2):
        if (operation == '+'):
            return op1 + op2
        elif (operation == '-'):
            return op1 - op2

    def do_func_call(self, statement_node):
        func = statement_node.dict['name']


def main():
    #all programs will be provided to your interpreter as a python string,
    # just as shown here.
    program_source = """func main() {
        x = 5 + 6;
        print("The sum is: ", x);
    }
    """

    program_source2 = """func main() {
        x = 5;
        y = 6;
        z = "tester";
        x = z;
    }
    """

    program_source3 = """func main() {
        y = 10;
        x  = 1 + (10 + (9 - y));
    }
    """
    
    # this is how you use our parser to parse a valid Brewin program into 
    # an AST:

    i.run(program_source3)
    #print(parse_program(program_source3))

    '''
    print(parsed_program) # elem_type: program
    # program: functions: [func: name: main, args: [], statements: [=: name: x, expression: [+: op1: [int: val: 5], op2: [int: val: 6]], fcall: name: print, args: [string: val: The sum is: , var: name: x]]]
    
    print(parsed_program.dict["functions"][0]) # elem_type: func
    # func: name: main, args: [], statements: [=: name: x, expression: [+: op1: [int: val: 5], op2: [int: val: 6]], fcall: name: print, args: [string: val: The sum is: , var: name: x]]
    
    print(parsed_program.dict["functions"][0].dict["name"])
    # main
    
    print(parsed_program.dict["functions"][0].dict["statements"])
    # returns list of statements

    print(parsed_program.dict["functions"][0].dict["statements"][0]) # elem_type: =
    # =: name: x, expression: [+: op1: [int: val: 5], op2: [int: val: 6]]

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["name"])
    # x

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["expression"]) # elem_type: +
    # +: op1: [int: val: 5], op2: [int: val: 6]

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["expression"].dict["op1"]) # elem_type: int (this is a value node)
    # int: val: 5

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["expression"].dict["op1"].dict["val"]) # value nodes only hold 'val'
    # 5

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["expression"].dict["op2"]) # elem_type: int (this is a value node)
    # int: val: 6

    print(parsed_program.dict["functions"][0].dict["statements"][0].dict["expression"].dict["op2"].dict["val"])
    # 6

    print(parsed_program.dict["functions"][0].dict["statements"][1].elem_type) # elem_type: fcall
    # fcall: name: print, args: [string: val: The sum is: , var: name: x]

    print(parsed_program.dict["functions"][0].dict["statements"][1].dict["name"])
    # print

    print(parsed_program.dict["functions"][0].dict["statements"][1].dict["args"][0]) # elem_type: string (this is a value node)
    # string: val: The sum is: 

    print(parsed_program.dict["functions"][0].dict["statements"][1].dict["args"][0].dict["val"])  # value nodes only hold one key, 'val'
    # The sum is:

    print(parsed_program.dict["functions"][0].dict["statements"][1].dict["args"][1]) # elem_type: var
    # var: name: x

    print(parsed_program.dict["functions"][0].dict["statements"][1].dict["args"][1].dict["name"]) # var nodes only hold one key, 'name'
    # x
    '''


i = Interpreter()
main()