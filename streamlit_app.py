import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

def display_app_title() -> None:
    """ Show app title and description """
    st.set_page_config(page_title="New Request", page_icon="🎫")
    st.title("🎫 :blue[New request]")
    st.write(
        """
        This app shows how you can build an internal tool in Streamlit. Here, we are 
        implementing a support ticket workflow. The user can create a ticket, edit 
        existing tickets, and view some statistics.
        """
    )
    st.markdown("Powered with Streamlit :streamlit:")
    st.divider()


def display_user_section() -> dict:
    """ Show a section to declare the user informations """
    req_department = ""
    req_user = ""
    with st.container():
        st.header(":orange[User informations]")
        req_dept_values_00 = ["DMN-ACCOUNTING", "DTD-DESIGN TECHNICAL DEPARTMENT", "COMMERCIALE AFTER MARKET"]
        req_department = st.selectbox(":blue[Requester Department(:red[*])]", req_dept_values_00, index=None)
        if req_department == "DMN-ACCOUNTING":
            req_user_values_01 = ["COMELLINI GIORGIO", "ROMANI CORRADO", "ROSSI PAOLA"]
            req_user = st.selectbox(":blue[Requester User(:red[*])]", req_user_values_01, index=None)
        elif req_department == "DTD-DESIGN TECHNICAL DEPARTMENT":
            req_user_values_02 = ["CARLINI MICHELE", "FENARA GABRIELE", "PALMA NICOLA"]
            req_user = st.selectbox(":blue[Requester User(:red[*])]", req_user_values_02, index=None)
        elif req_department == "COMMERCIALE AFTER MARKET":
            req_user_values_03 = ["GIORGI IVAN", "ANGOTTI FRANCESCO", "BALDINI ROBERTO"]
            req_user = st.selectbox(":blue[Requester User(:red[*])]", req_user_values_03, index=None)
    st.divider()    
    rec_out =    {
                     "Req_dept": req_department,
                     "Req_user": req_user
                 }
           
    return rec_out        


def display_productgroup_section() -> dict:
    """ Show a section to declare the product group informations """
    
    product_line = ""
    product_family = ""
    with st.container():
        st.header(":orange[Product group informations]")
        product_line_values_00 = ["POWER TAKE OFFs", "HYDRAULICS", "CYLINDERS", "ALL"]
        product_line = st.selectbox(":blue[Product line(:red[*])]", product_line_values_00, index=None)
        if product_line == "POWER TAKE OFFs":
            product_line_values_01 = ["GEARBOX PTO", "ENGINE PTO", "SPLIT SHAFT PTO", "PARALLEL GEARBOXES"]
            product_family = st.selectbox(":blue[Product family(:red[*])]", product_line_values_01, index=None)
        elif product_line == "HYDRAULICS":
            product_line_values_02 = ["PUMPS", "MOTORS", "VALVES", "WET KITS"]
            product_family = st.selectbox(":blue[Product family(:red[*])]", product_line_values_02, index=None)
        elif product_line == "CYLINDERS":
            product_line_values_03 = ["FRONT-END CYLINDERS", "UNDERBODY CYLINDERS", "DOUBLE ACTING CYLINDERS", "BRACKETS FOR CYLINDERS"]
            product_family = st.selectbox(":blue[Product family(:red[*])]", product_line_values_03, index=None)
    st.divider()       
    rec_out =    {
                     "Prd_line": product_line,
                     "Prd_family": product_family
                 }
    return rec_out 


def display_request_section() -> dict:
    """ Show a section to declare the request informations """
    req_type = ""
    req_category = ""
    st.header(":orange[Add a request]")
    with st.container():
        priority_values_00 = ["High", "Medium", "Low"]
        req_priority = st.selectbox(":blue[Priority]", priority_values_00, index=1)
        type_values_00 = ["DOCUMENTATION", "PRODUCT", "SERVICE"]
        req_type = st.selectbox(":blue[Request type (:red[*])]", type_values_00, index=None)
        if req_type == "PRODUCT":
            category_01 = ["NEW PRODUCT", "PRODUCT CHANG", "OBSOLETE PRODUCT", "PRODUCT VALIDATION"]
            req_category = st.selectbox(":blue[Request category(:red[*])]", category_01, index=None)
        elif req_type == "DOCUMENTATION":
            category_02 = ["WEBPTO", "DRAWING", "IMDS (INTERNATIONAL MATERIAL DATA SYSTEM)", "CATALOGUE"]
            req_category = st.selectbox(":blue[Request category(:red[*])]", category_02, index=None)
        elif req_type == "SERVICE":
            category_03 = ["VISITING CUSTOMER PLANT", "VISITING SUPPLIER PLANT"]
            req_category = st.selectbox(":blue[Request category(:red[*])]", category_03, index=None)
        req_title = st.text_input(":blue[Request title(:red[*])]")
        req_detail = st.text_area(":blue[Request details(:red[*])]", key="req_det")
    st.divider()   
    rec_out =    {
                    "Req_priority": req_priority, 
                    "Req_type": req_type,
                    "Req_category": req_category,                    
                    "Req_title": req_title,
                    "Req_info": req_detail
                }
    return rec_out 

def check_ticket_fields(record: dict) -> bool:
    res = all(record.values())
    return res


# if "my_text" not in st.session_state:
#     st.session_state.my_text = ""

# def submit():
#     st.session_state.my_text = st.session_state.widget
#     st.session_state.widget = ""

# st.text_input("Enter text here", key="widget", on_change=submit)

