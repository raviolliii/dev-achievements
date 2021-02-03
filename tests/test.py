import ast
import itertools
import os
import unittest

from dev_achievements.achievements import *


# some constants
SAMPLE_SRCS_DIR = 'tests/samples/{valid}/{ach}.py'
VALIDITY_DIR_NAMES = ['valid', 'invalid']
CASE_DELIM = '>> CASE'

ALL_ACHIEVEMENTS = Achievement.subclasses()


class TestAchievements(unittest.TestCase):
    """ Checks all Achievements using sample source code
    
    Unit tests are created and set dynamically, based on Achievements
    with written sample source code (in tests/samples directory).
    """
    pass


def _build_table(src):
    """ Builds AST tree table from given source.

    Args:
        src (str): source code
    
    Returns:
        dict: table of ast.AST nodes in tree
    """
    table = {}
    tree = ast.parse(src)
    for node in ast.walk(tree):
        curr = table.get(node.__class__, [])
        table[node.__class__] = curr + [node]
    return table


def _read_file(file_path):
    """ Reads returns file contents.

    Args:
        file_path (str): path of file
    
    Returns:
        str: file contents
    """
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return ''.join(lines)


def _parse_sample_src(src):
    """ Splits sample source string based on CASE_DELIM.

    Args:
        src (str): sample source code 
    
    Returns:
        list: sample source split by test case
    """
    cases = src.split(CASE_DELIM)
    if len(cases) > 1:
        return cases[1:]
    return cases


def create_achievement_test(ach, cases, exp_result):
    """ Creates a unit test out of the source cases.

    The Achievement's _check_condition method is called on each case
    given (as a subtest), and compared against the expected result.

    Args:
        ach (Achievement): Achievement for test
        cases (list): sample source cases
        exp_result (bool): expected _check_condition result
    
    Returns:
        function: created unit test
    """
    def _test(self):
        for i, case in enumerate(cases):
            nodes = _build_table(case)
            res = ach()._check_condition(nodes)
            with self.subTest(case=i):
                self.assertEqual(res, exp_result)
    return _test


# dynamically create and set unit tests for TestAchievements

# combinations of Achievement names and valid/invalid sources
v_ach_combos = itertools.product(VALIDITY_DIR_NAMES, ALL_ACHIEVEMENTS)
for valid, ach in v_ach_combos:
    file_path = SAMPLE_SRCS_DIR.format(valid=valid, ach=ach.__name__)
    if not os.path.isfile(file_path):
        continue
    # get all cases in source file
    sample_src = _read_file(file_path)
    cases = _parse_sample_src(sample_src)
    exp_result = valid == 'valid'
    # create and set unit test method
    test_method = create_achievement_test(ach, cases, exp_result)
    test_method.__name__ = f'test_{ach.__name__}_{valid}'
    setattr(TestAchievements, test_method.__name__, test_method)
