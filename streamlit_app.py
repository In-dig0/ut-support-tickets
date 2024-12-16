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

def upload_pdf_file():
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
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        rec_out =    {
                    "Atch_name": uploaded_file.name,
                    "Atch_type": "GENERIC",
                    "Atch_link": " ",                    
                    "Atch_data": bytes_data,
                }
    st.divider()              
    return rec_out       

def check_request_fields(record: dict) -> bool:
    res = all(record.values())
    return res

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
    finally:
        cursor.close()

def save_request_to_sqlitecloud(row:dict, atch: dict) -> None:
    """ Save applog into SQLite Cloud Database """
    rc = 0
    req_nr = dict()
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
        st.error(f"**ERROR inserting row in tab TORP_REQUESTS: \n{errMsg}", icon="🚨")
        rc = 1
    else:
        conn.commit()
        req_nr = f"R-{str(next_rowid).zfill(4)}"
        rc = 0
    if len(atch) > 0:
    # Setup sqlcode for inserting applog as a new row
        sqlcode = """INSERT INTO TORP_ATTACHMENTS (a_type, a_title, a_link, a_data, a_reqid) 
                VALUES (?, ?, ?, ?, ?);
                """  
            # Setup row values
        values = (atch["Atch_name"], atch["Atch_type"], atch["Atch_link"], atch["Atch_data"], next_rowid)
        try:
            cursor.execute(sqlcode, values)
        #    cursor.lastrowid
        except Exception as errMsg:
            st.error(f"**ERROR inserting row in tab TORP_ATTACHMENTS: \n{errMsg}", icon="🚨")
            rc = 1
        else:
            conn.commit()
    
    cursor.close()    
    if conn:
        conn.close()

    return req_nr, rc    

##################################
# import sqlite3

# def convertToBinaryData(filename):
#     # Convert digital data to binary format
#     with open(filename, 'rb') as file:
#         blobData = file.read()
#     return blobData

# def insertBLOB(empId, name, photo, resumeFile):
#     try:
#         sqliteConnection = sqlite3.connect('SQLite_Python.db')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")
#         sqlite_insert_blob_query = """ INSERT INTO new_employee
#                                   (id, name, photo, resume) VALUES (?, ?, ?, ?)"""

#         empPhoto = convertToBinaryData(photo)
#         resume = convertToBinaryData(resumeFile)
#         # Convert data into tuple format
#         data_tuple = (empId, name, empPhoto, resume)
#         cursor.execute(sqlite_insert_blob_query, data_tuple)
#         sqliteConnection.commit()
#         print("Image and file inserted successfully as a BLOB into a table")
#         cursor.close()

#     except sqlite3.Error as error:
#         print("Failed to insert blob data into sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("the sqlite connection is closed")

# insertBLOB(1, "Smith", "E:\pynative\Python\photos\smith.jpg", "E:\pynative\Python\photos\smith_resume.txt")
# insertBLOB(2, "David", "E:\pynative\Python\photos\david.jpg", "E:\pynative\Python\photos\david_resume.txt")
################################

###############################
# import sqlite3

# def writeTofile(data, filename):
#     # Convert binary data to proper format and write it on Hard Disk
#     with open(filename, 'wb') as file:
#         file.write(data)
#     print("Stored blob data into: ", filename, "\n")

# def readBlobData(empId):
#     try:
#         sqliteConnection = sqlite3.connect('SQLite_Python.db')
#         cursor = sqliteConnection.cursor()
#         print("Connected to SQLite")

#         sql_fetch_blob_query = """SELECT * from new_employee where id = ?"""
#         cursor.execute(sql_fetch_blob_query, (empId,))
#         record = cursor.fetchall()
#         for row in record:
#             print("Id = ", row[0], "Name = ", row[1])
#             name = row[1]
#             photo = row[2]
#             resumeFile = row[3]

#             print("Storing employee image and resume on disk \n")
#             photoPath = "E:\pynative\Python\photos\db_data\\" + name + ".jpg"
#             resumePath = "E:\pynative\Python\photos\db_data\\" + name + "_resume.txt"
#             writeTofile(photo, photoPath)
#             writeTofile(resumeFile, resumePath)

#         cursor.close()

#     except sqlite3.Error as error:
#         print("Failed to read blob data from sqlite table", error)
#     finally:
#         if sqliteConnection:
#             sqliteConnection.close()
#             print("sqlite connection is closed")

# readBlobData(1)
# readBlobData(2)




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