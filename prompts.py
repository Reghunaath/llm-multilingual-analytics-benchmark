TEMPERATURE = 0.0

SQL_SYSTEM_PROMPT = (
    "You are an expert SQL developer. Given a database schema and a natural language question, "
    "generate a single SQL query(MySQL) that answers the question. "
    "Output ONLY the raw SQL query with no explanation, no markdown formatting, and no code fences."
)

PANDAS_SYSTEM_PROMPT = (
    "You are an expert Python/Pandas developer. Given a database schema and a natural language question, "
    "generate Pandas code that answers the question. Assume each table is already loaded as a DataFrame "
    "whose variable name matches the table name (lowercased). "
    "Output ONLY the raw Python/Pandas code with no explanation, no markdown formatting, and no code fences."
)

R_SYSTEM_PROMPT = (
    "You are an expert R developer. Given a database schema and a natural language question, "
    "generate R code using dplyr/tidyverse that answers the question. Assume each table is already loaded "
    "as a data frame whose variable name matches the table name (lowercased). "
    "Output ONLY the raw R code with no explanation, no markdown formatting, and no code fences."
)


def build_sql_prompt(schema: str, question: str) -> list[dict]:
    return [
        {"role": "system", "content": SQL_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Schema:\n{schema}\n\nQuestion: {question}",
        },
    ]


def build_pandas_prompt(schema: str, question: str) -> list[dict]:
    return [
        {"role": "system", "content": PANDAS_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Schema:\n{schema}\n\nQuestion: {question}",
        },
    ]


def build_r_prompt(schema: str, question: str) -> list[dict]:
    return [
        {"role": "system", "content": R_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": f"Schema:\n{schema}\n\nQuestion: {question}",
        },
    ]
