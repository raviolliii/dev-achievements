from dev_achievements.achievements import *
from dev_achievements.utilities.utils import load_store, save_completed


class AchievementTree:
    """ Tree of Achievements with dependencies as edges.

    Attributes:
        nodes (list[Achievement]): all Achievements
        queue (list[Achievement]): list of unlockable Achievements
    """
    def __init__(self):
        self._init_nodes()
    
    def _init_nodes(self):
        """ Creates list of all Achievements according to their unlocked
        state. Each one prints its unlock message and saves to the store
        upon being unlocked.
        """
        unlocked_ach = load_store(field='unlocked')

        def _create_node(ach):
            # helper to create achievement with unlocked state and handler
            unlocked = ach.__name__ in unlocked_ach
            save_ach = lambda: save_completed(ach.__name__)
            return ach(unlocked=unlocked, on_unlock=save_ach)
        
        self.nodes = [_create_node(a) for a in Achievement.subclasses()]
        # set node dependencies as references to initialized nodes
        for node in self.nodes:
            node.dependencies = [self.nodes[d.uid] for d in node.dependencies]
        return
    
    @property
    def queue(self):
        """ Returns a list of unlockable Achievements.
        An Achievement is unlockable if it's still locked, and all its
        dependencies are unlocked.

        Returns:
            list: All unlockable Achievements
        """
        def _is_unlockable(node):
            # helper to determine if given node is unlockable
            par_unlocked = all([p.unlocked for p in node.dependencies])
            is_locked = not node.unlocked
            return par_unlocked and is_locked
        # filter nodes to unlockable ones
        return [n for n in self.nodes if _is_unlockable(n)]
