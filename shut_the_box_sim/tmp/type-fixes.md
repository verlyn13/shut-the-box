Okay, team! Here's a dev checklist to help you squash those `mypy` type errors. Work through these items one by one. When you've fixed an error and `mypy` no longer complains about it, check it off!

**General Tips for Junior Devs Tackling Type Errors:**

* **Read the Error Carefully:** `mypy` usually gives good clues. Pay attention to the line number and the types it mentions (e.g., "expected X, got Y").
* **`typing` Module is Your Friend:** Most type hints come from the `typing` module (e.g., `List`, `Dict`, `Optional`, `Any`, `Tuple`, `Set`, `Union`). Remember to import them!
* **`-> None` for Functions That Don't Return:** If your function just does something (like printing or modifying an object in place) and doesn't `return` a value, its return type is `-> None`.
* **`Any` as a Last Resort:** While `Any` can make an error go away, try to be as specific as possible with your types. `Any` tells `mypy` "don't check this part."
* **Untyped Calls:** If you see "Call to untyped function," it means the function being called needs type hints. Fix the *called* function first.
* **Iterate:** Fix a few errors, then re-run `mypy`. Sometimes fixing one error resolves others!

---
## MyPy Error Dev Checklist

### `src/stbsim/stats.py`

* **`[x] stats.py:8: error: Missing type parameters for generic type "Dict" [type-arg]`**
    * **Task:** Specify the key and value types for `Dict` in the function signature.
        * `def calculate_summary_stats(game_results: List[Dict]) -> Dict:`
    * **How to Fix:**
        1.  For `game_results: List[Dict]`: Determine the structure of the dictionaries inside the list. If they have string keys and values of any type, change `Dict` to `Dict[str, Any]`. So, `List[Dict[str, Any]]`.
        2.  For the return type `-> Dict`: Determine the structure of the dictionary this function returns. If it also has string keys and values of any type, change `Dict` to `Dict[str, Any]`.
    * **Corrected Example:** `def calculate_summary_stats(game_results: List[Dict[str, Any]]) -> Dict[str, Any]:`
    * **Junior Dev Tip:** `Dict` is a generic type, like a template. You need to tell Python what types the keys and values will be. For example, `Dict[str, int]` means keys are strings, values are integers. `Any` means the value can be of any type.

---
### `src/stbsim/player.py`

* **`[x] player.py:6: error: Function is missing a return type annotation [no-untyped-def]`**
    * **Task:** Add a return type annotation to the function definition at line 6.
    * **How to Fix:** If the function doesn't return any value, add `-> None`. If it returns, say, an integer, add `-> int`.
    * **Example:** `def my_function(some_arg: str) -> None:`
    * **Junior Dev Tip:** Every function needs to declare what type of value it returns. This helps `mypy` (and other developers!) understand how the function is supposed to be used.

* **`[x] player.py:9: error: Function is missing a type annotation [no-untyped-def]`**
    * **Task:** Add type annotations for the arguments and the return type of the function at line 9.
    * **How to Fix:** Similar to the above, but also add types for each parameter.
    * **Example:** `def another_function(name: str, age: int) -> bool:`
    * **Junior Dev Tip:** Type hint all parameters passed into a function as well as its return value.

---
### `src/stbsim/board.py`

* **`[x] board.py:17: error: Function is missing a type annotation [no-untyped-def]`**
    * **Task:** Add type annotations for the arguments and the return type of the function at line 17.
    * **How to Fix:** Add type hints for each parameter and a return type annotation (e.g., `-> None`, `-> str`).
    * **Example:** `def setup_board(size: int, pieces: List[str]) -> None:`

---
### `src/stbsim/dice.py`

* **`[x] dice.py:11: error: Incompatible types in assignment (expression has type "int", variable has type "None") [assignment]`**
    * **Task:** The variable was likely typed as `None` or not explicitly typed and inferred as `None` initially, but you're assigning an `int` to it.
    * **How to Fix:**
        1.  Check how the variable is declared/initialized.
        2.  If it's intended to hold an integer but might sometimes be `None` (e.g., before it's set), its type should be `Optional[int]`. Remember to `from typing import Optional`.
        3.  If it should *always* be an integer after this point, ensure its type is `int`. The error might stem from an earlier incorrect type inference or annotation for that variable.
    * **Junior Dev Tip:** `Optional[X]` is a shorthand for `Union[X, None]`, meaning the variable can either be of type `X` or be `None`.

