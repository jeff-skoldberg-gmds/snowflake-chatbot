# NYC Weather Wiz: Build a LLM Chatbot in Streamlit on your Snowflake Data


## Overview

This guide was adapted from:
https://github.com/Snowflake-Labs/sfguide-frosty-llm-chatbot-on-streamlit-snowflake/tree/main

Full tutorial is found here:
https://quickstarts.snowflake.com/guide/frosty_llm_chatbot_on_streamlit_snowflake/#0

In this guide, we will build an LLM-powered chatbot named "NYC Weather Wiz" that performs data exploration and question answering by writing and executing SQL queries on Snowflake data. The application uses Streamlit and Snowflake and can be plugged into your LLM of choice, alongside data from Snowflake Marketplace. By the end of the session, you will have an interactive web application chatbot which can converse and answer questions based on a public job listings dataset.


## Run the app

Once environment is set up and secrets are configured including connection to a Snowflake environment with the relevant view, the app can be run by:

```sh
streamlit run src/nyc_weather_wiz.py
```
