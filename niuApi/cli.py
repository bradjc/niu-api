"""CLI Script for NIU API
"""

from niuApi.arg import get_args
from niuApi.commands import dispatch
from niuApi.exceptions import NIURequestError

def run():
    """CLI entrypoint

    Returns:
        int: depending on errors
    """

    args = get_args()
    
    try:
        print(dispatch(args.action, args.options))
    except TypeError as exc:
        print(exc)
        return 3
    except NIURequestError as exc:
        print(exc)
        return 2

    return 0
