import subprocess
import re

# Якщо виконання code вклалося у встановлений ліміт часу
# і закінчилося без винятку, або з винятком "new Error('OK')",
# виконання коду вважається успішним.
# у іншому випадку виконная вважається хибним.
# 
# В разі успішного виконная функція поверте рядок, якй починається з 'OK'.
# В разі хибного виконная функція поверте рядок, якй не починається з 'OK'


def exec(code, timeout):
    try:
        # Виконуємо node з кодом через stdin
        result = subprocess.run(
            ['node'],
            input=code,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return "OK. " + result.stdout
    except subprocess.TimeoutExpired:
        return "Перевищений ліміт часу."
    except subprocess.CalledProcessError as e:
        reOK =    r'new\s+Error\s*\(\s*[\'\"]OK'
        reWrong = r'new\s+Error\s*\(\s*[\'\"]Wrong'
        if re.search(reOK, e.stderr):
            return "OK"
        if re.search(reWrong, e.stderr):
            return "Wrong"
        return "Error. " + e.stderr
    except FileNotFoundError:
        return "Node.js не встановлений або не доданий до PATH."

