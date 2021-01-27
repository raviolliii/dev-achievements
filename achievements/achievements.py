import ast
from abc import abstractmethod


# Base classes
# ------------


class Achievement:
    """ Base Achievement with common unlock and dependency fields.

    Attributes:
        unlocked (bool): unlock state
        dependencies (list[Achievements]): list of Achievements to unlock first
        on_unlock (function): callback on Achievement unlock
        unlock_message (str): pretty formatted message after being unlocked
    
    Args:
        unlocked (bool): unlock state
        on_unlock (function): Achievement unlock handler
    """
    def __init__(self, unlocked=False, on_unlock=None):
        # unlocked state and dependencies
        self._unlocked = unlocked
        self.dependencies = []
        # state change handlers
        self.on_unlock = on_unlock
    
    @property
    def unlocked(self):
        """ Get unlocked state """
        return self._unlocked

    @unlocked.setter
    def unlocked(self, status):
        """ Sets the unlocked state, and calls the event handler 
        accordingly.

        Args:
            status (bool): new unlocked state
        """
        self._unlocked = status
        if self._unlocked and callable(self.on_unlock):
            self.on_unlock()
        return

    @property
    def unlock_message(self):
        """ Gives the message to show when unlocked based on the 
        Achievement title.

        Returns:
            str: Pretty formatted unlock message
        """
        if not hasattr(self, 'title'):
            return 'Achievement Unlocked!'
        res = f'Achievement Unlocked: {self.title}'
        return res

    @abstractmethod
    def _check_condition(self, nodes):
        """ When implemented, specifies whether or not this Achievement
        should be unlocked based on the given AST node table. Must be
        implemented for every subclass of Achievement.

        Args:
            nodes (dict): table of ast.AST nodes in tree

        Returns:
            bool: True if this Achievement should be unlocked, False otherwise

        Raises:
            NotImplementedError: If not implemented in subclasses
        """
        msg = 'Must implement _check_condition method for' \
            + f' class {self.__class__.__name__}'
        raise NotImplementedError(msg)

    def check(self, nodes):
        """ Calls the _check_condition method with the given AST nodes 
        and updates the unlocked state accordingly.

        Args:
            nodes (dict): table of ast.AST nodes in tree
        
        Returns:
            bool: Unlocked state after checking condition
        """
        if not self.unlocked:
            self.unlocked = self._check_condition(nodes)
        return self.unlocked
    
    @classmethod
    def subclasses(cls):
        """ Returns a list of subclasses to Achievement """
        return cls.__subclasses__()
    
    def __init_subclass__(cls, /, **kwargs):
        """ Each subclass to this Achievement will get a UID as a class 
        variable. The UID is just sequentially generated on every subclass.

        Reference:
            https://docs.python.org/3/reference/datamodel.html#customizing-class-creation
        """
        super().__init_subclass__(**kwargs)
        cls.uid = len(Achievement.__subclasses__()) - 1

    def __repr__(self):
        """ Representation version of the Achievement """
        res = f'{self.__class__.__name__}(dependencies={self.dependencies})'
        return res

    def __str__(self):
        """ String version of the Achievement """
        ulock_str = 'unlocked' if self.unlocked else 'locked'
        res = f'Achievement {self.uid}: {self.__class__.__name__}' \
            + f' ({ulock_str})'
        return res


# All unlockable achievements
# ---------------------------

# hello world
# variables
# operations
# conditionals
# loops
# pass
# list comprehension
# functions
# lambdas
# file io
# modules
# classes
# exceptions
# type hints


class AssignAchievement(Achievement):
    """ Unlocks on variable assignment """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Variables!'
    
    def _check_condition(self, nodes):
        return bool(ast.Assign in nodes)


class ForLoopAchievement(Achievement):
    """ Unlocks on loops (for and while) """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'For Loops!'
        self.dependencies = [AssignAchievement]
    
    def _check_condition(self, nodes):
        return bool(ast.For in nodes)


class PassAchievement(Achievement):
    """ Unlocks on using pass """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Doing Nothing!'
        self.dependencies = [ForLoopAchievement]
    
    def _check_condition(self, nodes):
        return bool(ast.Pass in nodes)

