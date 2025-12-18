from app.executors import cs

TEMPLATE = """using System;
class Program {{
    static void Main(string[] args) {{  
    {0}
    }}
}}
"""
timeout = 20

def test_cs_success():
    code = """
       Console.WriteLine(111);
    """
    code = TEMPLATE.format(code)
    res = cs.exec(code, timeout)
    assert res.startswith('OK')

def test_cs_wrong():
    code = """
       throw new System.Exception("Wrong");
    """
    code = TEMPLATE.format(code)
    res = cs.exec(code, timeout)
    assert res.startswith('Wrong')

def test_cs_error():
    code = """
       ConsoleZ.WriteLine(111);
    """
    code = TEMPLATE.format(code)
    res = cs.exec(code, timeout)
    assert res.startswith('Error')

def test_cs_overtime():
    code = """
       while (true) Console.WriteLine(111);
    """
    res = cs.exec(code, 0.5)
    code = TEMPLATE.format(code)
    assert res.startswith('Перевищений')
