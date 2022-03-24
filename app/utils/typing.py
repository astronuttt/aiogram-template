from typing import (
    Dict,
    Any,
    Callable,
    List,
    get_type_hints,
    get_origin,
    Union,
    get_args,
)
from collections import Mapping
import re


def type_cast(node: str, node_type):
    """type cast handler's arguments based on type hints"""

    if node_type is None or node is None:
        return node
    if isinstance(node, Mapping):
        return node_type(**node)
    if get_origin(node_type) is Union:
        nullable = False
        for union_type in get_args(node_type):
            if union_type is type(None):
                nullable = True
                continue
            try:
                return union_type(node)
            except ValueError:
                continue
        if nullable:
            return None
    return node_type(node)


def extract_vars_from_callback_data(
    query_data: List[str], handler: Callable
) -> Dict[str, Any]:
    """extract variables from inline keyboard's callback_data"""
    args = get_type_hints(handler)  # get type hints from handler arguments
    return {
        cmd[0]: type_cast(cmd[1], args.get(cmd[0]))
        for cmd in (cmd.split("=") for cmd in query_data if re.match(r"(.*)=(.*)", cmd))
        if cmd[0] in args
    }


def get_handler_partial_args(data: Dict[str, str], handler: Callable) -> Dict[str, Any]:
    """get type hints from callable and convert the data to the desired type"""
    args = get_type_hints(handler)
    return {
        key: type_cast(val, args.get(key)) for key, val in data.items() if key in args
    }
