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
        return f'Achievement Unlocked: {self.title}'

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

# file io
# modules
# exceptions
# type hints


class SampleAchievement(Achievement):
    """ Sample Achievement for reference """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'SAMPLE'
    
    def _check_condition(self, nodes):
        """ Check something """
        return False


class HelloWorldAchievement(Achievement):
    """ Unlocks on printing Hello World """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Hello Hello!'
        self.dependencies = []
    
    def _check_condition(self, nodes):
        """ Checks for print call with "hello world" """
        for call in nodes.get(ast.Call, []):
            # has to call "print" function
            if call.func.id != print.__name__:
                continue
            # has to have at least 1 str literal (constant) argument
            if not len(call.args):
                continue
            arg = call.args[0]
            is_str = isinstance(arg, ast.Constant) and type(arg.value) == str
            # check "hello world" in first arg
            if is_str and 'hello world' in arg.value.lower():
                return True
        return False


class AssignAchievement(Achievement):
    """ Unlocks on variable assignment """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Variables!'
    
    def _check_condition(self, nodes):
        """ Checks for assignment operator """
        return bool(ast.Assign in nodes)


class MathOperatorsAchievement(Achievement):
    """ Unlocks on using any math (non binary) operator """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Operators!'
    
    def _check_condition(self, nodes):
        """ Checks for any non-binary operator """
        ops = [ast.Add, ast.Sub, ast.Mult, ast.Div,
               ast.FloorDiv, ast.Mod, ast.Pow, ast.MatMult]
        return any([o in nodes for o in ops])


class BitwiseOperatorsAchievement(Achievement):
    """ Unlocks on using any bitwise operators """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Bitwise!'
        self.dependencies = [MathOperatorsAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for any bitwise operators """
        ops = [ast.LShift, ast.RShift, ast.BitOr,
               ast.BitAnd, ast.BitXor, ast.Invert]
        return any([o in nodes for o in ops])


class ConditionalAchievement(Achievement):
    """ Unlocks on using if statements """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'If statements!'
    
    def _check_condition(self, nodes):
        """ Checks for if statements (regular and ternary) """
        reg = bool(ast.If in nodes)
        tern = bool(ast.IfExp in nodes)
        return reg or tern


class LoopsAchievement(Achievement):
    """ Unlocks on loops (for and while) """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Loops!'
        self.dependencies = [AssignAchievement, ConditionalAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for loop keywords """
        has_for = bool(ast.For in nodes)
        has_while = bool(ast.While in nodes)
        return has_for or has_while


class ComprehensionsAchievement(Achievement):
    """ Unlocks on any form of comprehension (list, set, etc.) """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Comprehensions!'
        self.dependencies = [LoopsAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for any form of comprehension """
        comps = [ast.ListComp, ast.SetComp, ast.GeneratorExp, ast.DictComp]
        return any([c in nodes for c in comps])


class PassAchievement(Achievement):
    """ Unlocks on using pass """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Pass!'
        self.dependencies = [LoopsAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for pass keyword """
        return bool(ast.Pass in nodes)


class FunctionAchievement(Achievement):
    """ Unlocks on defining and calling a function """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Functions!'
        self.dependencies = [ConditionalAchievement, LoopsAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for user defined function calls """
        fn_defs = nodes.get(ast.FunctionDef, [])
        fn_calls = nodes.get(ast.Call, [])
        # unique names of functions defined/called
        def_names = set([fn.name for fn in fn_defs])
        call_names = set([c.func.id for c in fn_calls])
        # at least one function must be defined and called
        return len(def_names & call_names) > 0


class LambdaAchievement(Achievement):
    """ Unlocks on using lambda functions """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Lambdas!'
        self.dependencies = [FunctionAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for lambda functions """
        return bool(ast.Lambda in nodes)


class ListAchievement(Achievement):
    """ Unlocks on using lists """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Lists!'
    
    def _check_condition(self, nodes):
        """ Checks for list data type """
        return bool(ast.List in nodes)


class DictAchievement(Achievement):
    """ Unlocks on using a dict """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Dictionaries!'
    
    def _check_condition(self, nodes):
        """ Checks for dict data type """
        return bool(ast.Dict in nodes)


class ClassAchievement(Achievement):
    """ Unlocks on declaring and creating an instance of a class """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'Classes!'
        self.dependencies = [FunctionAchievement]
    
    def _check_condition(self, nodes):
        """ Checks for creating a class and creating an instance """
        cls_defs = nodes.get(ast.ClassDef, [])
        cls_calls = nodes.get(ast.Call, [])
        # unique names of functions defined/called
        cls_names = set([fn.name for fn in cls_defs])
        call_names = set([c.func.id for c in cls_calls])
        # at least one function must be defined and called
        return len(cls_names & call_names) > 0

