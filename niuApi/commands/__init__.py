import importlib
import inspect

from pydoc import locate

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

    module = command.split('.')[0]
    func = command.split('.')[1]

    mod = importlib.import_module(f'niuApi.commands.{module}')

    # check options
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
