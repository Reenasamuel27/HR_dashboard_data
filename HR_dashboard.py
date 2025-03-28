import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st
import sqlite3
import time
import hashlib
import plotly.graph_objects as go


#USER CREDENTIALS
if "VALID_USERS" not in st.session_state:
    st.session_state.VALID_USERS = {
        "admin": hashlib.sha256("admin123".encode()).hexdigest(),
        "hr_manager": hashlib.sha256("hr2024".encode()).hexdigest(),
        "employee1": hashlib.sha256("emp5678".encode()).hexdigest()
    }

#STYLE CUSTOMIZATION

# Apply custom CSS for sidebar background color
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background: url("https://img.freepik.com/premium-photo/light-blue-white-gradient-white-background_929087-7035.jpg?semt=ais_hybrid") no-repeat center center fixed;
            background-size: cover;
            color: #343434 !important;  /* White Text */
        }
        section[data-testid="stSidebar"] * {
            color: #343434 !important;  /* Ensures all text inside is white */
        }
    </style>
    """,
    unsafe_allow_html=True
)

#Coustom for Visual side Background
st.markdown(
    """
    <style>
        .stApp {
            background: url("https://www.aihr.com/wp-content/uploads/hrm-basics-cover.png") no-repeat center center fixed;
            background-size: cover;
        }

    </style>
    """,
    unsafe_allow_html=True
)
#AUTHENTICATION FUNCTION
def authenticate_user():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.username = ""

    with st.sidebar:
        st.header("🔐Login")
        user = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")

        if st.button("Login"):
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user in st.session_state.VALID_USERS and st.session_state.VALID_USERS[user] == hashed_password:
                st.session_state.authenticated = True
                st.session_state.username = user
                st.success(f"✅ Welcome, {user}!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("❌ Invalid credentials")

# Forgot Password Option
        if st.button("Forgot Password?"):
            st.session_state.show_reset = True
            st.rerun()

    return st.session_state.authenticated

#OGOUT FUNCTION
def logout():
    for key in ["authenticated", "username"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

#RESET PASSWORD FUNCTION
def reset_password():
    with st.sidebar:
        st.header("🔑 Reset Password")
        username = st.text_input("Enter your Username")

        if username in st.session_state.VALID_USERS:
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.button("Reset Password"):
                if new_password and confirm_password:
                    if new_password == confirm_password:
#Store the new hashed password
                        st.session_state.VALID_USERS[username] = hashlib.sha256(new_password.encode()).hexdigest()
                        st.success("✅ Password Reset Successfully! Please login again.")
                        time.sleep(1)
                        del st.session_state["show_reset"]
                        st.rerun()
                    else:
                        st.error("❌ Passwords do not match!")
                else:
                    st.warning("⚠️ Please enter a valid password!")
        elif username:
            st.error("❌ Username not found! Please check your username.")

        if st.button("🔙 Back to Login"):
            del st.session_state["show_reset"]
            st.rerun()

#CHECK LOGIN STATUS
if "show_reset" in st.session_state and st.session_state.show_reset:
    reset_password()
    st.stop()

authenticated = authenticate_user()
if not authenticated:
    st.warning("🔒 Please log in to view the dashboard.")
    st.stop()

#SHOW DASHBOARD AFTER LOGIN
st.write(f"👤 **User:** {st.session_state.username}")

# Sidebar navigation
page= st.sidebar.radio("Navigation", ["Home","Employee details","payroll"])

#ADD LOGOUT BUTTON
with st.sidebar:
    st.divider()
    if st.button("🚪 Logout"):
        logout()


# Apply custom CSS for sidebar background color
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            background: url("https://png.pngtree.com/thumb_back/fh260/background/20210926/pngtree-watercolor-ink-background-with-blue-pastel-image_907645.png") no-repeat center center fixed;
            background-size: cover;
            color: #343434 !important;  /* White Text */
        }
        section[data-testid="stSidebar"] * {
            color: #343434 !important;  /* Ensures all text inside is white */
        }
    </style>
    """,
    unsafe_allow_html=True
)

## Coustom for Visual side Background
st.markdown(
    """
    <style>
        .stApp {
            background: url("https://png.pngtree.com/thumb_back/fh260/background/20210926/pngtree-watercolor-ink-background-with-blue-pastel-image_907645.png") no-repeat center center fixed;
            background-size: cover;
        }

    </style>
    """,
    unsafe_allow_html=True
)

