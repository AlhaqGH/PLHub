from __future__ import annotations
from typing import Any, Dict, List, Optional, Callable

from .poh_ast import *
from .poh_parser import parse_program, ParseError


class RuntimeErrorPoh(Exception):
    """Unified runtime error for PohLang.

    All messages should already be prefixed with `[file:line N:col M]` form
    produced via Interpreter._format_err. This class is a simple marker so
    tests can assert on error types without relying on exact Python
    exception varieties.
    """
    pass


class Environment:
    def __init__(self, parent: Optional['Environment']=None, frame_type: str = "block"):
        self.parent = parent
        self.frame_type = frame_type  # 'global' | 'function' | 'block'
        self.values: Dict[str, Any] = {}

    def get(self, name: str) -> Any:
        if name in self.values:
            return self.values[name]
        if self.parent:
            return self.parent.get(name)
        raise RuntimeErrorPoh(f"Undefined variable '{name}'")

    def set(self, name: str, value: Any) -> None:
        """
        Assignment resolution rules:
        - If the variable exists in any enclosing scope, mutate the closest scope that already defines it.
        - Otherwise:
            * If we're inside a function (current frame or an ancestor function frame before hitting global), define it in the innermost function frame (i.e., local variable).
            * If no function frame found (we are at global), define globally.
        This prevents accidental mutation of globals by implicit local assignment inside functions, while still allowing
        loops/blocks inside a function to assign to locals declared in that function.
        """
        # Case 1: already defined in this frame
        if name in self.values:
            self.values[name] = value
            return
        # Case 2: exists in some parent => assign to that defining frame
        cur = self.parent
        defining_env: Optional[Environment] = None
        while cur:
            if name in cur.values:
                defining_env = cur
                break
            cur = cur.parent
        if defining_env is not None:
            defining_env.values[name] = value
            return
        # Case 3: new symbol
        if self.frame_type == 'block':
            # Always keep block-introduced names local to the block (true lexical scoping).
            self.values[name] = value
            return
        # For function or global frames: function -> local; global -> global
        if self.frame_type == 'function':
            self.values[name] = value
            return
        # global frame
        self.values[name] = value

    def define(self, name: str, value: Any) -> None:
        self.values[name] = value

    def has(self, name: str) -> bool:
        if name in self.values:
            return True
        if self.parent:
            return self.parent.has(name)
        return False


class Function:
    def __init__(self, decl: FunctionDefStmt, closure: Environment, interpret: 'Interpreter'):
        self.decl = decl
        self.closure = closure
        self.interpret = interpret

    def call(self, args: List[Any], call_node: Optional[object] = None) -> Any:
        # Populate defaults
        filled: list[Any] = []
        for i, pname in enumerate(self.decl.params):
            if i < len(args):
                filled.append(args[i])
            else:
                default_expr = self.decl.defaults[i] if i < len(self.decl.defaults) else None
                if default_expr is None:
                    def_line = getattr(self.decl, 'line', '?')
                    msg = (
                        f"Function '{self.decl.name}' defined at line {def_line} expects at least {i+1} argument(s)"
                    )
                    raise RuntimeErrorPoh(self.interpret.runtime_error(msg, node=call_node))
                # Evaluate default in closure (definition-time environment)
                try:
                    dv = self.interpret._eval(default_expr, self.closure)
                except RuntimeErrorPoh as e:
                    raise RuntimeErrorPoh(self.interpret.runtime_error(f"Error evaluating default for parameter '{pname}': {e}", node=call_node))
                filled.append(dv)
        # Too many args check
        if len(args) > len(self.decl.params):
            def_line = getattr(self.decl, 'line', '?')
            msg = (
                f"Function '{self.decl.name}' defined at line {def_line} takes at most {len(self.decl.params)} argument(s) but got {len(args)}"
            )
            raise RuntimeErrorPoh(self.interpret.runtime_error(msg, node=call_node))
        env = Environment(self.closure, frame_type='function')
        for name, val in zip(self.decl.params, filled):
            env.define(name, val)
        # push call frame
        self.interpret.call_stack.append(self.decl.name)
        # Debug enter
        if self.interpret.debug_enabled:
            # Build parameter assignment preview
            parts = []
            for p, v in zip(self.decl.params, args):
                parts.append(f"{p}={v!r}")
            call_line = getattr(call_node, 'line', getattr(self.decl, 'line', None))
            call_col = getattr(call_node, 'col', None)
            self.interpret._debug_print(call_line, call_col, f"Enter function {self.decl.name}({', '.join(parts)})")
        try:
            try:
                result = self.interpret._exec_block(self.decl.body, env)
                # Implicit None return
                if self.interpret.debug_enabled:
                    ret_line = getattr(call_node, 'line', getattr(self.decl, 'line', None))
                    ret_col = getattr(call_node, 'col', None)
                    self.interpret._debug_print(ret_line, ret_col, f"Return {result!r}")
                return result
            except _ReturnSignal as r:
                if self.interpret.debug_enabled:
                    ret_line = getattr(call_node, 'line', getattr(self.decl, 'line', None))
                    ret_col = getattr(call_node, 'col', None)
                    self.interpret._debug_print(ret_line, ret_col, f"Return {r.value!r}")
                return r.value
            return None
        finally:
            self.interpret.call_stack.pop()


