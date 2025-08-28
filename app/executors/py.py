import subprocess


def exec(py_code, timeout):
    try:
        # Виконуємо node з кодом через stdin
        result = subprocess.run(
            ['python'],
            input=py_code,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return "OK. " + result.stdout
    except subprocess.TimeoutExpired:
        return "Перевищений ліміт часу."
    except subprocess.CalledProcessError as e:
        if e.stderr.find("Exception: OK") != -1:
            return "OK"
        if e.stderr.find("Exception: Wrong") != -1:
            return "Wrong"
        return "Error. " + e.stderr
    except FileNotFoundError:
        return "Python не встановлений або не доданий до PATH."