* **`[x] dice.py:12: error: Incompatible return value type (got "None", expected "int") [return-value]`**
    * **Task:** A function declared to return an `int` (e.g., `-> int`) is returning `None`.
    * **How to Fix:**
        1.  Ensure all possible paths in the function return an `int`.
        2.  Or, if it's valid for the function to sometimes return `None`, change its return type annotation to `-> Optional[int]`.
    * **Junior Dev Tip:** If a function *can* return `None` in some situations and an `int` in others, `Optional[int]` is the correct return type.

* **`[x] dice.py:25: error: Function is missing a return type annotation [no-untyped-def]`**
    * **Task:** Add a return type annotation to the function at line 25.
    * **How to Fix:** Use `-> ReturnType` (e.g., `-> int`, `-> None`).

* **`[x] dice.py:28: error: Function is missing a type annotation for one or more arguments [no-untyped-def]`**
    * **Task:** Add type hints to the arguments of the function at line 28.
    * **How to Fix:** Add `parameter_name: type` for each argument.

---
### `src/stbsim/loggers.py`

* **`[x] loggers.py:32: error: Function is missing a return type annotation [no-untyped-def]` (note: Use `-> None`...)**
    * **Task:** Add a return type. `mypy` suggests `-> None`.
    * **How to Fix:** Add `-> None` to the function definition if it doesn't return a value.

* **`[x] loggers.py:42: error: Missing type parameters for generic type "dict" [type-arg]`**
    * **Line in question:** `) -> dict:`
    * **Task:** Change `dict` to `Dict[KeyType, ValueType]`.
    * **How to Fix:** Given your `GameEvent` is `Dict[str, Any]`, it's likely this function should return `Dict[str, Any]`.
    * **Corrected Example:** `) -> Dict[str, Any]:`
    * **Junior Dev Tip:** Remember to `from typing import Dict, Any`.

* **`[x] loggers.py:56: error: Function is missing a return type annotation [no-untyped-def]`**
    * **Task:** Add a return type annotation.
* **`[x] loggers.py:56: error: Function is missing a type annotation for one or more arguments [no-untyped-def]`**
    * **Task:** Add type hints for the function's arguments.

* **Series of `[arg-type]` errors for `append` (lines 60, 72, 106, 125, 134, 143):**
    * **Error Example:** `loggers.py:60: error: Argument 1 to "append" of "list" has incompatible type "dict[str, Any]"; expected "GameEvent" [arg-type]`
    * **And:** `loggers.py:72: error: Argument 1 to "append" of "list" has incompatible type "dict[Any, Any]"; expected "GameEvent" [arg-type]`
    * **Task:** You have a list like `List[GameEvent]` (where `GameEvent` is `class GameEvent(Dict[str, Any]):`). You're trying to append a plain dictionary.
    * **How to Fix (for each append):**
        1.  Ensure the dictionary you are appending matches the `GameEvent` structure (string keys, any values).
        2.  When appending, explicitly create a `GameEvent` instance if needed: `my_list.append(GameEvent(your_dictionary_data))`.
        3.  For the `dict[Any, Any]` errors, this is critical: `GameEvent` expects `str` keys. You *must* ensure the dictionaries you're trying to append have string keys. If a key is an `int`, for example, it's incompatible.
    * **Junior Dev Tip:** Even though `GameEvent` *is* a `Dict[str, Any]`, `mypy` can be stricter when dealing with subclass relationships and list appends. Providing an actual `GameEvent` instance or casting can resolve this. The `dict[Any, Any]` errors mean your dictionary keys are not just strings, which directly violates the `GameEvent` definition.

* **`[x] loggers.py:62, 74, 108, 127, 136: error: Function is missing a type annotation [no-untyped-def]`**
    * **Task:** Add type annotations for arguments and return types for these functions.

* **`[x] loggers.py:145, 150: error: Function is missing a return type annotation [no-untyped-def]` (note: Use `-> None`...)**
    * **Task:** Add `-> None` or the correct return type for these functions.

---
### `src/stbsim/turn_manager.py`

* **`[x] turn_manager.py:33: error: Function is missing a return type annotation [no-untyped-def]`**
    * **Task:** Add a return type annotation.

* **Series of `[no-untyped-call]` errors (lines 41, 55, 72, 96):**
    * **Error Example:** `turn_manager.py:41: error: Call to untyped function "log_dice_roll" in typed context [no-untyped-call]`
    * **Task:** The functions `log_dice_roll`, `log_move_attempt`, `log_turn_end` (likely defined in `loggers.py`) are missing type annotations.
    * **How to Fix:** Go to the definitions of these functions and add full type hints (for their arguments and return values). Many of these were flagged in `loggers.py` already. Fixing them there will resolve these errors.
    * **Junior Dev Tip:** When `mypy` says "Call to untyped function," it means the function *being called* needs types. Go to that function's definition and add them.

---
### `src/stbsim/game.py`