#Read CSV data 
employee_data = pd.read_csv("Employee_Details.csv")
attendance_data  = pd.read_csv("Attendance.csv")
payroll_data  = pd.read_csv("Payroll.csv")
performance_data = pd.read_csv("Performance.csv")

#convert date to datetime
attendance_data["Date"]= pd.to_datetime(attendance_data["Date"])
payroll_data["Payment_Date"]=pd.to_datetime(payroll_data["Payment_Date"])
performance_data["Review_Date"]=pd.to_datetime(performance_data["Review_Date"])

#Handle null and duplicate value
employee_data.dropna()
attendance_data.dropna()
payroll_data.dropna()
performance_data.dropna()

employee_data.drop_duplicates()
attendance_data.drop_duplicates()
payroll_data.drop_duplicates()
performance_data.drop_duplicates()

# Home Page
if page == "Home":
    st.markdown("<h1 style='color: black; font-size: 30px;'>Welcome to the HR Dashboard</h1>", unsafe_allow_html=True)
# overall employee count
    st.subheader("Overall Employee")
    overall_count = employee_data['Employee_ID'].count()
    st.metric("Total Employees", overall_count)

#Department wise count
    col1, col2 = st.columns(2)
    with col1:
        department_count = employee_data['Department'].value_counts().reset_index()
        department_count.columns = ['Department', 'Count']
        fig = px.bar(department_count,x='Department', y='Count', color_discrete_sequence=["blue"],  text='Count', title='Employee Count-Department')
        fig.update_traces(textposition='outside', width=[0.4] * len(department_count))
        fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
        font=dict(color="white"),  # White text for better visibility
)
        st.plotly_chart(fig) 
#Gender wise count 
    with col2:
        Gender_count = employee_data['Gender'].value_counts().reset_index()
        Gender_count.columns = ['Gender', 'Count']
        fig = px.bar(Gender_count,  x='Gender', y='Count', color_discrete_sequence=["blue"], text='Count',title='Employee Count-Gender')
        fig.update_traces(textposition='outside', width=[0.3] * len(department_count))
        fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
        font=dict(color="white"),  # White text for better visibility
)
        st.plotly_chart(fig)        
        
#Job wise count
    col3, col4 = st.columns(2)
    with col3:
        job_details = employee_data['Job_Title'].value_counts().reset_index()
        job_details.columns = ['Job_Title', 'Count']
        fig_pie = px.pie(job_details, names='Job_Title',values='Count', color_discrete_sequence=["#1E90FF","#0000CD","#000080","#1E90FF","#4169E1"],  title='Job Title Distribution',hole=0.0)# Optional for a donut-style chart
        fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
        font=dict(color="white"),  # White text for better visibility
)

        st.plotly_chart(fig_pie, use_container_width=True)        
       
#Year wise payment 
    with col4:
        payroll_data['Year'] = pd.to_datetime(payroll_data['Payment_Date']).dt.year
        payment_details = payroll_data['Year'].value_counts().reset_index()
        payment_details.columns = ['Year', 'Count']
        fig_pie = px.pie(payment_details,  names='Year', values='Count', color_discrete_sequence=["blue"], title='Yearly Payment Distribution',hole=0.6 )
        fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
        font=dict(color="white"),  # White text for better visibility
)
        st.plotly_chart(fig_pie, use_container_width=True)       
    
#Country wise count 
    Country_count = employee_data['Country'].value_counts().reset_index()
    Country_count.columns = ['Country', 'Count']
    fig = px.bar(Country_count, x='Count', y='Country', color_discrete_sequence=["blue"], text='Count',title='Employee Count Per Country')
    fig.update_traces(textposition='outside', width=[0.0] * len(Country_count))  
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
        font=dict(color="white"),  # White text for better visibility
)
    st.plotly_chart(fig, use_container_width=True)           


