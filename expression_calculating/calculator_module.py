from collections import deque
from operator import add, sub, mul, truediv


class Calculator(object):
    '''
    Class that help calculates math-expression.
    
    Instance : 
        bracket :   dict
        op :        dict
    
    Method :
        is_not_value() :        bool
        split_proc() :          string
        is_valid() :            bool
        to_postfix_proc() :     string
        calc_proc() :           float
        eval_proc() :           float or string
    '''
    bracket = {'(' : 1, ')' : 2}
    op = {'+': add, '-': sub, '*': mul, '/': truediv}

    def is_not_value(self, c):
        '''
        Determinate that it is operator or not.

        input :     charactor(one size string)
        output :    true / false
        '''
        if c in self.op: return True
        elif c in self.bracket: return True
        return False

    def split_proc(self, s):
        '''
        Result splited with each signal/number with space, 
        can handle float, negative and brackets.

        input :     infix style expression
        output :    splited infix style expression
        '''
        res, value = '', ''
        for c in s:
            if self.is_not_value(c):
                if len(value): res += value + ' '
                res += c + ' '
                value = ''
            else:
                value += c
        res += value
        return res
        
    def is_valid(self, s):
        '''
        Count brackets from expression.
        If open bracket != close_bracket, It is NOT valid expression.
        
        input :     infix style expression
        output :    true / false
        '''
        # It should find edge cases.. ex) 1+-0
        open_bracket = 0
        close_bracket = 0
        for c in s:
            if c == '(': open_bracket += 1
            elif c == ')': close_bracket += 1
        if open_bracket == close_bracket: return True
        else: return False
    
    def to_postfix_proc(self, s):
        '''
        Make it postfix style after parsing bracket and considering operator priority.
        
        input :     splited infix style expression
        output :    splited postfix style expression
        '''
        st = []
        ret = ''
        tokens = s.split()
        for tok in tokens:
            if tok in ['*', '/']:
                while st and st[-1] in ['*', '/']:
                    ret += st.pop() + ' '
                st.append(tok)
            elif tok in ['+', '-']:
                while st and st[-1] != '(':
                    ret += st.pop() + ' '
                st.append(tok)
            elif tok == '(':
                st.append(tok)
            elif tok == ')':
                while st[-1] != '(':
                    ret += st.pop() + ' '
                st.pop()
            else:
                ret += tok + ' '
        while st:
            ret += st.pop() + ' '
        return ret

    def calc_proc(self, s):
        '''
        calculates postfix style expression.
        
        input :     splited postfix style expression
        output :    calculated result
        '''
        st = []
        tokens = s.split()
        try:
            for tok in tokens:
                if tok not in self.op:
                    st.append(float(tok))
                else:
                    n1 = st.pop()
                    n2 = st.pop()
                    if tok == '/' and n1 == 0:
                        return 'NAN'
                    else:
                        st.append(self.op[tok](n2, n1))
        except Exception :
            return 'INVALID'
        return st.pop()

    def eval_proc(self, string):
        '''
        evaluates that the expression is valid or NOT and returns result.
        
        input :     infix style expression
        output :    calculated result or 'INVALID'
        '''
        if not len(string): return 'INVALID'
        if self.is_valid(string): 
            return self.calc_proc(self.to_postfix_proc(self.split_proc(string)))
        else:
            return 'INVALID'
