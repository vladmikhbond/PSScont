import subprocess
import tempfile
import os
import re
import shutil
import threading
from pathlib import Path

# Виконує C# код, повертає рядки подібно до js.exec/py.exec

TEMPLATE_DIR = Path(__file__).parent / '.cs_template'
TEMPLATE_LOCK = threading.Lock()


def ensure_template():
    """Створює один раз шаблонний проєкт .NET і виконує restore/build для кешування залежностей."""
    if TEMPLATE_DIR.exists():
        return
    with TEMPLATE_LOCK:
        if TEMPLATE_DIR.exists():
            return
        TEMPLATE_DIR.mkdir(parents=True, exist_ok=True)
        # Ініціалізуємо простий консольний проект у шаблонній директорії
        subprocess.run(
            ['dotnet', 'new', 'console', '--output', str(TEMPLATE_DIR), '--language', 'C#'],
            check=True,
            capture_output=True,
            text=True
        )
        # Робимо restore/build щоб заповнити кеш і зменшити час наступних запусків
        subprocess.run(
            ['dotnet', 'restore', str(TEMPLATE_DIR)],
            check=True,
            capture_output=True,
            text=True
        )
        subprocess.run(
            ['dotnet', 'build', str(TEMPLATE_DIR)],
            check=True,
            capture_output=True,
            text=True
        )


def exec(code, timeout):
    try:
        ensure_template()
        with tempfile.TemporaryDirectory() as td:
            # Копіюємо вміст шаблону в нову тимчасову директорію
            for item in TEMPLATE_DIR.iterdir():
                src = str(item)
                dst = os.path.join(td, item.name)
                if item.is_dir():
                    shutil.copytree(src, dst)
                else:
                    shutil.copy2(src, dst)

            prog_path = os.path.join(td, 'Program.cs')
            
#             # Обгортаємо код користувача у блок try/catch щоб зловити винятки і вивести їх у stderr
#             program_text = f"""using System;
# class Program {{
#     static void Main(string[] args) {{
#         try {{
# {code}
#         }} catch (Exception e) {{
#             Console.Error.WriteLine(e.ToString());
#             Environment.Exit(1);
#         }}
#     }}
# }}
# """
            with open(prog_path, 'w', encoding='utf-8') as f:
                f.write(code)

            # Запускаємо проект з тимчасової директорії
            result = subprocess.run(
                ['dotnet', 'run', '--project', td],
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            word = "Wrong. " if result.returncode else "OK. "
            return word + result.stdout
        
    except subprocess.TimeoutExpired:
        return "Перевищений ліміт часу."
    except subprocess.CalledProcessError as e:
        reOK =    r'\bOK\b'
        reWrong = r'\bWrong\b'
        # Пошук у stderr
        if re.search(reOK, e.stderr):
            return "OK"
        if re.search(reWrong, e.stderr):
            return "Wrong"
        return "Error. " + e.stderr
    except FileNotFoundError:
        return "dotnet не встановлений або не доданий до PATH."