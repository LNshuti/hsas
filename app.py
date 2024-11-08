import os
import json
import openai
import duckdb
import gradio as gr
from functools import lru_cache

# =========================
# Configuration and Setup
# =========================

openai.api_key = os.getenv("OPENAI_API_KEY")
DATASET_PATH = 'hsas.parquet'  # Update with your Parquet file path

SCHEMA = [
    {"column_name": "total_charges", "column_type": "BIGINT"},
    {"column_name": "medicare_prov_num", "column_type": "BIGINT"},
    {"column_name": "zip_cd_of_residence", "column_type": "VARCHAR"},
    {"column_name": "total_days_of_care", "column_type": "BIGINT"},
    {"column_name": "total_cases", "column_type": "BIGINT"},
]

@lru_cache(maxsize=1)
def get_schema():
    return SCHEMA

COLUMN_TYPES = {col['column_name']: col['column_type'] for col in get_schema()}

# =========================
# OpenAI API Integration
# =========================

def parse_query(nl_query):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that converts natural language queries into SQL queries for the 'hsa_data' table. "
                "Ensure the SQL query is syntactically correct and uses only the columns provided in the schema."
            ),
        },
        {
            "role": "user",
            "content": f"Schema:\n{json.dumps(get_schema(), indent=2)}\n\nQuery:\n\"{nl_query}\"\n\nSQL:",
        },
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=messages,
            temperature=0,
            max_tokens=150,
        )
        sql_query = response.choices[0].message.content.strip()
        return sql_query, ""
    except Exception as e:
        return "", f"Error generating SQL query: {e}"

# =========================
# Database Interaction
# =========================

def execute_sql_query(sql_query):
    try:
        con = duckdb.connect(database=':memory:')
        con.execute(f"CREATE OR REPLACE VIEW hsa_data AS SELECT * FROM '{DATASET_PATH}'")
        result_df = con.execute(sql_query).fetchdf()
        con.close()
        return result_df, ""
    except Exception as e:
        return None, f"Error executing query: {e}"

# =========================
# Gradio Application UI
# =========================

with gr.Blocks() as demo:
    gr.Markdown("""
    # Text-to-SQL Healthcare Data Analyst Agent

    Analyze U.S. prescription data from the Center of Medicare and Medicaid.

    ## Instructions

    1. **Describe the data you want**: e.g., `Show total days of care by zip`
    2. **Use Example Queries**: Click on any example query button below to execute.
    3. **Generate SQL**: Or, enter your own query and click "Generate SQL".

    ## Example Queries
    """)

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### Example Queries:")
            query_buttons = [
                "Calculate the average total_charges by zip_cd_of_residence",
                "For each zip_cd_of_residence, calculate the sum of total_charges",
                "SELECT * FROM hsa_data WHERE total_days_of_care > 40 LIMIT 30;",
            ]
            btn_queries = [gr.Button(q) for q in query_buttons]

            query_input = gr.Textbox(
                label="Your Query",
                placeholder='e.g., "Show total charges over 1M by state"',
                lines=1,
            )

            btn_generate_sql = gr.Button("Generate SQL Query")
            sql_query_out = gr.Code(label="Generated SQL Query", language="sql")
            btn_execute_query = gr.Button("Execute Query")
            error_out = gr.Markdown(visible=False)
        with gr.Column(scale=2):
            results_out = gr.Dataframe(label="Query Results")

    with gr.Tab("Dataset Schema"):
        gr.Markdown("### Dataset Schema")
        schema_display = gr.JSON(label="Schema", value=get_schema())

    # =========================
    # Event Functions
    # =========================

    def generate_sql(nl_query):
        sql_query, error = parse_query(nl_query)
        if error:
            error_update = gr.Markdown.update(visible=True, value=error)
        else:
            error_update = gr.Markdown.update(visible=False)
        return sql_query, error_update

    def execute_query(sql_query):
        result_df, error = execute_sql_query(sql_query)
        if error:
            error_update = gr.Markdown.update(visible=True, value=error)
        else:
            error_update = gr.Markdown.update(visible=False)
        return result_df, error_update

    def handle_example_click(example_query):
        if example_query.strip().upper().startswith("SELECT"):
            sql_query = example_query
            result_df, error = execute_sql_query(sql_query)
            if error:
                error_update = gr.Markdown.update(visible=True, value=error)
            else:
                error_update = gr.Markdown.update(visible=False)
            return sql_query, gr.update(), result_df, error_update
        else:
            sql_query, error = parse_query(example_query)
            if error:
                error_update = gr.Markdown.update(visible=True, value=error)
                return sql_query, error_update, None, error_update
            result_df, exec_error = execute_sql_query(sql_query)
            if exec_error:
                error_update = gr.Markdown.update(visible=True, value=exec_error)
            else:
                error_update = gr.Markdown.update(visible=False)
            return sql_query, gr.update(), result_df, error_update

    # =========================
    # Button Click Event Handlers
    # =========================

    btn_generate_sql.click(
        fn=generate_sql,
        inputs=query_input,
        outputs=[sql_query_out, error_out],
    )

    btn_execute_query.click(
        fn=execute_query,
        inputs=sql_query_out,
        outputs=[results_out, error_out],
    )

    for btn, query in zip(btn_queries, query_buttons):
        btn.click(
            fn=lambda q=query: handle_example_click(q),
            outputs=[sql_query_out, error_out, results_out, error_out],
        )

# Launch the Gradio App
if __name__ == "__main__":
    demo.launch()