elif page == "Employee details":
  
    # Search Box (Only Appears in 'Employee Details' Page)
    emp_id = st.selectbox("Select Employee ID",employee_data["Employee_ID"].unique())
    employee_data["Full_Name"] = employee_data["First_Name"] + " " + employee_data["Last_Name"]

    if emp_id != "Select":
       # Filter DataFrame based on input Employee ID
        filtered_employee_data = employee_data[employee_data['Employee_ID'] == emp_id]   
        
        if not filtered_employee_data.empty:
            Name = filtered_employee_data['Full_Name'].values[0]  
            Dep = filtered_employee_data['Department'].values[0]  
            Job = filtered_employee_data['Job_Title'].values[0]  
            joining_date = filtered_employee_data['Date_of_Joining'].values[0]
            Gender = filtered_employee_data['Gender'].values[0]
            Job_Type = filtered_employee_data['Employment_Type'].values[0]
            DOB = filtered_employee_data['Date_of_Birth'].values[0]
            Contact_details = filtered_employee_data['Contact_Number'].values[0]
            Email_Address = filtered_employee_data['Email'].values[0]
            Location = filtered_employee_data['Country'].values[0]
            Permenent_Address = filtered_employee_data['Address'].values[0]


# show the result of employee details

            st.markdown("<h1 style='color: black; font-size: 15px;'>Profile</h1>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                st.success(f"Name : {Name}")
            with col2: 
                st.success(f"Department : {Dep}")
            with col3:
                st.success(f"Job Roll : {Job}")
                
            col4, col5, col6 = st.columns(3)
            with col4:
                st.success(f"Date of Joining : {joining_date}")
            with col5:    
                st.success(f"Gender : { Gender }")
            with col6:    
                st.success(f"Job Type : { Job_Type }")

            st.markdown("<h1 style='color: black; font-size: 15px;'>Personal Details</h1>", unsafe_allow_html=True)
            col7, col8, col9 = st.columns(3)
            with col7:
                st.success(f"data of Birth : {DOB}")
            with col8:
                st.success(f"Contact Details : {Contact_details}")
            with col9:
             st.success(f"Email Address : {Email_Address}")

            col10, col11, col12 = st.columns(3)
            with col10:
                st.success(f"Location : {Location}")
            with col11:
                st.success(f"Address : { Permenent_Address}")
        else:
            st.error("❌ Employee ID not found! Please check the ID.")

elif page == "payroll":

    # Overall company payroll average   
    st.subheader("Payroll Insights")
    avg_salary = payroll_data['Net_Salary'].mean()
    st.metric("Average Salary", f"{avg_salary:,.2f}")


#Dropdown selection bar for select employee details 
    emp_id = st.selectbox("Select Employee ID", payroll_data["Employee_ID"].unique())
    col1, col2 = st.columns(2)
    if emp_id != "Select":  
            filtered_payroll_data = payroll_data[payroll_data['Employee_ID'] == emp_id]


#Show the employee payment ID details
    with col1: 
            if not filtered_payroll_data.empty:
                Payment_ID = filtered_payroll_data['Payroll_ID'].values[0]  
                st.success(f"Payroll ID:{Payment_ID}")

#Net salary and Gross payment details pie chart 

                Salary_details = filtered_payroll_data[['Net_Salary', 'Deductions', 'Bonuses', 'Basic_Salary']].melt(var_name="Salary_Component", value_name="Amount")
                fig_pie = px.pie(Salary_details, names='Salary_Component', values='Amount',
                color_discrete_sequence=["#1E90FF","#0000CD","#000080","#1E90FF"], 
                title='Payslip Details', 
                hole=0.6)
                fig_pie.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',  # Transparent plot background
                paper_bgcolor='rgba(0,0,0,0)',  # Transparent figure background
                font=dict(color="white"),  # White text for better visibility
)
                st.plotly_chart(fig_pie, use_container_width=True)          

#Show the salary values
                Net_Salary = filtered_payroll_data['Net_Salary'].values[0]  
                Basic_Salary = filtered_payroll_data['Basic_Salary'].values[0]  
                Deductions = filtered_payroll_data['Deductions'].values[0]      
                Bonuses = filtered_payroll_data['Bonuses'].values[0]      
         
            if st.button("Show More"):
                st.success(f"Net Salary : {Net_Salary}")
                st.success(f"Basic Salary : {Basic_Salary}")
                st.success(f"Deductions : {Deductions}")
                st.success(f"Bonuses : {Bonuses}") 
    
            else:
                st.write("Net Salary: ***") 
                st.write("Basic Salary: ***") 
                st.write("Deductions: ***") 
                st.write("Bonuses: ***") 

       
        
        
        
         
   
        
    
       
       
       
   
    


    









    
   
