import argparse
import os
from urllib.parse import unquote

def url_decode(s):
    s = unquote(s)
    if s.startswith('file:///'):
        s = s[len('file://'):]
    return s

# Additional argparse types
def path(string):
    if not string:
        return ''
    s = url_decode(os.path.expanduser(string))
    if not os.path.exists(s):
        raise argparse.ArgumentTypeError(f'No such file or directory: "{string}"')
    return s

def file_path(string):
    if not string:
        return ''
    s = url_decode(os.path.expanduser(string))
    if not os.path.exists(s):
        raise argparse.ArgumentTypeError(f'No such file: "{string}"')
    return s

def dir_path(string):
    if not string:
        return ''
    s = url_decode(os.path.expanduser(string))
    if not os.path.exists(s):
        raise argparse.ArgumentTypeError(f'No such directory: "{string}"')
    return s

class HelpFormatter(argparse.HelpFormatter):
    INDENT_INCREMENT = 2
    MAX_HELP_POSITION = 24
    WIDTH = None

    def __init__(self, prog: str, indent_increment: int = 2, max_help_position: int = 24, width: int = None):
        super().__init__(prog, self.INDENT_INCREMENT, self.MAX_HELP_POSITION, self.WIDTH)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        if action.option_strings:

            # if the Optional doesn't take a value, format is:
            #    -s, --long
            if action.nargs == 0:
                return ', '.join(action.option_strings)

            # if the Optional takes a value, format is:
            #    -s, --long ARGS
            else:
                default = self._get_default_metavar_for_optional(action)
                args_string = self._format_args(action, default)
                return ', '.join(action.option_strings) + ' ' + args_string
        else:
            return super()._format_action_invocation(action)

def general_parser(g_parser):
    g_parser.add_argument('-v', '--verbose', action='store_true',
                        help='Print debug info and save intermediate images in result folder')
    g_parser.add_argument('--attempts', default=0, type=int,
                        help='Retry attempts on encountered error. -1 means infinite times.')
    g_parser.add_argument('--ignore-errors', action='store_true', help='Skip image on encountered error.')
    g_parser.add_argument('--model-dir', default=None, type=dir_path,
                        help='Model directory (by default ./models in project root)')
    g = g_parser.add_mutually_exclusive_group()
    g.add_argument('--use-gpu', action='store_true', help='Turn on/off gpu (auto switch between mps and cuda)')
    g.add_argument('--use-gpu-limited', action='store_true', help='Turn on/off gpu (excluding offline translator)')
    g_parser.add_argument('--font-path', default='', type=file_path, help='Path to font file')
    g_parser.add_argument('--pre-dict', default=None, type=file_path, help='Path to the pre-translation dictionary file')
    g_parser.add_argument('--post-dict', default=None, type=file_path,
                        help='Path to the post-translation dictionary file')
    g_parser.add_argument('--kernel-size', default=3, type=int,
                        help='Set the convolution kernel size of the text erasure area to completely clean up text residues')



def reparse(arr: list):
    p = argparse.ArgumentParser(prog='manga_translator',
                                     description='Seamlessly translate mangas into a chosen language',
                                     formatter_class=HelpFormatter)
    general_parser(p)
    return p.parse_args(arr)

parser = argparse.ArgumentParser(prog='manga_translator', description='Seamlessly translate mangas into a chosen language', formatter_class=HelpFormatter)
general_parser(parser)
subparsers = parser.add_subparsers(dest='mode', required=True, help='Mode of operation')

# API mode
parser_api = subparsers.add_parser('shared', help='Run in API mode')
parser_api.add_argument('--host', default='127.0.0.1', type=str, help='Host for API service')
parser_api.add_argument('--port', default=5003, type=int, help='Port for API service')
parser_api.add_argument('--nonce', default=os.getenv('MT_WEB_NONCE', ''), type=str, help='Nonce for securing internal API server communication')
parser_api.add_argument("--report", default=None,type=str, help='reports to server to register instance')
parser_api.add_argument('--models-ttl', default='0', type=int, help='models TTL in memory in seconds')

subparsers.add_parser('config-help', help='Print help information for config file')
