import ast

from dev_achievements.processing.tree import AchievementTree


class Visitor(ast.NodeVisitor):
    """ Traverses the AST syntax tree and processes each node
    accordingly.

    Attributes:
        ach_tree (AchievementTree): Achievements in tree structure
    """
    def __init__(self):
        super().__init__()
        self.ach_tree = AchievementTree()
        self.table = {}
    
    def generic_visit(self, node):
        """ Processes any general AST node type, checking all 
        Achievements in queue for any unlock state changes.

        Args:
            node (ast.AST): AST syntax tree node
        """
        node_class = node.__class__
        curr = self.table.get(node_class, [])
        self.table[node_class] = curr + [node]
        # call default visit traversal on node
        super().generic_visit(node)
        return
    
    def check_achievements(self):
        """ Checks and unlocks all possible Achievements. """
        changed = True
        check_ach = lambda ach: ach.check(self.table)
        while changed:
            # check if any Achievements have been unlocked
            checks = [check_ach(a) for a in self.ach_tree.queue]
            changed = any(checks)
        return