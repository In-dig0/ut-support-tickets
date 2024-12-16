import datetime
import os
import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import sqlitecloud
import pytz 
import io 

APPNAME = "TORP" #IPH Technical Office Request POC (Proof Of Concept)
APPCODE = "TORP"

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
                    "Req_detail": req_detail
                }
    return rec_out 

def upload_pdf_file() -> None:
    """ Widget used to upload an xml file """
    uploaded_file = st.file_uploader("Choose a PDF file:", type="pdf", accept_multiple_files=False)
    return uploaded_file

def display_attachment_section() -> dict:
    """ Show a section to upload attachments """
    rec_out = dict()
    st.header(":orange[Add an attachment (only PDF file)]")
    with st.container():
        uploaded_file = upload_pdf_file()
    if uploaded_file is not None:
        buffer = ""
        rec_out =    {
                    "Atch_name": uploaded_file.name,
                    "Atch_type": "GENERIC",
                    "Atch_link": " ",                    
                    "Atch_data": buffer,
                }
    st.divider()              
    return rec_out       

def check_request_fields(record: dict) -> bool:
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

def save_applog_to_sqlitecloud(log_values:dict) -> None:
    """ Save applog into SQLite Cloud Database """

    db_link = ""
    db_apikey = ""
    db_name = ""
    # Get database information
    try:
        #Search DB credentials using OS.GETENV
        db_link = os.getenv("SQLITECLOUD_DBLINK")
        db_apikey = os.getenv("SQLITECLOUD_APIKEY")
        db_name = os.getenv("SQLITECLOUD_DBNAME")
    except st.StreamlitAPIException as errMsg:
        try:
            #Search DB credentials using ST.SECRETS
            db_link = st.secrets["SQLITE_DBLINK"]
            db_apikey = st.secrets["SQLITE_APIKEY"]
            db_name = st.secrets["SQLITE_DBNAME"]
        except st.StreamlitAPIException as errMsg:
            st.error(f"**ERROR: DB credentials NOT FOUND: \n{errMsg}", icon="🚨")
    
    conn_string = "".join([db_link, db_apikey])
    # Connect to SQLite Cloud platform
    try:
        conn = sqlitecloud.connect(conn_string)
    except Exception as errMsg:
        st.error(f"**ERROR connecting to database: \n{errMsg}", icon="🚨")
    
    # Open SQLite database
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.cursor()
    
    # Setup sqlcode for inserting applog as a new row
    sqlcode = """INSERT INTO applog (appname, applink, appcode, apparam, appstatus, appmsg, cpudate) 
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        
    rome_tz = pytz.timezone('Europe/Rome')
    rome_datetime = rome_tz.localize(datetime.datetime.now()) 
    cpudate = rome_datetime.strftime("%Y-%m-%d %H:%M:%S")
    values = (log_values["appname"], log_values["applink"], log_values["appcode"], log_values["apparam"], log_values["appstatus"], log_values["appmsg"], cpudate)
    try:
        cursor.execute(sqlcode, values)
    except Exception as errMsg:
        st.error(f"**ERROR inserting new applog row: \n{errMsg}", icon="🚨")
    else:
        conn.commit()
        #row = cursor.fetchone()
        #st.write(f"LAST ROW APPLOG: {row}") 
    finally:
        cursor.close()

def save_request_to_sqlitecloud(row:dict, atch: dict) -> None:
    """ Save applog into SQLite Cloud Database """
    rc = 0
    db_link = ""
    db_apikey = ""
    db_name = ""
    # Get database information
    try:
        #Search DB credentials using OS.GETENV
        db_link = os.getenv("SQLITECLOUD_DBLINK")
        db_apikey = os.getenv("SQLITECLOUD_APIKEY")
        db_name = os.getenv("SQLITECLOUD_DBNAME")
    except st.StreamlitAPIException as errMsg:
        try:
            #Search DB credentials using ST.SECRETS
            db_link = st.secrets["SQLITE_DBLINK"]
            db_apikey = st.secrets["SQLITE_APIKEY"]
            db_name = st.secrets["SQLITE_DBNAME"]
        except st.StreamlitAPIException as errMsg:
            st.error(f"**ERROR: DB credentials NOT FOUND: \n{errMsg}", icon="🚨")
    
    conn_string = "".join([db_link, db_apikey])
    # Connect to SQLite Cloud platform
    try:
        conn = sqlitecloud.connect(conn_string)
    except Exception as errMsg:
        st.error(f"**ERROR connecting to database: \n{errMsg}", icon="🚨")
    
    # Open SQLite database
    conn.execute(f"USE DATABASE {db_name}")
    cursor = conn.cursor()
    
    # Setup sqlcode for inserting applog as a new row
    sqlcode = """INSERT INTO TORP_REQUESTS (r_id, r_dept, r_requester, r_pline, r_pfamily, r_priority, r_type, r_category, r_title, r_detail, r_insdate) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
            """    
    # Calculate the next rowid
    cursor.execute('SELECT MAX(r_id) FROM TORP_REQUESTS')
    max_rowid = cursor.fetchone()[0]
    next_rowid = (max_rowid + 1) if max_rowid is not None else 1
     
    # Setup row values
    values = (next_rowid, row["Req_dept"], row["Req_user"], row["Prd_line"], row["Prd_family"], row["Req_priority"], row["Req_type"], row["Req_category"], row["Req_title"], row["Req_detail"], row["Req_insdate"])
    try:
        cursor.execute(sqlcode, values)
    #    cursor.lastrowid
    except Exception as errMsg:
        st.error(f"**ERROR inserting row: \n{errMsg}", icon="🚨")
        rc = 1
    else:
        conn.commit()
        #row = cursor.fetchone()
        #st.write(f"LAST ROW APPLOG: {row}") 
    finally:
        cursor.close()
        conn.close()
    
    req_nr = f"R-{str(next_rowid).zfill(4)}"
    return req_nr, rc    

def main() -> None:
    if 'submit_clicked' not in st.session_state:
        st.session_state.submit_clicked = False
    display_app_title()
    rec_user = display_user_section()
    rec_pgroup = display_productgroup_section()
    rec_req = display_request_section()
    rec_attchment = display_attachment_section() 
    rec_request = rec_user | rec_pgroup | rec_req
    insdate = datetime.datetime.now().strftime("%Y-%m-%d")
    rec_request["Req_insdate"] = insdate
    st.button("Submit", type="primary", on_click=click_submit_button)
    if st.session_state.submit_clicked:
        if check_request_fields(rec_request):
            nr_req = ""
            applog = dict()
            nr_req, rc = save_request_to_sqlitecloud(rec_request, rec_attchment)
            if rc == 0:
                # Creare una lista di tuple chiave-valore
                items = list(rec_request.items())
                # Inserire la nuova coppia chiave-valore nella prima posizione
                items.insert(0, ("Req_nr", nr_req))
                # Convertire di nuovo la lista in un dizionario
                rec_request = dict(items)
                st.write(f"Request {nr_req} submitted! Here are the ticket details:")
                df_request = pd.DataFrame([rec_request])
                st.dataframe(df_request, use_container_width=True, hide_index=True)
                applog["appstatus"] = "COMPLETED"
                applog["appmsg"] = " "
            else:
                applog["appstatus"] = "ERROR"
                applog["appmsg"] = "TABLE TORP_REQUESTS: UNIQUE CONSTRAIN ON FIELD r_title"    
            
            applog["appname"] = APPNAME
            applog["applink"] = __file__
            applog["appcode"] = APPCODE
            applog["apparam"] = str(rec_request)
            save_applog_to_sqlitecloud(applog)           
        else:
            st.write(":red-background[**ERROR: please fill all mandatory fields (:red[*])]")



if __name__ == "__main__":
    main()