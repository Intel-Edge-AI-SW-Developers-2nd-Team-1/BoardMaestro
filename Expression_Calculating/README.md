## Documentation
### Description
- It does NOT require any external module.

```
    Class that help calculates math-expression.
    
    Instance : 
        bracket : dict
        op : dict
    
    Method :
        is_not_value() : bool
        split_proc() : str
        is_valid() : bool
        to_postfix_proc() : str
        calc_proc() : float
        eval_proc() : float or str
```

### Flow
For example, let expression be "(1+2*3)/4".

#### First 
- It should be splited to operate.

#### Second
- It should be converted from infix to postfix to put it to stack.
#### Third
- It is calculated in calc_proc() method.

#### Finally
- The result is 1.75.

![](/flow.png)

### Usage
- Example Code

```python
calc = Calculator()
expression = input("Enter math expression : ")
print(calc.eval_proc(expression))
```