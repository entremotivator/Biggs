import streamlit as st
import pandas as pd

# App title and configuration
st.set_page_config(page_title="The Zoo by Bigs", layout="wide", initial_sidebar_state="expanded")
st.title("Welcome to 🦁 **The Zoo by Bigs** 🐾")

# Initialize DataFrames with demo data
if "barbers" not in st.session_state:
    st.session_state.barbers = pd.DataFrame({
        "Name": ["Bigs", "Mike", "Sam", "Chris", "Leo", "Jay", "Drew", "Eddie", "Tony", "Will"],
        "Specialty": ["Fades", "Beards", "Braids", "Dreads", "Lineups", "Tapers", "Shaves", "Coloring", "Kids Cuts", "Designs"],
        "Experience (Years)": [10, 8, 6, 5, 7, 9, 4, 6, 11, 5],
        "Contact": ["555-1234", "555-5678", "555-9012", "555-3456", "555-7890",
                    "555-2468", "555-1357", "555-9753", "555-8642", "555-6428"]
    })

if "clients" not in st.session_state:
    st.session_state.clients = pd.DataFrame({
        "Name": ["John Doe", "Jane Smith", "Paul Johnson", "Sarah Brown", "Michael Davis",
                 "Emily Clark", "Robert Wilson", "Linda Taylor", "James Lee", "Sophia Harris"],
        "Phone": ["555-1111", "555-2222", "555-3333", "555-4444", "555-5555",
                  "555-6666", "555-7777", "555-8888", "555-9999", "555-0000"],
        "Email": ["john@example.com", "jane@example.com", "paul@example.com", "sarah@example.com",
                  "michael@example.com", "emily@example.com", "robert@example.com", "linda@example.com",
                  "james@example.com", "sophia@example.com"]
    })

if "bookings" not in st.session_state:
    st.session_state.bookings = pd.DataFrame(columns=["Client Name", "Barber Name", "Date", "Time", "Service"])

# Sidebar Navigation
menu = st.sidebar.radio("Navigation", ["🏠 Home", "📊 Dashboard", "💈 Barbers", "👥 Clients", "📅 Bookings"])

# Home Page
if menu == "🏠 Home":
    st.subheader("Welcome to 🦁 **The Zoo by Bigs** 🐾")
    st.write(
        """
        **The Zoo by Bigs** is a modern barber management system designed to make life easier for barbers, clients, 
        and anyone in the hair grooming industry! This app helps you keep track of:
        """
    )
    st.markdown(
        """
        ### 🌟 Key Features:
        - **💈 Barber Management:** Easily add and manage barbers with specialties, years of experience, and contact details.
        - **👥 Client Management:** Store and organize client information, including phone numbers and emails.
        - **📅 Booking System:** Effortlessly schedule appointments and keep track of upcoming bookings.
        - **📊 Dashboard:** Get a quick overview of barbers, clients, and bookings in one place.
        - **🔍 Data Insights:** View and filter barber and client information for better organization.
        - **✨ Customizable:** Built for barbershops of all sizes, from local businesses to global enterprises.
        """
    )
    st.markdown("---")
    st.write("## Why Choose Us?")
    st.markdown(
        """
        - **📱 User-Friendly Interface:** Streamlined and easy to use for everyone.
        - **🌎 Global Support:** Ideal for barbershops of all scales across the world.
        - **🚀 Performance:** Designed for speed and efficiency.
        """
    )
    st.image(
        "https://source.unsplash.com/800x400/?barbershop",
        caption="A seamless barber management experience.",
        use_column_width=True,
    )

# Dashboard
elif menu == "📊 Dashboard":
    st.subheader("📊 Dashboard")
    st.write(f"**Total Barbers:** {len(st.session_state.barbers)}")
    st.write(f"**Total Clients:** {len(st.session_state.clients)}")
    st.write(f"**Upcoming Bookings:** {len(st.session_state.bookings)}")

    if not st.session_state.bookings.empty:
        st.write("**Next Booking:**")
        st.write(st.session_state.bookings.head(1))
    else:
        st.write("No upcoming bookings.")

    st.markdown("---")
    st.write("**Barbers at The Zoo by Bigs:**")
    st.dataframe(st.session_state.barbers)
    st.markdown("---")
    st.write("**Our Valued Clients:**")
    st.dataframe(st.session_state.clients)

# Barber Management
elif menu == "💈 Barbers":
    st.subheader("💈 Barber Management")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Current Barbers:**")
        st.dataframe(st.session_state.barbers)

    with col2:
        st.write("**Add New Barber:**")
        name = st.text_input("Name")
        specialty = st.text_input("Specialty")
        experience = st.number_input("Experience (Years)", min_value=0, max_value=50, step=1)
        contact = st.text_input("Contact Information")

        if st.button("Add Barber"):
            new_barber = pd.DataFrame([[name, specialty, experience, contact]],
                                      columns=st.session_state.barbers.columns)
            st.session_state.barbers = pd.concat([st.session_state.barbers, new_barber], ignore_index=True)
            st.success(f"Barber {name} added!")

# Client Management
elif menu == "👥 Clients":
    st.subheader("👥 Client Management")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Current Clients:**")
        st.dataframe(st.session_state.clients)

    with col2:
        st.write("**Add New Client:**")
        client_name = st.text_input("Client Name")
        client_phone = st.text_input("Phone")
        client_email = st.text_input("Email")

        if st.button("Add Client"):
            new_client = pd.DataFrame([[client_name, client_phone, client_email]],
                                      columns=st.session_state.clients.columns)
            st.session_state.clients = pd.concat([st.session_state.clients, new_client], ignore_index=True)
            st.success(f"Client {client_name} added!")

# Booking Management
elif menu == "📅 Bookings":
    st.subheader("📅 Booking Management")
    col1, col2 = st.columns(2)

    with col1:
        st.write("**Upcoming Bookings:**")
        st.dataframe(st.session_state.bookings)

    with col2:
        st.write("**Schedule a New Booking:**")
        client_name = st.selectbox("Select Client", st.session_state.clients["Name"] if not st.session_state.clients.empty else [])
        barber_name = st.selectbox("Select Barber", st.session_state.barbers["Name"] if not st.session_state.barbers.empty else [])
        date = st.date_input("Booking Date")
        time = st.time_input("Booking Time")
        service = st.text_input("Service Details")

        if st.button("Add Booking"):
            new_booking = pd.DataFrame([[client_name, barber_name, date, time, service]],
                                       columns=st.session_state.bookings.columns)
            st.session_state.bookings = pd.concat([st.session_state.bookings, new_booking], ignore_index=True)
            st.success("Booking added!")

                st.error("Please fill all fields.")
