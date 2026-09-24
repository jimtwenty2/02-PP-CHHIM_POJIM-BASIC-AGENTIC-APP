from pydantic import ValidationError

from app import tools
from app.schemas import BookIdInput, ListBooksInput, SearchBookInput

# allowlist:
TOOL_REGISTRY = {
    "list_books": (ListBooksInput, tools.list_books),
    "search_book": (SearchBookInput, tools.search_book),
    "check_availability": (BookIdInput, tools.check_availability),
    "borrow_book": (BookIdInput, tools.borrow_book),
}

# permission rule: which role may use which tool
PERMISSIONS = {
    "customer": {"list_books", "search_book", "check_availability"},
    "admin": {"list_books", "search_book", "check_availability", "borrow_book"},
}

def run_tool(name, args, user_role):

    # allowlist
    if name not in TOOL_REGISTRY:
        return {"ok": False, "error": "TOOL_NOT_ALLOWED"}

    # permission
    if name not in PERMISSIONS.get(user_role, set()):
        return {"ok": False, "error": "PERMISSION_DENIED"}

    # input validation
    schema, function = TOOL_REGISTRY[name]
    try:
        clean = schema(**args)
    except ValidationError:
        return {"ok": False, "error": "INVALID_INPUT"}

    # run the tool
    try:
        return function(**clean.model_dump())
    except Exception:
        return {"ok": False, "error": "TOOL_FAILED"}