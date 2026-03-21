# Natural Language to SQL/Pandas Converter

A Streamlit web app that converts natural language questions into SQL and Pandas queries using OpenAI GPT-5.4 and Google Gemini 3.1 Pro.

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure API keys**

   Copy the example env file and add your keys:

   ```bash
   cp .env.example .env
   ```

   Edit `.env` with your OpenAI and/or Google API keys. You can also enter them in the app sidebar at runtime.

3. **Run the app**

   ```bash
   streamlit run app.py
   ```

## Usage

1. Paste a table schema (CREATE TABLE statement or plain description) into the schema text area.
2. Type a natural language question about your data.
3. Choose a model (GPT-5.4, Gemini 3.1 Pro, or Compare Both) and output type (SQL, Pandas, or Both).
4. Click **Generate** to get the query.

The tool generates queries only — it does not execute them against any database.