class _ReturnSignal(Exception):
    def __init__(self, value: Any):
        self.value = value


class _BreakSignal(Exception):
    pass


class _ContinueSignal(Exception):
    pass


class Interpreter:
    def __init__(self, input_fn: Optional[Callable[[str], str]]=None, output_fn: Optional[Callable[[str], None]]=None):
        self.globals = Environment(frame_type='global')
        self.input_fn = input_fn or (lambda prompt: input(prompt))
        self.output_fn = output_fn or print
        self.functions: Dict[str, Function] = {}
        self.call_stack: List[str] = []  # track active function names for debugging / future error reporting
        # Module registry: module_name -> exported variables dict
        self.modules: Dict[str, Dict[str, Any]] = {}
        # Expose modules dictionary to user code for explicit access
        self.globals.define('_modules', self.modules)
        # Built-in standard library functions
        self._install_builtins()
        self.debug_enabled = False
        self.import_stack: list[str] = []
        self.loaded_files: set[str] = set()
        self.current_file: Optional[str] = None  # legacy single file tracker (kept for compatibility)
        self.file_stack: List[str] = []  # stack of filenames for nested imports / executions
        # Collect deprecation warnings for printing; also print immediately
        self.warnings: List[str] = []

    # Mutability helpers -------------------------------------------------
    class FrozenDict(dict):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        def __hash__(self):
            return hash(tuple(sorted(self.items())))
        # block mutating methods
        def _blocked(self, *a, **k):
            raise TypeError("FrozenDict is immutable")
        clear = pop = popitem = setdefault = update = __setitem__ = _blocked

    class PohList(list):
        __slots__ = ("_mutable", "_legacy", "_origin_node")
        def __init__(self, items, mutable: bool, legacy: bool, origin_node: Optional[object]):
            super().__init__(items)
            self._mutable = mutable
            self._legacy = legacy
            self._origin_node = origin_node

    class PohDict(dict):
        __slots__ = ("_mutable", "_legacy", "_origin_node")
        def __init__(self, items, mutable: bool, legacy: bool, origin_node: Optional[object]):
            super().__init__(items)
            self._mutable = mutable
            self._legacy = legacy
            self._origin_node = origin_node

    def run(self, src: str, filename: str | None = None) -> None:
        fname = filename or '<stdin>'
        self.file_stack.append(fname)
        prev = self.current_file
        self.current_file = fname
        try:
            lines = src.splitlines()
            program = parse_program(lines, filename=filename)
            self.execute(program)
        finally:
            self.current_file = prev
            self.file_stack.pop()

    def run_file(self, path: str) -> None:
        import os, difflib
        full = os.path.abspath(path)
        if full in self.import_stack:
            chain = ' -> '.join(self.import_stack + [full])
            # Requirement: "[file:line:col] Error: Circular import detected with <filename>."
            basename = os.path.basename(full)
            raise RuntimeErrorPoh(self.runtime_error(f"Error: Circular import detected with {basename}. Chain: {chain}"))
        if full in self.loaded_files:
            return
        self.import_stack.append(full)
        try:
            try:
                with open(full, 'r', encoding='utf-8') as f:
                    src = f.read()
            except FileNotFoundError:
                # Build candidate list: scan current working directory (and examples/poh) for .poh files
                cwd = os.getcwd()
                candidates: list[str] = []
                for root, _, files in os.walk(cwd):
                    for fn in files:
                        if fn.lower().endswith('.poh'):
                            candidates.append(os.path.join(root, fn))
                short_requested = os.path.basename(full)
                scored = difflib.get_close_matches(short_requested, [os.path.basename(c) for c in candidates], n=1)
                if scored:
                    suggestion = scored[0]
                    raise RuntimeErrorPoh(self.runtime_error(f"I couldn't find the file '{path}'. Did you mean '{suggestion}'?"))
                raise RuntimeErrorPoh(self.runtime_error(f"I couldn't find the file '{path}'."))
            cwd_before = os.getcwd()
            os.chdir(os.path.dirname(full) or cwd_before)
            try:
                # Parse and execute in its own module environment to avoid leaking variables
                from .poh_parser import parse_program
                prev = self.current_file
                self.current_file = full
                self.file_stack.append(full)
                try:
                    program = parse_program(src.splitlines(), filename=full)
                    module_name = os.path.splitext(os.path.basename(full))[0]
                    module_env = Environment(self.globals, frame_type='module')
                    self._execute_module(program, module_env)
                    # Export module variables (non-function values) into registry for explicit access
                    exports = {k: v for k, v in module_env.values.items() if k not in self.functions}
                    self.modules[module_name] = exports
                finally:
                    self.file_stack.pop()
                    self.current_file = prev
            finally:
                os.chdir(cwd_before)
            self.loaded_files.add(full)
        finally:
            self.import_stack.pop()

    def execute(self, program: Program) -> None:
        # first pass: collect function defs and bind as values in globals
        for st in program.statements:
            if isinstance(st, FunctionDefStmt):
                fn = Function(st, self.globals, self)
                self.functions[st.name] = fn
                # Bind as value for first-class usage
                self.globals.define(st.name, fn)
        # second pass: run top-level statements except function defs
        for st in program.statements:
            if isinstance(st, FunctionDefStmt):
                continue
            self._exec_stmt(st, self.globals)

    def _execute_module(self, program: Program, module_env: Environment) -> None:
        """Execute a parsed Program inside a dedicated module environment.
        Functions are still registered globally (so they are directly callable), but their closure
        captures the module environment, enabling per-module state without leaking module variables
        into the global namespace.
        """
        # Collect function defs with closure = module_env and bind into module scope
        for st in program.statements:
            if isinstance(st, FunctionDefStmt):
                fn = Function(st, module_env, self)
                self.functions[st.name] = fn
                module_env.define(st.name, fn)
        # Execute non-function statements inside the module scope
        for st in program.statements:
            if isinstance(st, FunctionDefStmt):
                continue
            self._exec_stmt(st, module_env)

    def _exec_block(self, stmts: List[Stmt], env: Environment) -> Any:
        # Execute until a Return is thrown or end.
        for st in stmts:
            if isinstance(st, ReturnStmt):
                val = self._eval(st.value, env) if st.value is not None else None
                raise _ReturnSignal(val)
            self._exec_stmt(st, env)
        return None

    def _log(self, msg: str) -> None:
        if self.debug_enabled:
            self.output_fn(f"[debug] {msg}")

    def _debug_prefix(self, line: Optional[int], col: Optional[int]) -> str:
        file = (self.file_stack[-1] if self.file_stack else (self.current_file or '<stdin>'))
        parts = [file]
        if line is not None:
            parts.append(f"Line {line}")
        if col is not None:
            parts.append(f"Col {col}")
        return f"[{': '.join(parts)}]"

    def _debug_print(self, line: Optional[int], col: Optional[int], message: str):
        if self.debug_enabled:
            self.output_fn(f"{self._debug_prefix(line, col)} {message}")

    def runtime_error(self, message: str, node: Optional[object] = None) -> str:
        """Return standardized runtime error string.

        Format: [filename: Line N: Col M] message
        - filename from top of file_stack (or <stdin>)
        - Always includes Line when node has line attribute
        - Includes Col when node has col attribute
        """
        file = (self.file_stack[-1] if self.file_stack else (self.current_file or '<stdin>'))
        line = getattr(node, 'line', None)
        col = getattr(node, 'col', None)
        parts = [file]
        if line is not None:
            parts.append(f"Line {line}")
        if col is not None:
            parts.append(f"Col {col}")
        prefix = f"[{': '.join(parts)}]"
        return f"{prefix} {message}"

    def runtime_warning(self, message: str, node: Optional[object] = None) -> str:
        file = (self.file_stack[-1] if self.file_stack else (self.current_file or '<stdin>'))
        line = getattr(node, 'line', None)
        col = getattr(node, 'col', None)
        parts = [file]
        if line is not None:
            parts.append(f"Line {line}")
        if col is not None:
            parts.append(f"Col {col}")
        prefix = f"[{': '.join(parts)}]"
        msg = f"{prefix} Warning: {message}"
        self.warnings.append(msg)
        # Print warning immediately for visibility
        self.output_fn(msg)
        return msg

    def _exec_stmt(self, st: Stmt, env: Environment) -> None:
        # Debug: show statement type
        if self.debug_enabled:
            line = getattr(st, 'line', None)
            col = getattr(st, 'col', None)
            self._debug_print(line, col, f"Executing: {st.__class__.__name__}")
        if isinstance(st, WriteStmt):
            val = self._eval(st.expr, env)
            self.output_fn(str(val))
        elif isinstance(st, AskStmt):
            raw = self.input_fn(f"Enter {st.name}: ")
            if st.kind == 'number':
                try:
                    env.set(st.name, int(raw.strip()))
                except Exception:
                    self._log(f"Invalid number input for {st.name}, defaulting to 0")
                    env.set(st.name, 0)
            elif st.kind == 'decimal':
                try:
                    env.set(st.name, float(raw.strip()))
                except Exception:
                    self._log(f"Invalid decimal input for {st.name}, defaulting to 0.0")
                    env.set(st.name, 0.0)
            else:
                env.set(st.name, raw)
        elif isinstance(st, SetStmt):
            value = self._eval(st.expr, env)
            env.set(st.name, value)
            if self.debug_enabled:
                line = getattr(st, 'line', None)
                col = getattr(st, 'col', None)
                self._debug_print(line, col, f"Set variable '{st.name}' = {value!r}")
        elif isinstance(st, IncStmt):
            new_val = (env.get(st.name) if env.has(st.name) else 0) + self._eval(st.amount, env)
            env.set(st.name, new_val)
            if self.debug_enabled:
                self._debug_print(getattr(st, 'line', None), getattr(st, 'col', None), f"Set variable '{st.name}' = {new_val!r}")
        elif isinstance(st, DecStmt):
            new_val = (env.get(st.name) if env.has(st.name) else 0) - self._eval(st.amount, env)
            env.set(st.name, new_val)
            if self.debug_enabled:
                self._debug_print(getattr(st, 'line', None), getattr(st, 'col', None), f"Set variable '{st.name}' = {new_val!r}")
        elif isinstance(st, IfStmt):
            if self._is_truthy(self._eval(st.condition, env)):
                try:
                    self._exec_block(st.then_body, Environment(env, frame_type='block'))
                except (_BreakSignal, _ContinueSignal):
                    pass
            else:
                if st.else_body is not None:
                    try:
                        self._exec_block(st.else_body, Environment(env, frame_type='block'))
                    except (_BreakSignal, _ContinueSignal):
                        pass
        elif isinstance(st, WhileStmt):
            while self._is_truthy(self._eval(st.condition, env)):
                try:
                    self._exec_block(st.body, Environment(env, frame_type='block'))
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    continue
        elif isinstance(st, RepeatStmt):
            iter_val = self._eval(st.count, env)
            # If numeric, repeat N times; if list, iterate elements; if dict, iterate keys
            if isinstance(iter_val, int):
                iterator = range(iter_val)
            elif isinstance(iter_val, float):
                iterator = range(int(iter_val))
            elif isinstance(iter_val, list):
                iterator = iter_val
            elif isinstance(iter_val, dict):
                iterator = list(iter_val.keys())
            else:
                try:
                    iterator = range(int(iter_val))
                except Exception:
                    iterator = []
            for current in iterator:
                try:
                    loop_env = Environment(env, frame_type='block')
                    # Provide implicit 'it' for list/dict iteration
                    if isinstance(iter_val, (list, dict)):
                        loop_env.define('it', current)
                    self._exec_block(st.body, loop_env)
                except _BreakSignal:
                    break
                except _ContinueSignal:
                    continue
        elif isinstance(st, AddToListStmt):
            target = self._eval(st.target, env)
            value = self._eval(st.value, env)
            if isinstance(target, (list, Interpreter.PohList, tuple)):
                # If it's our wrapper with mutability markers
                if isinstance(target, Interpreter.PohList):
                    if target._mutable:
                        target.append(value)
                    else:
                        # legacy allows mutation with warning
                        if target._legacy:
                            self.runtime_warning("Implicit mutable list is deprecated. Use 'mutable list' instead.", node=st)
                            target.append(value)
                        else:
                            raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
                elif isinstance(target, tuple):
                    raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
                else:
                    # plain python list (shouldn't generally happen for new forms) – assume mutable
                    target.append(value)
            else:
                raise RuntimeErrorPoh(self.runtime_error("Add to expects a list", node=st))
        elif isinstance(st, RemoveFromListStmt):
            target = self._eval(st.target, env)
            value = self._eval(st.value, env)
            if isinstance(target, (list, Interpreter.PohList, tuple)):
                if isinstance(target, Interpreter.PohList):
                    if target._mutable:
                        try:
                            target.remove(value)
                        except ValueError:
                            pass
                    else:
                        if target._legacy:
                            self.runtime_warning("Implicit mutable list is deprecated. Use 'mutable list' instead.", node=st)
                            try:
                                target.remove(value)
                            except ValueError:
                                pass
                        else:
                            raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
                elif isinstance(target, tuple):
                    raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
                else:
                    try:
                        target.remove(value)
                    except ValueError:
                        pass
            else:
                raise RuntimeErrorPoh(self.runtime_error("Remove from expects a list", node=st))
        elif isinstance(st, AddToDictStmt):
            target = self._eval(st.target, env)
            key = self._eval(st.key, env)
            value = self._eval(st.value, env)
            if isinstance(target, dict):
                if isinstance(target, Interpreter.PohDict):
                    if target._mutable:
                        target[key] = value
                    else:
                        if target._legacy:
                            self.runtime_warning("Implicit mutable dictionary is deprecated. Use 'mutable dictionary' instead.", node=st)
                            target[key] = value
                        else:
                            raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable dictionary. Did you mean \"Make a mutable dictionary ...\"?", node=st))
                else:
                    try:
                        target[key] = value
                    except TypeError:
                        # Likely FrozenDict
                        raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable dictionary. Did you mean \"Make a mutable dictionary ...\"?", node=st))
            else:
                raise RuntimeErrorPoh(self.runtime_error("Add to expects a dictionary when using key: value", node=st))
        elif isinstance(st, RemoveFromDictStmt):
            target = self._eval(st.target, env)
            key = self._eval(st.key, env)
            if isinstance(target, dict):
                if isinstance(target, Interpreter.PohDict):
                    if target._mutable:
                        target.pop(key, None)
                    else:
                        if target._legacy:
                            self.runtime_warning("Implicit mutable dictionary is deprecated. Use 'mutable dictionary' instead.", node=st)
                            target.pop(key, None)
                        else:
                            raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable dictionary. Did you mean \"Make a mutable dictionary ...\"?", node=st))
                else:
                    try:
                        target.pop(key, None)
                    except TypeError:
                        raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable dictionary. Did you mean \"Make a mutable dictionary ...\"?", node=st))
            else:
                raise RuntimeErrorPoh(self.runtime_error("Remove from expects a dictionary when key is provided", node=st))
        elif isinstance(st, SetNthItemStmt):
            container = self._eval(st.container, env)
            if not isinstance(container, (list, Interpreter.PohList, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("Set Nth item expects a list", node=st))
            # Evaluate index with friendly fallback: undefined -> non-numeric error
            try:
                idx_val = self._eval(st.index, env)
            except RuntimeErrorPoh as ex:
                msg = str(ex)
                if "Undefined variable" in msg:
                    raise RuntimeErrorPoh(self.runtime_error("Index must be a number", node=st))
                raise
            try:
                idx = int(idx_val)
            except Exception:
                raise RuntimeErrorPoh(self.runtime_error("Index must be a number", node=st))
            # 1-based index
            idx0 = idx - 1
            if idx0 < 0 or idx0 >= len(container):
                raise RuntimeErrorPoh(self.runtime_error(f"Index {idx} is out of range for the list.", node=st))
            # Mutability enforcement for PohList
            if isinstance(container, Interpreter.PohList):
                if container._mutable:
                    value = self._eval(st.value, env)
                    container[idx0] = value
                else:
                    if container._legacy:
                        self.runtime_warning("Implicit mutable list is deprecated. Use 'mutable list' instead.", node=st)
                        value = self._eval(st.value, env)
                        container[idx0] = value
                    else:
                        raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
            elif isinstance(container, tuple):
                raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
            else:
                value = self._eval(st.value, env)
                container[idx0] = value
        elif isinstance(st, RemoveLastItemStmt):
            container = self._eval(st.container, env)
            if not isinstance(container, (list, Interpreter.PohList, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("Remove last item expects a list", node=st))
            if isinstance(container, Interpreter.PohList):
                if container._mutable:
                    if container:
                        container.pop()
                else:
                    if container._legacy:
                        self.runtime_warning("Implicit mutable list is deprecated. Use 'mutable list' instead.", node=st)
                        if container:
                            container.pop()
                    else:
                        raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
            elif isinstance(container, tuple):
                raise RuntimeErrorPoh(self.runtime_error("Cannot modify immutable list. Did you mean \"Make a mutable list ...\"?", node=st))
            else:
                if container:
                    container.pop()
        elif isinstance(st, StopStmt):
            raise _BreakSignal()
        elif isinstance(st, SkipStmt):
            raise _ContinueSignal()
        elif isinstance(st, DebugStmt):
            self.debug_enabled = st.enabled
            self._log(f"Debug {'enabled' if self.debug_enabled else 'disabled'} at line {st.line}")
        elif isinstance(st, FunctionDefStmt):
            # Nested or dynamic function definition: create function capturing current env
            fn = Function(st, env, self)
            # Define in current scope for first-class usage and local calls
            env.define(st.name, fn)
            # Do not register globally to avoid leaking nested functions; callers can reference via variable
        elif isinstance(st, UseStmt):
            if st.name not in self.functions:
                # Suggest close match
                import difflib
                suggestion = difflib.get_close_matches(st.name, list(self.functions.keys()), n=1)
                hint = f" Did you mean '{suggestion[0]}'?" if suggestion else ""
                raise RuntimeErrorPoh(self.runtime_error(f"Unknown function '{st.name}'.{hint}", node=st))
            fn = self.functions[st.name]
            args = [self._eval(a, env) for a in st.args]
            fn.call(args, call_node=st)
        elif isinstance(st, CallValueStmt):
            callee = self._eval(st.callee, env)
            args = [self._eval(a, env) for a in st.args]
            if isinstance(callee, Function):
                callee.call(args, call_node=st)
            else:
                raise RuntimeErrorPoh(self.runtime_error("Target is not callable", node=st))
        elif isinstance(st, ImportStmt):
            import os
            if st.system:
                # System import: from stdlib/<name>.poh; shared global scope
                base = os.path.join(os.path.dirname(__file__), 'stdlib')
                full = os.path.abspath(os.path.join(base, f"{st.path}.poh"))
                if self.debug_enabled:
                    self.output_fn(f"[import system: {st.path}]")
                # Execute into globals (shared scope), but track circular imports
                prev_env = self.globals
                prev_file = self.current_file
                try:
                    self.run_file(full)
                except RuntimeErrorPoh as e:
                    msg = str(e)
                    if msg.startswith('['):
                        raise
                    raise RuntimeErrorPoh(self.runtime_error(msg, node=st))
                finally:
                    self.current_file = prev_file
            else:
                path = st.path
                if not os.path.isabs(path):
                    path = os.path.normpath(os.path.join(os.getcwd(), path))
                if self.debug_enabled:
                    self.output_fn(f"[import: {os.path.basename(path)}]")
                try:
                    # Execute target file (if not loaded). Exports registered in self.modules.
                    self.run_file(path)
                    # If we're inside a module environment, inject exported variables from the imported module
                    if env.frame_type == 'module':
                        module_basename = os.path.splitext(os.path.basename(path))[0]
                        exports = self.modules.get(module_basename, {})
                        for k, v in exports.items():
                            # Do not override existing names in current module
                            if k not in env.values:
                                env.define(k, v)
                except RuntimeErrorPoh as e:
                    # If already formatted (starts with '[') keep as-is
                    msg = str(e)
                    if msg.startswith('['):
                        raise
                    raise RuntimeErrorPoh(self.runtime_error(msg, node=st))
        elif isinstance(st, ReturnStmt):
            raise _ReturnSignal(self._eval(st.value, env) if st.value is not None else None)
        elif isinstance(st, BlockStmt):
            self._exec_block(st.body, Environment(env, frame_type='block'))
        else:
            # placeholders for Stop/Skip were mapped to Write None in parser; detect specifically
            pass

    def _eval(self, e: Expr, env: Environment) -> Any:
        if isinstance(e, LiteralExpr):
            result = e.value
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Literal => {result!r}")
            return result
        if isinstance(e, IdentifierExpr):
            if e.name.lower() == 'true':
                result = True
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Identifier '{e.name}' => {result!r}")
                return result
            if e.name.lower() == 'false':
                result = False
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Identifier '{e.name}' => {result!r}")
                return result
            if e.name.lower() == 'nothing':
                result = None
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Identifier '{e.name}' => {result!r}")
                return result
            # Undefined variable handling with context
            try:
                result = env.get(e.name)
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Identifier '{e.name}' => {result!r}")
                return result
            except RuntimeErrorPoh:
                # If a function with this name exists, treat it as a first-class value
                if e.name in self.functions:
                    fn_val = self.functions[e.name]
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Identifier '{e.name}' => <function>")
                    return fn_val
                raise RuntimeErrorPoh(self.runtime_error(f"Undefined variable '{e.name}'", node=e))
        if isinstance(e, UnaryExpr):
            v = self._eval(e.expr, env)
            if e.op == '-':
                result = -v
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Unary '{e.op}' => {result!r}")
                return result
            if e.op == '+':
                result = +v
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Unary '{e.op}' => {result!r}")
                return result
            if e.op == '!':
                result = not self._is_truthy(v)
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Unary '{e.op}' => {result!r}")
                return result
        if isinstance(e, BinaryExpr):
            if e.op in ('+', '-', '*', '/'):
                l = self._eval(e.left, env)
                r = self._eval(e.right, env)
                # Type mismatch detection for numeric ops (except '+' where string concat is allowed)
                if e.op != '+' and (isinstance(l, str) or isinstance(r, str)):
                    raise RuntimeErrorPoh(self.runtime_error(f"Type mismatch: cannot apply '{e.op}' to string operand(s)", node=e))
                if e.op == '+':
                    # Allow string concatenation
                    if isinstance(l, str) or isinstance(r, str):
                        result = str(l) + str(r)
                    else:
                        result = l + r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Binary '+' => {result!r}")
                    return result
                if e.op == '-':
                    result = l - r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Binary '-' => {result!r}")
                    return result
                if e.op == '*':
                    result = l * r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Binary '*' => {result!r}")
                    return result
                if e.op == '/':
                    try:
                        result = l / r
                        if self.debug_enabled:
                            self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Binary '/' => {result!r}")
                        return result
                    except ZeroDivisionError:
                        raise RuntimeErrorPoh(self.runtime_error("Oops! You tried to divide by zero. That's not allowed.", node=e))
            if e.op in ('==', '!=', '>', '<', '>=', '<='):
                l = self._eval(e.left, env)
                r = self._eval(e.right, env)
                if e.op == '==':
                    result = l == r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '==' => {result!r}")
                    return result
                if e.op == '!=':
                    result = l != r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '!=' => {result!r}")
                    return result
                if e.op == '>':
                    result = l > r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '>' => {result!r}")
                    return result
                if e.op == '<':
                    result = l < r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '<' => {result!r}")
                    return result
                if e.op == '>=':
                    result = l >= r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '>=' => {result!r}")
                    return result
                if e.op == '<=':
                    result = l <= r
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Compare '<=' => {result!r}")
                    return result
            if e.op in ('&&', '||'):
                l = self._is_truthy(self._eval(e.left, env))
                if e.op == '&&':
                    result = l and self._is_truthy(self._eval(e.right, env))
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Logic '&&' => {result!r}")
                    return result
                else:
                    result = l or self._is_truthy(self._eval(e.right, env))
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Logic '||' => {result!r}")
                    return result
        if isinstance(e, PredicateExpr):
            v = self._eval(e.value, env)
            if not isinstance(v, (int, float)):
                raise RuntimeErrorPoh(self.runtime_error("Predicate expects a number", node=e))
            if e.name == 'even':
                result = int(v) % 2 == 0
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Predicate even => {result!r}")
                return result
            if e.name == 'odd':
                result = int(v) % 2 != 0
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Predicate odd => {result!r}")
                return result
            if e.name == 'positive':
                result = v > 0
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Predicate positive => {result!r}")
                return result
            if e.name == 'negative':
                result = v < 0
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Predicate negative => {result!r}")
                return result
        if isinstance(e, CallExpr):
            # Allow identifier call in expression positions
            if e.name in self.functions:
                fn = self.functions[e.name]
                args = [self._eval(a, env) for a in e.args]
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Call {e.name}(...)")
                result = fn.call(args, call_node=e)
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Call {e.name} => {result!r}")
                return result
            # Fallback: call a function value stored in a variable
            try:
                callee = env.get(e.name)
            except RuntimeErrorPoh:
                callee = None
            if isinstance(callee, Function):
                args = [self._eval(a, env) for a in e.args]
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Call <var {e.name}>(...)")
                return callee.call(args, call_node=e)
            import difflib
            suggestion = difflib.get_close_matches(e.name, list(self.functions.keys()), n=1)
            hint = f" Did you mean '{suggestion[0]}'?" if suggestion else ""
            raise RuntimeErrorPoh(self.runtime_error(f"Unknown function '{e.name}'.{hint}", node=e))
        if isinstance(e, RandomIntBetweenExpr):
            import random
            lo = self._eval(e.low, env)
            hi = self._eval(e.high, env)
            result = random.randint(int(lo), int(hi))
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: RandomIntBetween => {result!r}")
            return result
        if isinstance(e, RandomFloatBetweenExpr):
            import random
            lo = float(self._eval(e.low, env))
            hi = float(self._eval(e.high, env))
            result = random.uniform(lo, hi)
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: RandomFloatBetween => {result!r}")
            return result
        if isinstance(e, RandomFromExpr):
            import random
            col = self._eval(e.collection, env)
            if isinstance(col, (list, str)):
                if not col:
                    result = None
                else:
                    result = random.choice(list(col))
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: RandomFrom => {result!r}")
                return result
            if isinstance(col, dict):
                keys = list(col.keys())
                if not keys:
                    result = None
                else:
                    result = col[random.choice(keys)]
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: RandomFrom => {result!r}")
                return result
            raise RuntimeErrorPoh(self.runtime_error("random from expects a list, string, or dictionary", node=e))
        if isinstance(e, ContainsExpr):
            col = self._eval(e.collection, env)
            needle = self._eval(e.needle, env)
            if isinstance(col, dict):
                result = needle in col
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Contains => {result!r}")
                return result
            try:
                result = needle in col
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Contains => {result!r}")
                return result
            except TypeError:
                return False
        if isinstance(e, AllPredicateExpr):
            col = self._eval(e.collection, env)
            if not isinstance(col, (list, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("all <collection> are <predicate> expects a list", node=e))
            result = all(self._num_predicate(v, e.predicate) for v in col)
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: AllPredicate => {result!r}")
            return result
        if isinstance(e, AnyPredicateExpr):
            col = self._eval(e.collection, env)
            if not isinstance(col, (list, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("any <collection> is <predicate> expects a list", node=e))
            result = any(self._num_predicate(v, e.predicate) for v in col)
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: AnyPredicate => {result!r}")
            return result
        if isinstance(e, ListLiteralExpr):
            vals = [self._eval(it, env) for it in e.items]
            # Legacy forms take precedence: treat as legacy wrappers (immutable flag + legacy warning on mutation)
            if e.legacy_literal:
                result = Interpreter.PohList(vals, mutable=False, legacy=True, origin_node=e)
            elif e.mutable:
                result = Interpreter.PohList(vals, mutable=True, legacy=False, origin_node=e)
            else:
                result = tuple(vals)
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: ListLiteral => {result!r}")
            return result
        if isinstance(e, DictLiteralExpr):
            kv = {self._eval(k, env): self._eval(v, env) for k, v in e.items}
            if e.legacy_literal:
                result = Interpreter.PohDict(kv, mutable=False, legacy=True, origin_node=e)
            elif e.mutable:
                result = Interpreter.PohDict(kv, mutable=True, legacy=False, origin_node=e)
            else:
                result = Interpreter.FrozenDict(kv)
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: DictLiteral => {result!r}")
            return result
        if isinstance(e, AtExpr):
            container = self._eval(e.container, env)
            key = self._eval(e.key, env)
            if isinstance(container, (list, tuple, Interpreter.PohList)):
                try:
                    result = container[key]
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: Index => {result!r}")
                    return result
                except IndexError:
                    raise RuntimeErrorPoh(self.runtime_error(f"Index {key} is out of range for the list.", node=e))
            if isinstance(container, (dict, Interpreter.FrozenDict, Interpreter.PohDict)):
                try:
                    result = container[key]
                    if self.debug_enabled:
                        self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: KeyLookup => {result!r}")
                    return result
                except KeyError:
                    raise RuntimeErrorPoh(self.runtime_error(f"Key {key} was not found in the dictionary.", node=e))
            raise RuntimeErrorPoh(self.runtime_error("'at' expects a list index or dictionary key", node=e))
        if isinstance(e, NthItemExpr):
            container = self._eval(e.container, env)
            if not isinstance(container, (list, tuple, Interpreter.PohList)):
                raise RuntimeErrorPoh(self.runtime_error("Nth item expects a list", node=e))
            try:
                idx_val = self._eval(e.index, env)
            except RuntimeErrorPoh as ex:
                msg = str(ex)
                if "Undefined variable" in msg:
                    raise RuntimeErrorPoh(self.runtime_error("Index must be a number", node=e))
                raise
            try:
                idx = int(idx_val)
            except Exception:
                raise RuntimeErrorPoh(self.runtime_error("Index must be a number", node=e))
            idx0 = idx - 1
            if idx0 < 0 or idx0 >= len(container):
                raise RuntimeErrorPoh(self.runtime_error(f"Index {idx} is out of range for the list.", node=e))
            result = container[idx0]
            if self.debug_enabled:
                self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: NthItem => {result!r}")
            return result
        if isinstance(e, KeysOfExpr):
            container = self._eval(e.container, env)
            if isinstance(container, (dict, Interpreter.FrozenDict, Interpreter.PohDict)):
                result = list(container.keys())
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: KeysOf => {result!r}")
                return result
            raise RuntimeErrorPoh(self.runtime_error("keys of expects a dictionary", node=e))
        if isinstance(e, ValuesOfExpr):
            container = self._eval(e.container, env)
            if isinstance(container, (dict, Interpreter.FrozenDict, Interpreter.PohDict)):
                result = list(container.values())
                if self.debug_enabled:
                    self._debug_print(getattr(e, 'line', None), getattr(e, 'col', None), f"Evaluating: ValuesOf => {result!r}")
                return result
            raise RuntimeErrorPoh(self.runtime_error("values of expects a dictionary", node=e))
        return None

    def _is_truthy(self, v: Any) -> bool:
        return bool(v)

    def _install_builtins(self) -> None:
        # length(x): works for strings, lists, dicts
        def _length(args: List[Any]) -> Any:
            if len(args) != 1:
                raise RuntimeErrorPoh(self.runtime_error("length expects 1 argument"))
            x = args[0]
            try:
                return len(x)
            except Exception:
                raise RuntimeErrorPoh(self.runtime_error("length expects a collection or string"))

        # sum(list): numeric sum
        def _sum(args: List[Any]) -> Any:
            if len(args) != 1:
                raise RuntimeErrorPoh(self.runtime_error("sum expects 1 argument"))
            x = args[0]
            if not isinstance(x, (list, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("sum expects a list"))
            total = 0
            for v in x:
                if not isinstance(v, (int, float)):
                    raise RuntimeErrorPoh(self.runtime_error("sum expects numeric values"))
                total += v
            return total

        # min(list) / max(list): numeric min/max
        def _minf(args: List[Any]) -> Any:
            if len(args) != 1:
                raise RuntimeErrorPoh(self.runtime_error("min expects 1 argument"))
            x = args[0]
            if not isinstance(x, (list, tuple)) or not x:
                raise RuntimeErrorPoh(self.runtime_error("min expects a non-empty list"))
            for v in x:
                if not isinstance(v, (int, float)):
                    raise RuntimeErrorPoh(self.runtime_error("min expects numeric values"))
            return min(x)

        def _maxf(args: List[Any]) -> Any:
            if len(args) != 1:
                raise RuntimeErrorPoh(self.runtime_error("max expects 1 argument"))
            x = args[0]
            if not isinstance(x, (list, tuple)) or not x:
                raise RuntimeErrorPoh(self.runtime_error("max expects a non-empty list"))
            for v in x:
                if not isinstance(v, (int, float)):
                    raise RuntimeErrorPoh(self.runtime_error("max expects numeric values"))
            return max(x)

        class _Builtin(Function):
            def __init__(self, name: str, impl: Callable[[List[Any]], Any]):
                self.name = name
                self.impl = impl

            def call(self, args: List[Any], call_node: Optional[object] = None) -> Any:  # type: ignore[override]
                return self.impl(args)

        # New built-ins --------------------------------------------------
        def _range(args: List[Any]) -> Any:
            # range(n) or range(start, stop[, step])
            if not 1 <= len(args) <= 3:
                raise RuntimeErrorPoh(self.runtime_error("range expects 1 to 3 arguments"))
            nums = [int(a) for a in args]
            if len(nums) == 1:
                return list(range(nums[0]))
            if len(nums) == 2:
                return list(range(nums[0], nums[1]))
            return list(range(nums[0], nums[1], nums[2]))

        def _join(args: List[Any]) -> Any:
            # join(list, sep) or join(list) default sep empty
            if not (1 <= len(args) <= 2):
                raise RuntimeErrorPoh(self.runtime_error("join expects list and optional separator"))
            col = args[0]
            if not isinstance(col, (list, tuple)):
                raise RuntimeErrorPoh(self.runtime_error("join expects a list"))
            sep = args[1] if len(args) == 2 else ''
            return str(sep).join(str(x) for x in col)

        def _split(args: List[Any]) -> Any:
            # split(text, sep) -> list
            if len(args) != 2:
                raise RuntimeErrorPoh(self.runtime_error("split expects text and separator"))
            return str(args[0]).split(str(args[1]))

        def _now(args: List[Any]) -> Any:
            if args:
                raise RuntimeErrorPoh(self.runtime_error("now expects no arguments"))
            import datetime
            return datetime.datetime.now().isoformat(timespec='seconds')

        self.functions['length'] = _Builtin('length', _length)
        self.functions['sum'] = _Builtin('sum', _sum)
        self.functions['min'] = _Builtin('min', _minf)
        self.functions['max'] = _Builtin('max', _maxf)
        self.functions['range'] = _Builtin('range', _range)
        self.functions['join'] = _Builtin('join', _join)
        self.functions['split'] = _Builtin('split', _split)
        self.functions['now'] = _Builtin('now', _now)

    def _num_predicate(self, v: Any, pred: str) -> bool:
        if not isinstance(v, (int, float)):
            return False
        if pred == 'even':
            return int(v) % 2 == 0
        if pred == 'odd':
            return int(v) % 2 != 0
        if pred == 'positive':
            return v > 0
        if pred == 'negative':
            return v < 0
        return False
