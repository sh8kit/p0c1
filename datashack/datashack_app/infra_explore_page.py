import os
import streamlit as st
from functools import lru_cache
from python_terraform import Terraform
from presto_utils import get_table_sample
from states_conf import *


@lru_cache()
def get_table_from_file_name(f_name):
    parsed_yaml_name = f_name.split(".")
    table_name = parsed_yaml_name[1]
    db_name = parsed_yaml_name[0].split("_")[1]
    return db_name, table_name


@lru_cache
def get_tf():
    terraform = Terraform()
    terraform.init()
    return terraform


def get_tf_vars_dict():
    return {"presto_host": os.environ.get("presto_host", "localhost"),
            "kafka_connect_host": os.environ.get("kafka_connect_host", "localhost"),
            "minio_host": os.environ.get("minio_host", "localhost"),
            "kafka_bootstarp_server": os.environ.get("kafka_bootstarp_server", "localhost:9092")}


def explore_infra():
    with st.spinner("Configuring"):
        if os.getcwd().rsplit("/", 1)[1] != "local":
            os.chdir("terraform/environments/local")
        terraform = get_tf()

    with st.spinner("Planning"):
        state_return_code, state_stdout, state_stderr = terraform.cmd(cmd="state list")
    if not state_stdout:
        st.markdown("""#### There is no available infra at the moment""")
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

                python -m datashack.cli apply my_app/models local_docker/yamls

                ```
                """)
    else:
        tables_yamls = os.listdir("../../modules/datashack/yamls")

        with st.container():
            st.markdown("# Datashack page status 🏄🏻‍")
        with st.container():
            col1, col2 = st.columns(2)
            with col1:
                st.metric("number of tables", value=len(tables_yamls), delta=len(tables_yamls), delta_color="normal")
            with col2:
                st.metric("data quality ", value="100%", delta="100%", delta_color="normal")
        with st.container():
            st.markdown("""
            
            """)  # just space
        with st.container():
            st.markdown("# Inventory 👷🏽")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**Data location**")
            with col2:
                st.markdown("**Kafka topics**")
            with col3:
                st.markdown("**Consumer**")
            states = state_stdout.split("\n")

            for table_f in tables_yamls:
                db_name, table_name = get_table_from_file_name(table_f)
                # each table have a container
                with st.container():
                    minio_col, kafka_col, consumer_col = st.columns(3)
                    for state in states:
                        if table_f in state:
                            if PrestoTable.is_presto_table(state):
                                with minio_col:
                                    st.markdown(PrestoTable.get_minio_data_location(db_name, table_name))
                            elif KafkaTopic.is_kafka_topic(state):
                                with kafka_col:
                                    st.markdown(KafkaTopic.get_kafka_topic_markdown(table_name))
                            elif KafkaConnector.is_connector(state):
                                with consumer_col:
                                    st.markdown(KafkaConnector.get_connector_markdown(table_name))
        with st.container():
            st.markdown("""

            """)  # just space
        with st.container():
            st.markdown("# Data exploration 🤖")
            st.markdown("[Presto Ui link](http://localhost:8080/ui/)")
            tables_strings = []
            for t in tables_yamls:
                db_name, table_name = get_table_from_file_name(t)
                tables_strings.append(f"{db_name}.{table_name}")
            option = st.selectbox('choose a table', tables_strings)
            if option:
                with st.spinner(f"Loading data for {option}"):
                    df = get_table_sample(option)
                st.table(df)
