import importlib
import inspect

from pydoc import locate

def dispatch(command, options=None):

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
                raise TypeError(f'Option {key} should be type {annotation} - type {type(value).__name__} is given')

    return getattr(mod, func)(**options)