# my_text = st.session_state.my_text

# st.write(my_text)


# def display_ticket_section() -> pd.DataFrame:
#     """ """


#     # We're adding tickets via an `st.form` and some input widgets. If widgets are used
#     # in a form, the app will only rerun once the submit button is pressed.
#     with st.form("add_ticket_form"):
#         req_type = ""
#         req_category = ""
#         req_type = st.selectbox("Request type (:red[*])",["DOCUMENTATION", "PRODUCT", "SERVICE"], index=None)
#         if req_type == "PRODUCT":
#             req_category = st.selectbox("Request category(:red[*])", ["NEW PRODUCT", "PRODUCT CHANG", "OBSOLETE PRODUCT", "PRODUCT VALIDATION"], index=None)
#         elif req_type == "DOCUMENTATION":
#             req_category = st.selectbox("Request category(:red[*])", ["WEBPTO", "DRAWING", "IMDS (INTERNATIONAL MATERIAL DATA SYSTEM)", "CATALOGUE"], index=None)
#         elif req_type == "SERVICE":
#             req_category = st.selectbox("Request category(:red[*])", ["VISITING CUSTOMER PLANT", "VISITING SUPPLIER PLANT"], index=None)
#         req_title = st.text_input("Request title(:red[*])")
#         req_info = st.text_area("Request details(:red[*])")
#         req_priority = st.selectbox("Priority", ["High", "Medium", "Low"], index=1)
#         df_out = pd.DataFrame(
#              [
#                  {
#                      "Req_type": req_type,
#                      "Req_category": req_category,
#                      "Req_priority": req_info,                     
#                      "Req_title": req_title,
#                      "Req_info": req_info
#                  }
#              ]
#          )        
#         submitted = st.form_submit_button("Submit")

#     if submitted:
#     #     # Make a dataframe for the new ticket and append it to the dataframe in session
#     #     # state.
#         last_ticket_number = 10
#         today = datetime.datetime.now().strftime("%m-%d-%Y")
#         df_new = pd.DataFrame(
#              [
#                  {
#                      "ID": f"TICKET-{last_ticket_number+1}",
#                      "Title": request_title,
#                      "Status": "Open",
#                      "Priority": priority,
#                      "Date Submitted": today,
#                  }
#              ]
#          )

#     #     # Show a little success message.
#         st.write("Ticket submitted! Here are the ticket details:")
#         st.dataframe(df_new, use_container_width=True, hide_index=True)
#        st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)

    # # Show section to view and edit existing tickets in a table.
    # st.header("Existing tickets")
    # st.write(f"Number of tickets: `{len(st.session_state.df)}`")

    # st.info(
    #     "You can edit the tickets by double clicking on a cell. Note how the plots below "
    #     "update automatically! You can also sort the table by clicking on the column headers.",
    #     icon="✍️",
    # )

    # # Show the tickets dataframe with `st.data_editor`. This lets the user edit the table
    # # cells. The edited data is returned as a new dataframe.
    # edited_df = st.data_editor(
    #     st.session_state.df,
    #     use_container_width=True,
    #     hide_index=True,
    #     column_config={
    #         "Status": st.column_config.SelectboxColumn(
    #             "Status",
    #             help="Ticket status",
    #             options=["Open", "In Progress", "Closed"],
    #             required=True,
    #         ),
    #         "Priority": st.column_config.SelectboxColumn(
    #             "Priority",
    #             help="Priority",
    #             options=["High", "Medium", "Low"],
    #             required=True,
    #         ),
    #     },
    #     # Disable editing the ID and Date Submitted columns.
    #     disabled=["ID", "Date Submitted"],
    # )

# # Show some metrics and charts about the ticket.
# st.header("Statistics")

# # Show metrics side by side using `st.columns` and `st.metric`.
# col1, col2, col3 = st.columns(3)
# num_open_tickets = len(
#     st.session_state.df[st.session_state.df.Status == "Open"])
# col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
# col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
# col3.metric(label="Average resolution time (hours)", value=16, delta=2)

# # Show two Altair charts using `st.altair_chart`.
# st.write("")
# st.write("##### Ticket status per month")
# status_plot = (
#     alt.Chart(edited_df)
#     .mark_bar()
#     .encode(
#         x="month(Date Submitted):O",
#         y="count():Q",
#         xOffset="Status:N",
#         color="Status:N",
#     )
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

# st.write("##### Current ticket priorities")
# priority_plot = (
#     alt.Chart(edited_df)
#     .mark_arc()
#     .encode(theta="count():Q", color="Priority:N")
#     .properties(height=300)
#     .configure_legend(
#         orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
#     )
# )
# st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")

def click_submit_button():
    st.session_state.submit_clicked = True

def clear_text(t_txt):
    st.session_state[t_txt] = ""

def main() -> None:
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False

    display_app_title()
    rec_user = display_user_section()
    rec_pgroup = display_productgroup_section()
    rec_req = display_request_section() 
    rec_request = rec_user | rec_pgroup | rec_req
    cpudate = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    rec_request["Insert_date"] = cpudate
    st.button("Submit", type="primary", on_click=click_submit_button)
    if st.session_state.submit_clicked:
        if check_ticket_fields(rec_request):
            df_request = pd.DataFrame([rec_request])
            st.write("Ticket submitted! Here are the ticket details:")
            st.dataframe(df_request, use_container_width=True, hide_index=True)
            
        else:
            st.write(":red-background[**ERROR: please fill all mandatory fields (:red[*])]")



if __name__ == "__main__":
    main()