import os
import importlib
import inspect
import pkgutil

from pydoc import locate

from niuApi.exceptions import NIUCommandError

def dispatch(command, options=None):
    """Dispatch function

    Args:
        command (str): module.function to execute
        options (dict, optional): arguments for further module execution. Defaults to None.

    Raises:
        TypeError: if option value(s) doesn't match with function annotations

    Returns:
        str: return value of executed function
    """

    try:
        module = command.split('.')[0]
        func = command.split('.')[1]
        mod = importlib.import_module(f'niuApi.commands.{module}')
    except IndexError or ModuleNotFoundError:
        modules = pkgutil.iter_modules([os.path.dirname(__file__)])
        for pkg in modules:
            print_help(importlib.import_module(f'niuApi.commands.{pkg.name}'), pkg.name, options.get('help', True))
        raise NIUCommandError("Module doesn't exist")

    # check options
    try:
        test_function = inspect.signature(getattr(mod, func))
        for parameter in test_function.parameters.keys():
            annotation = test_function.parameters[parameter].annotation.__name__
            if annotation == '_empty':
                continue

            opt = options.get(parameter, False)
            if opt:
                if not isinstance(opt, locate(annotation)):
                    if annotation == 'list':
                        options[parameter] = [ opt ]
                    else:
                        raise TypeError(f'Option {parameter} should be type {annotation} - type {type(opt).__name__} is given')

            return getattr(mod, func)(**options)
    except AttributeError:
        print_help(mod, module, options.get('help', True))
        raise NIUCommandError("Function doesn't exist")

def print_help(mod, mod_name, help=True):
    """Print help messages for functions

    Args:
        mod (object): imported module 
        mod_name (str): module name
        help (bool, optional): Print help message of modules. Defaults to True.
    """

    functions = inspect.getmembers(mod, inspect.isfunction)
    count = 1
    for function, data in functions:
        docs = inspect.getdoc(data).splitlines(True)
        print(f'{mod_name}.{function}:')
        if help:
            # dirty: tab before first element
            docs[0] = f'\t{docs[0]}'
            print('\t'.join(docs))
            if len(functions) > count: print('\n')
        count+= 1