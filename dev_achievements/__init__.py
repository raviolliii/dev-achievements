import ast
import os
import sys

from dev_achievements.processing.visitor import Visitor
from dev_achievements.utilities.utils import bordered


# package version
__version__ = '1.0.2'


def process_tree(tree):
    """ Creates an AST Node Visitor to process the built
    syntax tree.

    Args:
        tree (ast.AST): AST syntax tree
    """
    v = Visitor()
    v.visit(tree)
    unlocked = v.check_achievements()
    if unlocked:
        text = '\n'.join(a.unlock_message for a in unlocked)
        print('\n' + bordered(text) + '\n')
    return


def build_tree(file_path):
    """ Creates an AST syntax tree from the source file.

    Args:
        file_path (str): path of source file
    
    Returns:
        ast.AST: Root of syntax tree
    """
    tree = None
    with open(file_path, 'r') as file:
        tree = ast.parse(file.read())
    return tree


def process_file(file_path):
    """ Builds an AST syntax tree and visits each node to 
    process for Achievements.

    Args:
        file_path (str): path of file
    """
    tree = build_tree(file_path)
    process_tree(tree)
    return


# run the whole Achievement process on package import
# if the passed script path exists
if __name__ != '__main__':
    if len(sys.argv) > 0 and os.path.isfile(sys.argv[0]):
        process_file(sys.argv[0])
