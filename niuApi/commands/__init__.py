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

        for key, value in options.items():
            if not isinstance(value, locate(annotation)):
                if annotation == 'list':
                    options[key] = [ value ]
                else:
                    raise TypeError(f'Option {key} should be type {annotation} - type {type(value).__name__} is given')

    return getattr(mod, func)(**options)
