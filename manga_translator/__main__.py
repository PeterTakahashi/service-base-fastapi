import asyncio
import logging
from argparse import Namespace

from manga_translator import Config
from manga_translator.args import parser, reparse
from .manga_translator import (
    set_main_logger
)
from .args import parser
from .utils import (
    init_logging,
    get_logger,
    set_log_level,
)

# TODO: Dynamic imports to reduce ram usage in web(-server) mode. Will require dealing with args.py imports.

async def dispatch(args: Namespace):
    args_dict = vars(args)

    if args.mode == 'shared':
        from manga_translator.mode.share import MangaShare
        translator = MangaShare(args_dict)
        await translator.listen(args_dict)
    elif args.mode == 'config-help':
        import json
        config = Config.schema()
        print(json.dumps(config, indent=2))

if __name__ == '__main__':
    args = None
    init_logging()
    try:
        args, unknown = parser.parse_known_args()
        args = Namespace(**{**vars(args), **vars(reparse(unknown))})
        set_log_level(level=logging.DEBUG if args.verbose else logging.INFO)
        logger = get_logger(args.mode)
        set_main_logger(logger)
        if args.mode != 'web':
            logger.debug(args)

        asyncio.run(dispatch(args))
    except KeyboardInterrupt:
        if not args or args.mode != 'web':
            print()
    except Exception as e:
        logger.error(f'{e.__class__.__name__}: {e}',
                     exc_info=e if args and args.verbose else None)