* **`[x] game.py:10: error: Function is missing a type annotation for one or more arguments [no-untyped-def]`**
    * **Task:** Add type hints for all arguments of the function (likely `__init__`) at line 10.

* **`[x] game.py:30, 36, 75: error: Function is missing a return type annotation [no-untyped-def]` (note: Use `-> None`...)**
    * **Task:** Add `-> None` or the correct return type.

* **`[x] game.py:37: error: Call to untyped function "initialize" in typed context [no-untyped-call]`**
    * **Task:** The `initialize` method/function needs type annotations.
    * **How to Fix:** Find its definition (it might be one of the functions at line 30 or 36) and add argument types and a return type.

* **`[x] game.py:39: error: Call to untyped function "log_game_start" in typed context [no-untyped-call]`**
* **`[x] game.py:68: error: Call to untyped function "log_game_end" in typed context [no-untyped-call]`**
    * **Task:** `log_game_start` and `log_game_end` need type annotations.
    * **How to Fix:** Go to their definitions in `loggers.py` and add full type hints.

* **`[x] game.py:53: error: Argument "sim_id" to "TurnManager" has incompatible type "int"; expected "str | None" [arg-type]`**
* **`[x] game.py:54: error: Argument "game_id" to "TurnManager" has incompatible type "int"; expected "str | None" [arg-type]`**
    * **Task:** You're passing an `int` to `TurnManager`'s constructor for `sim_id` and `game_id`, but it expects `str` or `None`.
    * **How to Fix (Choose one):**
        1.  **Convert to string:** Pass `str(your_int_sim_id)` and `str(your_int_game_id)`.
        2.  **Change `TurnManager`:** If `TurnManager` *can* logically accept integers, update its `__init__` signature for these parameters to `sim_id: Optional[Union[str, int]]` (and import `Union`).
    * **Junior Dev Tip:** Make sure the data types you pass to functions match what the function declares it expects.

* **`[x] game.py:58: error: Call to untyped function "play_turn" in typed context [no-untyped-call]`**
    * **Task:** The `play_turn` method (likely in `TurnManager`) needs type annotations.
    * **How to Fix:** Go to its definition and add type hints for its arguments and return value.

---
### `src/stbsim/simulation.py`

* **`[x] simulation.py:13: error: Function is missing a return type annotation [no-untyped-def]` (note: Use `-> None`...)**
    * **Task:** Add `-> None` for the `__init__` method (if it's line 13 and it is `__init__`) or the correct return type for the function at this line.

* **`[x] simulation.py:22: error: Missing type parameters for generic type "Dict" [type-arg]`**
    * **Line in question:** `) -> List[Dict]:`
    * **Task:** Specify key/value types for `Dict` within the `List`.
    * **How to Fix:** Likely `List[Dict[str, Any]]` if these are game results or events.
    * **Corrected Example:** `) -> List[Dict[str, Any]]:`

* **`[x] simulation.py:30: error: Call to untyped function "InMemoryEventLogger" in typed context [no-untyped-call]`**
    * **Task:** The `InMemoryEventLogger` class constructor (`__init__` method in `loggers.py`) needs type annotations.
    * **How to Fix:** Go to the `InMemoryEventLogger` class definition and add types to its `__init__` method.

* **`[x] simulation.py:35: error: Call to untyped function "start_game" in typed context [no-untyped-call]`**
    * **Task:** The `start_game` method (likely in your `Game` class) needs type annotations.
    * **How to Fix:** Go to its definition and add type hints.

---
### `src/stbsim/cli.py`

* **`[x] cli.py:8: error: Library stubs not installed for "tqdm" [import-untyped]`**
    * **Task:** Install type stubs for the `tqdm` library.
    * **How to Fix (as suggested by `mypy`):**
        * Run: `python3 -m pip install types-tqdm`
        * If you are using `rye` (as indicated by your prompt `rye run typecheck`), use: `rye add --dev types-tqdm` and then `rye sync`.
        * If you are using another environment manager like Poetry or PDM: `poetry add types-tqdm --group dev` or `pdm add -d types-tqdm`.
        * **Junior Dev Tip:** Some libraries don't come with their own type information. "Stub" packages provide this information for `mypy`. Since you're not an admin on the machine, make sure you're installing this into your project's specific Python virtual environment.

* **`[x] cli.py:17: error: Function is missing a return type annotation [no-untyped-def]`**
    * **Task:** Add a return type annotation.

* **`[x] cli.py:54: error: Call to untyped function "Simulation" in typed context [no-untyped-call]`**
    * **Task:** The `Simulation` class constructor (`__init__` method in `simulation.py`) needs type annotations.
    * **How to Fix:** Go to the `Simulation` class definition and add types to its `__init__` method.

