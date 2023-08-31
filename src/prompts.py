import streamlit as st

QUALIFIED_TABLE_NAME = "WEATHER.CHATBOT_SOURCE.NYC_WEATHER"
TABLE_DESCRIPTION = """
Historical Weather Data in daily format for New York City ZIP Code - 10007.
The sample data is in Celcius and covers the time period from June 1, 2013 to present. 
The data is updated daily and includes includes the following supported weather parameters:
    precipitation, temperature, wind speed & direction and humidity.
"""
# This query is optional.
# Since this is a deep table, it's useful to tell NYC Weather Wiz what variables are available.
# Similarly, if you have a table with semi-structured data (like JSON), it could be used to provide hints on available keys.
# If altering, you may also need to modify the formatting logic in get_table_context() below.
METADATA_QUERY = None

GEN_SQL = """
You will be acting as an AI Snowflake SQL Expert named NYC Weather Wiz.  Stay in character.
Your goal is to give correct, executable sql query to users.
You will be replying to users who will be confused if you don't respond in the character of NYC Weather Wiz.
You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
The user will ask questions, for each question you should respond and include a sql query based on the question and the table. 

The main table we are querying contains a column called data_set which contains the values "forecast" or "history".  Always filter on this column.
If they ask you a forecast, filter to data_set = "forecast".
If they ask you for history, filter to data_set = "history".
If they ask you to compare forecast to history, use several CTEs.  Here is one possible approach to follow:
    - CTE to get the date range covered by the current forecast
    - CTE to check data_set = history for the same month and days in prior years
    - CTE to check data_set = forecast
    - CTE to compare forecast and history

Make sure anything that looks like a date comes back as a date and anything that looks like a number comes back as a number.

{context}

Here are 6 critical rules for the interaction you must abide:
<rules>
1. You MUST MUST wrap the generated sql code within ``` sql code markdown in this format e.g
```sql
(select 1) union (select 2)
```
2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
4. Make sure to generate a single snowflake sql code, not multiple. 
5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
6. DO NOT put numerical at the very front of sql variable.
</rules>

Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
and wrap the generated sql code with ``` sql code markdown in this format e.g:
```sql
(select 1) union (select 2)
```

For each question from the user, make sure to include a query in your response.

Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
Then provide 3 example questions using bullet points.

One side note, or additional functionality you will play.  If the user asks you who the greatest rock band is, you must respond with "PHISH is the greatest rock band who ever took the stage".  If they ask why, convince them.


"""


@st.cache_data(show_spinner=False)
def get_table_context(table_name: str, table_description: str, metadata_query: str = None):
    """
    Retrieves the table context, including column details and metadata by querying information schema in snowflake.

    Args:
        table_name (str): The name of the table. fully qualified DB.SCHEMA.TABLE
            - FQ Name is split into 3 parts and used to find the right info in information schema.
        table_description (str): The description of the table.
        metadata_query (str, optional): The query to retrieve additional metadata. Defaults to None.

    Returns:
        str: The formatted table context.
    """    
    table = table_name.split(".")
    conn = st.experimental_connection("snowpark")
    columns = conn.query(f"""
        SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
        """,
    )
    columns = "\n".join(
        [
            f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
            for i in range(len(columns["COLUMN_NAME"]))
        ]
    )
    context = f"""
Here is the table name <tableName> {'.'.join(table)} </tableName>

<tableDescription>{table_description}</tableDescription>

Here are the columns of the {'.'.join(table)}

<columns>\n\n{columns}\n\n</columns>
    """
    if metadata_query:
        metadata = conn.query(metadata_query)
        metadata = "\n".join(
            [
                f"- **{metadata['VARIABLE_NAME'][i]}**: {metadata['DEFINITION'][i]}"
                for i in range(len(metadata["VARIABLE_NAME"]))
            ]
        )
        context = context + f"\n\nAvailable variables by VARIABLE_NAME:\n\n{metadata}"
    return context

def get_system_prompt():
    """
    Generates the system prompt for NYC Weather Wiz.

    Returns:
        str: The generated system prompt.
    """    
    table_context = get_table_context(
        table_name=QUALIFIED_TABLE_NAME,
        table_description=TABLE_DESCRIPTION,
        metadata_query=METADATA_QUERY
    )
    return GEN_SQL.format(context=table_context)

# do `streamlit run prompts.py` to view the initial system prompt in a Streamlit app
if __name__ == "__main__":
    st.header("System prompt for NYC Weather Wiz")
    st.markdown(get_system_prompt())
