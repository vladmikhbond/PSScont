from app.executors import py, js


def test_js_success():
    code = """
       console.log(111);
    """
    res = js.exec(code, 1)
    assert res.startswith('OK')

def test_js_wrong():
    code = """
       throw new Error('Wrong');
    """
    res = js.exec(code, 1)
    assert res.startswith('Wrong')

def test_js_error():
    code = """
       consoleZ.logZ(111);
    """
    res = js.exec(code, 1)
    assert res.startswith('Error')

def test_js_overtime():
    code = """
       while (true) console.log(111);
    """
    res = js.exec(code, 0.5)
    assert res.startswith('Перевищений')



def test_py_success():
    code = """print(111)
    """
    res = py.exec(code, 1)
    assert res.startswith('OK')
    
def test_py_wrong():
    code = """raise Exception('Wrong');
    """
    res = py.exec(code, 1)
    assert res.startswith('Wrong')

def test_py_error():
    code = """consoleZ.logZ(111)
    """
    res = py.exec(code, 1)
    assert res.startswith('Error')

def test_py_overtime():
    code = """while True: print(111)
    """
    res = py.exec(code, 0.5)
    assert res.startswith('Перевищений')

