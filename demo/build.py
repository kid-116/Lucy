import os
from pathlib import Path
import subprocess
import re

WAIT_UNIT = 'ms'
EXEC_WAIT_BEFORE_ENTER = 500  # ms
EXEC_WAIT_AFTER_ENTER = 1000 * 5  # 5ms

ROOT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = 'out'

TAPE_EXT = 'tape'
TMP_EXT = 'tmp'

EXEC_CMD = 'Exec'
CLEAR_CMD = 'Clear'
WAIT_CMD = 'Sleep'


def transform(line):
    assert line.startswith(EXEC_CMD)
    cmd = re.search('^Exec[ \t]*"(.*)"$', line).group(1)
    return f"""Type "{cmd}"
{WAIT_CMD} {EXEC_WAIT_BEFORE_ENTER}{WAIT_UNIT}
Enter
{WAIT_CMD} {EXEC_WAIT_AFTER_ENTER}{WAIT_UNIT}
"""


def main():
    for entry in os.listdir(ROOT_PATH):
        if entry.endswith(f'.{TMP_EXT}.{TAPE_EXT}'):
            os.remove(ROOT_PATH / entry)
    tapes = [entry for entry in os.listdir(ROOT_PATH) if entry.endswith(f'.{TAPE_EXT}')]

    for tape in tapes:
        print(f'Building {tape} ...')
        tape_name, _ = tape.split('.')
        dest_path = ROOT_PATH / f'{tape_name}.{TMP_EXT}.{TAPE_EXT}'
        src_path = ROOT_PATH / tape
        # pylint: disable=unspecified-encoding
        with open(dest_path, 'w+') as dest:
            with open(src_path, 'r') as src:
                dest.write('Hide\n')
                dest.write('Source utils/setup.tape\n')
                dest.write('Show\n')
                dest.write("""Hide
Source utils/setup.tape
Type "clear"
Enter
Show
""")
                for line in src:
                    if line.startswith(EXEC_CMD):
                        dest.write(transform(line))
                    elif line.startswith(CLEAR_CMD):
                        dest.write("""Hide
Type "clear"
Enter
Show
""")
                    else:
                        dest.write(line)
                dest.write(f"""Hide
Source utils/teardown.tape
Type "clear"
Enter
Show
Output {OUT_DIR}/{tape_name}.gif
""")
        try:
            subprocess.check_call(['vhs', dest_path])
        except subprocess.CalledProcessError as e:
            print(f'Failed to build {tape}: {e}')


if __name__ == '__main__':
    main()
