"""
Many of these methods are ported or adopted from the TextMate support bundle's
(Ruby) TextMate module.
"""
import sys
import os

# Add TM supoprt path.
tm_support_path = os.path.join(os.environ["TM_SUPPORT_PATH"], "lib")
if not tm_support_path in sys.path:
    sys.path.insert(0, tm_support_path)

from dialog import menu, get_string
from tm_helpers import current_word, env_python, sh, sh_escape

def exit_discard():
    sys.exit(200)


def exit_replace_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(201)


def exit_replace_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(202)


def exit_insert_text(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(203)


def exit_insert_snippet(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(204)


def exit_show_html(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(205)


def exit_show_tool_tip(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(206)


def exit_create_new_document(out = None):
    if out:
        sys.stdout.write(out)
    sys.exit(207)

