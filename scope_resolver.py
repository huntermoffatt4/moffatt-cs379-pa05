"""
PA 5: The Scope Resolver -- starter.

Complete resolve_name below. See the assignment, Part B,
for the full requirements.
"""

from typing import List

from symtable import Environment, SemanticError


def resolve_name(
    name: str,
    current_env: Environment,
    call_stack: List[Environment],
    mode: str,
) -> int:
    """
    Return the declaration line `name` resolves to.

    mode == "static": climb current_env.parent links (ignore call_stack).
    mode == "dynamic": search call_stack from most-recent (index -1)
        to oldest (index 0), checking each caller's OWN locally-defined
        names only (not their parents), falling back to the global
        (outermost lexical) environment if not found on the stack.
    Any other mode raises ValueError. Raise SemanticError if `name`
    cannot be resolved under the requested mode.
    """
    # Error for when mode is not static or dynamic
    if mode not in ("static", "dynamic"):
        raise ValueError("must be 'static' or 'dynamic'")

    # Static; uses PA4 parent chain
    elif mode == "static":
        return current_env.resolve(name)

    # Dynamic; Caller stack for most recent caller
    for env in reversed(call_stack):
        if name in env._names:
            return env._names[name]

    # Global; fall back in case no caller has the variable
    global_env = current_env
    while global_env.parent is not None:
        global_env = global_env.parent

    return global_env.resolve(name)