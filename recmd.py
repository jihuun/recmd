#!/usr/bin/env python3
import argparse
import subprocess

def execute_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr

def confirm_and_execute(command):
    """Ask for confirmation before executing the command."""
    confirmation = input(f"Do you want execute the command? [y/n]: ").strip().lower()
    if confirmation == 'y':
        print(f"executing command...")
        execute_command(command)
    else:
        print("Command execution cancelled.")

def parse_arguments():
    """Define and parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="recmd",
        description="recmd: A program that recommends shell commands based on natural language input."
    )

    # Define options and arguments
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='recmd 1.0',
        help="Show the version of the program and exit."
    )
    parser.add_argument(
        '-o', '--output',
        type=str,
        metavar='FILE',
        help="Specify an output file."
    )
    parser.add_argument(
        '-c', '--config',
        type=str,
        metavar='FILE',
        help="Specify a configuration file."
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help="Enable verbose mode for detailed output."
    )

    # Define positional argument for natural language input
    parser.add_argument(
        'query',
        type=str,
        nargs='?',
        default=None,
        help="Natural language input string to interpret."
    )

    #return parser.parse_args()
    return parser

def handle_options(args):
    """Handle parsed arguments and execute appropriate actions."""

    if args.verbose:
        print("Verbose mode enabled.")
        return True

    if args.output:
        print(f"Output will be saved to: {args.output}")
        return True

    if args.config:
        print(f"Using configuration file: {args.config}")
        return True

    if args.query:
        print(f"user's input : {args.query}")
        return True

    return False

from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

def generated_cmds(user_input):
    # FIXME: return error code and error handling with return value of generated_cmds()
    warn_msg_no_relation = "Sorry, you can ask command line related query only."
    recmd_template = """You are a shell script expert.
- You must generate a shell command which is can be ran in the terminal directly from following [User Input].
- You must answer shell command only.
- No need descriptions.
- No need markdown codeblock.
- If user's query is not related shell command line, return the string in the [Not Related Cmd] below.
\n
-----
[User Input]: {user_query}
[Not Related Cmd]: {warn_no_related}

"""
    if not user_input:
        return ""

    output = StrOutputParser()

    llm_completion_model = ChatOpenAI(
            model = "gpt-4o-mini",
            temperature=0.1,
            )

    prompt = PromptTemplate(
            template=recmd_template,
            input_variables=[
                "user_query",
                "warn_no_related",
                ]
            )

    chain = prompt | llm_completion_model | output
    result = chain.invoke({
        "user_query": user_input,
        "warn_no_related": warn_msg_no_relation,
        })

    return result


def main():
    """Main entry point of the program."""
    parser = parse_arguments()
    args = parser.parse_args()
    if not handle_options(args):
        print("ERROR: there are no inputs\n")
        parser.print_help()
        return

    cmds = generated_cmds(args.query)
    print(f"generated command: {cmds}")
    confirm_and_execute(cmds)

if __name__ == "__main__":
    main()
