import streamlit as st
import pandas as pd
from datetime import date, datetime

# App Configuration
st.set_page_config(page_title="The Zoo by Bigs", layout="wide")
st.title("Welcome to The Zoo by Bigs")

# Initialize DataFrames
if "barbers" not in st.session_state:
    st.session_state.barbers = pd.DataFrame({
        "Name": ["Bigs", "Mike", "Sam", "Chris", "Leo", "Jay", "Drew", "Eddie", "Tony", "Will",
                 "Frank", "Alex", "Jordan", "Kyle", "Nate", "Oscar", "Victor", "Sean", "Rick", "Tom"],
        "Specialty": ["Fades", "Beards", "Braids", "Dreads", "Lineups", "Tapers", "Shaves", "Coloring", "Kids Cuts", "Designs",
                      "Fades", "Beards", "Braids", "Lineups", "Tapers", "Shaves", "Coloring", "Kids Cuts", "Designs", "Fades"],
        "Experience (Years)": [10, 8, 6, 5, 7, 9, 4, 6, 11, 5, 3, 12, 7, 9, 6, 8, 10, 5, 4, 7],
        "Contact": [f"555-{i:04d}" for i in range(1234, 1254)]
    })

if "clients" not in st.session_state:
    st.session_state.clients = pd.DataFrame({
        "Name": ["John Doe", "Jane Smith", "Paul Johnson", "Sarah Brown", "Michael Davis",
                 "Emily Clark", "Robert Wilson", "Linda Taylor", "James Lee", "Sophia Harris",
                 "Chris Martin", "Olivia Green", "Ethan White", "Mia Carter", "Liam Gray",
                 "Emma Scott", "Noah Adams", "Ava King", "Lucas Moore", "Ella Brooks"],
        "Phone": [f"555-{i:04d}" for i in range(1111, 1131)],
        "Email": [f"client{i}@example.com" for i in range(1, 21)]
    })

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame(columns=["Client Name", "Barber Name", "Date", "Time", "Service"])

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["Dashboard", "Barbers", "Clients", "Bookings"])

# Helper Function: Display Stats
def display_stats():
    avg_exp = st.session_state.barbers["Experience (Years)"].mean()
    total_barbers = len(st.session_state.barbers)
    total_clients = len(st.session_state.clients)
    client_to_barber_ratio = total_clients / total_barbers if total_barbers > 0 else 0

    st.metric("Average Barber Experience", f"{avg_exp:.1f} years")
    st.metric("Total Barbers", total_barbers)
    st.metric("Total Clients", total_clients)
    st.metric("Client-to-Barber Ratio", f"{client_to_barber_ratio:.1f}")

# Dashboard
if menu == "Dashboard":
    st.subheader("Dashboard")
    col1, col2 = st.columns(2)
    with col1:
        display_stats()
    with col2:
        st.write("**Next Booking:**")
        if not st.session_state.bookings.empty:
            next_booking = st.session_state.bookings.sort_values(["Date", "Time"]).iloc[0]
            st.write(next_booking)
        else:
            st.write("No upcoming bookings.")

# Barber Management
elif menu == "Barbers":
    st.subheader("Barber Management")
    tab1, tab2 = st.tabs(["Barber List", "Add Barber"])
    with tab1:
        st.write("**Current Barbers:**")
        search_barber = st.text_input("Search Barbers by Name or Specialty")
        filtered_barbers = st.session_state.barbers[
            st.session_state.barbers.apply(lambda row: search_barber.lower() in row.to_string().lower(), axis=1)
        ]
        st.dataframe(filtered_barbers if search_barber else st.session_state.barbers)
    with tab2:
        name = st.text_input("Name")
        specialty = st.text_input("Specialty")
        experience = st.number_input("Experience (Years)", min_value=0, max_value=50, step=1)
        contact = st.text_input("Contact Information")
        if st.button("Add Barber"):
            if name and specialty and contact:
                new_barber = pd.DataFrame([[name, specialty, experience, contact]],
                                          columns=st.session_state.barbers.columns)
                st.session_state.barbers = pd.concat([st.session_state.barbers, new_barber], ignore_index=True)
                st.success(f"Barber {name} added!")
            else:
                st.error("Please fill all fields.")

# Client Management
elif menu == "Clients":
    st.subheader("Client Management")
    tab1, tab2 = st.tabs(["Client List", "Add Client"])
    with tab1:
        st.write("**Current Clients:**")
        search_client = st.text_input("Search Clients by Name or Email")
        filtered_clients = st.session_state.clients[
            st.session_state.clients.apply(lambda row: search_client.lower() in row.to_string().lower(), axis=1)
        ]
        st.dataframe(filtered_clients if search_client else st.session_state.clients)
    with tab2:
        client_name = st.text_input("Client Name")
        client_phone = st.text_input("Phone")
        client_email = st.text_input("Email")
        if st.button("Add Client"):
            if client_name and client_phone and client_email:
                new_client = pd.DataFrame([[client_name, client_phone, client_email]],
                                          columns=st.session_state.clients.columns)
                st.session_state.clients = pd.concat([st.session_state.clients, new_client], ignore_index=True)
                st.success(f"Client {client_name} added!")
            else:
                st.error("Please fill all fields.")

# Booking Management
elif menu == "Bookings":
    st.subheader("Booking Management")
    tab1, tab2 = st.tabs(["Booking List", "Schedule Booking"])
    with tab1:
        st.write("**Upcoming Bookings:**")
        st.dataframe(st.session_state.bookings)
    with tab2:
        client_name = st.selectbox("Select Client", st.session_state.clients["Name"] if not st.session_state.clients.empty else [])
        barber_name = st.selectbox("Select Barber", st.session_state.barbers["Name"] if not st.session_state.barbers.empty else [])
        date = st.date_input("Booking Date", min_value=date.today())
        time = st.time_input("Booking Time", datetime.now().time())
        service = st.text_input("Service Details")
        if st.button("Add Booking"):
            if client_name and barber_name and service:
                new_booking = pd.DataFrame([[client_name, barber_name, date, time, service]],
                                           columns=st.session_state.bookings.columns)
                if not st.session_state.bookings[
                    (st.session_state.bookings["Barber Name"] == barber_name) &
                    (st.session_state.bookings["Date"] == date) &
                    (st.session_state.bookings["Time"] == time)
                ].empty:
                    st.error("Booking conflict! Please choose another time.")
                else:
                    st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)
                    st.success("Booking added!")
            else:
                st.error("Please fill all fields.")
