import streamlit as st
from python_terraform import *

from datashack.datashack_app.infra_explore_page import get_tf_vars_dict


def my_infra():
    with st.spinner("Configuring"):
        terraform = Terraform()
        terraform.init()
        if os.getcwd().rsplit("/", 1)[1] != "local":
            os.chdir("terraform/environments/local")
    if st.button("Click here to plan infra"):
        with st.spinner("Planning"):
            return_code, stdout, stderr = terraform.plan(var=get_tf_vars_dict())
            st.text(stdout)
    if st.button("Click here to apply infra"):
        with st.spinner("Applying"):
            return_code, stdout, stderr = terraform.apply(var=get_tf_vars_dict(),skip_plan=True)
            st.text(stdout)
    if st.button("Click here to destory infra"):
        with st.spinner("Destroying"):
            return_code, stdout, stderr = terraform.destroy(var=get_tf_vars_dict())
            st.text(stdout)