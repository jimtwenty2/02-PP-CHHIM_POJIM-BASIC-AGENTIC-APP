from pydantic import BaseModel, Field, PositiveInt

class ListBooksInput(BaseModel):
    pass

class SearchBookInput(BaseModel):

    query: str = Field(
        min_length=1,
        description="Book title to search for",
    )


class BookIdInput(BaseModel):

    book_id: PositiveInt = Field(
        description="Numeric book ID taken from a previous tool result, for example 2",
    )

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "list_books",
            "description": (
                "List all books with their ID, title, author, "
                "and number of available copies."
            ),
            "parameters": ListBooksInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_book",
            "description": (
                "Search books by title. Returns the book ID, "
                "title, and author, but not stock information."
            ),
            "parameters": SearchBookInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": (
                "Check how many copies of a specific book are available. "
                "Requires a book_id."
            ),
            "parameters": BookIdInput.model_json_schema(),
        },
    },
    {
        "type": "function",
        "function": {
            "name": "borrow_book",
            "description": (
                "Borrow one copy of a book. This operation is admin-only. "
                "Requires a book_id."
            ),
            "parameters": BookIdInput.model_json_schema(),
        },
    },
]