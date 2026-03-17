import re


def validate_schema(schema_text: str) -> tuple[bool, str]:
    """Validate that the schema text contains table-like content.

    Returns (is_valid, error_message). error_message is empty when valid.
    """
    if not schema_text or not schema_text.strip():
        return False, "Schema is empty. Please provide a table schema."

    text = schema_text.strip()

    has_create_table = bool(re.search(r"CREATE\s+TABLE", text, re.IGNORECASE))
    has_column_types = bool(
        re.search(
            r"\b(INT|INTEGER|VARCHAR|TEXT|CHAR|FLOAT|DOUBLE|DECIMAL|DATE|TIMESTAMP|BOOLEAN|BOOL|BIGINT|SMALLINT|SERIAL|UUID)\b",
            text,
            re.IGNORECASE,
        )
    )
    has_table_word = bool(re.search(r"\btable\b", text, re.IGNORECASE))
    has_column_word = bool(re.search(r"\bcolumn\b", text, re.IGNORECASE))
    has_parentheses = "(" in text and ")" in text

    if has_create_table:
        return True, ""
    if has_column_types and has_parentheses:
        return True, ""
    if has_table_word and (has_column_types or has_column_word):
        return True, ""

    return (
        False,
        "Schema doesn't appear to describe a database table. "
        "Please provide a CREATE TABLE statement or a description with table/column names and types.",
    )
