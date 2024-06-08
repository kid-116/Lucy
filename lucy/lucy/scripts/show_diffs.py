import termcolor

from lucy.ops.testing import DiffOps


def main():
    tests = [('1 2 3', '1 2 3'), ('1 2', '1 2 3'), ('2 3', '1 2 3'), ('2 3\n1', '2 3'),
             ('2 3', '2 3\n1'), ('1 2 3', '1 2 4'), ('1 2 3', '1 2'), ('1 3 4 2', '2 3 1')]
    for test in tests:
        in_txt, truth_txt = test
        print(termcolor.colored('Input:', 'black', 'on_white'))
        print(in_txt)
        print(termcolor.colored('Truth:', 'white', 'on_green'))
        print(truth_txt)
        print(termcolor.colored('Diff:', 'white', 'on_yellow'))
        DiffOps(in_txt, truth_txt).print()
        print()


if __name__ == '__main__':
    main()
