import argparse
import dataclasses
import os
import textwrap

prog = 'logri'

input_text = argparse.ArgumentParser(add_help=False)
input_text.add_argument('--vf', '--verilog-file',
    action='extend', nargs='+', default=[],
    metavar='VERILOG_FILE', dest='verilog_file')
input_text.add_argument('-e', '--encoding', nargs=1, default='utf-8')

output_bin = argparse.ArgumentParser(add_help=False)
output_bin.add_argument('-o', '--output', nargs=1, default='logri_out.bin')

input_bin = argparse.ArgumentParser(add_help=False)
input_bin.add_argument('--bf', '--binary-file', 
    nargs=1, metavar='BINARY_FILE', dest='binary_file')

@dataclasses.dataclass
class CommandEntry:
    name: str
    help: str
    parents: list[argparse.ArgumentParser]
    _parser: argparse.ArgumentParser | None = None

    @property
    def parser(self) -> argparse.ArgumentParser:
        if self._parser is None:
            self._parser = argparse.ArgumentParser(
                prog=f'{prog} {self.name}',
                parents=self.parents)
        return self._parser

compile_entry = CommandEntry(
    'compile', 'Compile verilog to python object', [input_text, output_bin])

simulate_entry = CommandEntry(
    'simulate', 'Run simulation on compiled object', [input_bin])

command_dict: dict[str, list[argparse.ArgumentParser]] = {
    'compile': compile_entry,
    'simulate': simulate_entry,
    }


def print_general_help():
    print(f'usage: {prog} <command> [options]\n')
    print('commands:')
    command_help_format = '  {: <16}{}\n'
    for command, entry in command_dict.items():
        print(command_help_format.format(command, entry.help), end='')
    print('  help            Show help for commands')


def print_command_help(argv: list[str]) -> None:
    command = argv[0]
    if command in command_dict: 
        command_dict[command].parser.print_help()
    elif command == 'help':
        print_general_help()
    else:
        print_general_help()
        print(f'\nerror: unrecognized command: {command}')


def get_arguments(argv):
    if len(argv) < 2:
        print_general_help()
        return None

    if len(argv) == 2:
        print_command_help(argv[1:2])
        return None

    command = argv[1]
    if command in command_dict:
        args = command_dict[command].parser.parse_args(argv[2:])
        args.command = command
        return args
    elif command == 'help':
        print_command_help(argv[2:])
        return None
    else:
        print_general_help()
        print(f'\nerror: unrecognized arguments: {' '.join(argv[1:])}')
        return None


def arguments_to_task_description(args):
    print(args)
    print('Cannot generate task description according to arguments.')
    return None


def execute_task(task):
    pass
