"""CLI Script for NIU API
"""

from niuApi.arg import get_args
from niuApi.commands import dispatch
from niuApi.exceptions import NIUCommandError, NIURequestError
from niuApi.output import out

def run():
    """CLI entrypoint

    Returns:
        int: depending on errors
    """

    args = get_args()
    
    try:
        out(dispatch(args.action, args.options))
    except TypeError as exc:
        print(exc)
        return 3
    except NIURequestError as exc:
        print(exc)
        return 2
    except NIUCommandError as exc:
        return 4

    return 0
