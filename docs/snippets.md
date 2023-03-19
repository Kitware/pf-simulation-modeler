# `engine/snippets/`

## `snippet_manager.py`

Handles the creation of page code snippets. Binds controller functions `toggle_snippet`, `get_snippet`, and `generate_code`.

- `toggle_snippet()` - Toggles the visibility of the code snippet overlay.
- `get_snippet(snippet)` - Generate the code snippet for the `snippet`'s page.
- `generate_code()` - Generates code for entire project.

---

## Snippets

Each of the following snippets correspond to a page in the UI:

- `boundary_conditions.py`
- `domain.py`
- `solver.py`
- `subsurface_properties.py`
- `timing.py`

Additionally, there is another snippet `domain_builder.py` that collects metadata from various pages to be used in `pftools`' `DomainBuilder` class.

The structure of each snippet is as follows:

```python
class TestSnippet:
    def __init__(self, state, ctrl):
        self.state, self.ctrl = state, ctrl

        self.a_code = ""
        self.b_code = ""
        ...

        self.domain_builder_params = {} # occasionally used

    def set_a(self):
        code = "# Generate the code for a!"
        ...
        self.a_code = code

    def set_b(self):
        ...
        self.b_code = code

    @property
    def snippet(self):
        self.set_a()
        self.set_b()
        ...
        return self.a_code + self.b_code + ...
```

Simply invoking `TestSnippet.snippet` will generate and return the code snippet for the page.
