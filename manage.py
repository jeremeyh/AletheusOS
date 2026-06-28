"""
CardHawk OS™
Developer CLI
"""

import argparse

from core.bootstrap import bootstrap


def cmd_boot(args):
    bootstrap.boot()


def cmd_replay(args):
    from intelligence.replay.replay_engine import replay_engine

    bootstrap.boot()

    count = replay_engine.replay()

    print(f"\nReplay complete ({count} events).")


def cmd_trace(args):
    from diagnostics.execution_trace import trace

    trace()


def cmd_health(args):
    from core.health import health

    bootstrap.boot()

    print(health.report())


parser = argparse.ArgumentParser(prog="manage.py")

sub = parser.add_subparsers(dest="command")

sub.add_parser("boot").set_defaults(func=cmd_boot)
sub.add_parser("replay").set_defaults(func=cmd_replay)
sub.add_parser("trace").set_defaults(func=cmd_trace)
sub.add_parser("health").set_defaults(func=cmd_health)

args = parser.parse_args()

if hasattr(args, "func"):
    args.func(args)
else:
    parser.print_help()

def cmd_status(args):

    from kernel.runtime import kernel

    kernel.boot()

    from pprint import pprint

    pprint(kernel.status())

sub.add_parser("status").set_defaults(func=cmd_status)
