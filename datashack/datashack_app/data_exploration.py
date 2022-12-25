import streamlit as st
from presto_utils import get_table_sample, get_tables_from_db


def data_explore():
    st.markdown("# Data exploration page❄️")
    st.markdown("### This page shows your available tables, pick one and it will show a sample of its data")
    st.sidebar.markdown("# Data exploration page❄️")
    with st.spinner("Looking for your tables 🧐"):
        tables = get_tables_from_db()
    if tables:
        option = st.selectbox('choose a table 😃', tables)
        with st.spinner(f"Loading data for {option}"):
            df = get_table_sample(option)
        st.table(df)
        if df.empty:
            st.markdown("""#### Table is empty, maybe you should insert some data using .insert() ?""")
    else:
        st.markdown("""#### There is no available tables at the moment""")
        st.markdown("add a new table using Table class")
        st.markdown("""
        ```python
        from datetime import datetime
        from datashack.entities.tables import Table, Column
        
        Users = Table(database='logs', table_name='user_events')
        Users['id'] = Column(str)
        Users['name'] = Column(str)
        Users['email'] = Column(str)
        Users['event_type'] = Column(str)
        Users['event_ts'] = Column(datetime)
        ```
        """)
        st.markdown("and run")
        st.markdown("""
        ```commandline
        
        python -m datashack.cli  generate state my_app/models local_docker/yamls
        
        ```
        """)
