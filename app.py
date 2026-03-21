import os

import streamlit as st
from dotenv import load_dotenv

from llm_client import generate, LLMError
from prompts import build_sql_prompt, build_pandas_prompt
from schema_parser import validate_schema

load_dotenv()

st.set_page_config(page_title="NL to SQL/Pandas Converter", layout="wide")
st.title("Natural Language to SQL/Pandas Converter")

# ── Sidebar: API keys ──────────────────────────────────────────────────────────
with st.sidebar:
    st.header("API Keys")
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
    )
    google_key = st.text_input(
        "Google API Key",
        type="password",
        value=os.getenv("GOOGLE_API_KEY", ""),
    )

api_keys = {"openai": openai_key, "google": google_key}

# ── Main area ──────────────────────────────────────────────────────────────────
schema = st.text_area(
    "Table Schema",
    height=180,
    placeholder="Paste a CREATE TABLE statement or describe your tables…",
)

question = st.text_input(
    "Your Question",
    placeholder='e.g. "How many users signed up last month?"',
)

col_model, col_output = st.columns(2)
with col_model:
    model_choice = st.radio(
        "Model",
        ["GPT-5.4", "Gemini 3.1 Pro", "Compare Both"],
        horizontal=True,
    )
with col_output:
    output_type = st.radio(
        "Output Type",
        ["SQL", "Pandas", "Both"],
        horizontal=True,
    )

MODEL_MAP = {
    "GPT-5.4": ["gpt-5.4"],
    "Gemini 3.1 Pro": ["gemini-3.1-pro-preview"],
    "Compare Both": ["gpt-5.4", "gemini-3.1-pro-preview"],
}
MODEL_LABELS = {"gpt-5.4": "GPT-5.4", "gemini-3.1-pro-preview": "Gemini 3.1 Pro"}

# ── Generate ───────────────────────────────────────────────────────────────────
if st.button("Generate", type="primary"):
    # Validate inputs
    if not question.strip():
        st.error("Please enter a question.")
    else:
        valid, err_msg = validate_schema(schema)
        if not valid:
            st.error(err_msg)
        else:
            models = MODEL_MAP[model_choice]
            prompt_builders = []
            if output_type in ("SQL", "Both"):
                prompt_builders.append(("SQL", build_sql_prompt))
            if output_type in ("Pandas", "Both"):
                prompt_builders.append(("Pandas", build_pandas_prompt))

            # Determine layout: side-by-side for Compare Both, else single column
            if len(models) > 1:
                columns = st.columns(len(models))
            else:
                columns = [st.container()]

            for col, model_id in zip(columns, models):
                with col:
                    st.subheader(MODEL_LABELS[model_id])
                    for label, builder in prompt_builders:
                        messages = builder(schema, question)
                        try:
                            result = generate(model_id, messages, api_keys)
                            lang = "sql" if label == "SQL" else "python"
                            st.markdown(f"**{label}**")
                            st.code(result, language=lang)
                        except LLMError as e:
                            st.error(f"{label} — {e.message}")
