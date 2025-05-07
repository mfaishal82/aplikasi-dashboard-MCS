import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Initialize SQLAlchemy engine
engine = create_engine(os.getenv("SUPABASE_CONNECTION_STRING"))

# Set page config
st.set_page_config(
    page_title="Dashboard Demo Tahfizh",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stMetric {
        background-color: #cadafa;
        padding: 1rem;
        border-radius: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Dashboard Demo Tahfizh")

# 1. Widget Overview (Ringkasan Umum)
st.header("1. Overview")

# Create three columns for metrics
col1, col2, col3 = st.columns(3)

# Fetch data from database
try:
    # Get total students
    with engine.connect() as conn:
        siswa_query = text("SELECT * FROM siswa")
        siswa_data = pd.read_sql(siswa_query, conn)
        total_siswa = len(siswa_data)
        siswa_gender = siswa_data['gender'].value_counts()

        # Get total teachers
        pengajar_query = text("SELECT * FROM pengajar")
        pengajar_data = pd.read_sql(pengajar_query, conn)
        total_pengajar = len(pengajar_data)
        pengajar_gender = pengajar_data['gender'].value_counts()

        # Get total active classes
        kelas_query = text("SELECT * FROM kelas")
        kelas_data = pd.read_sql(kelas_query, conn)
        total_kelas = len(kelas_data)

        # Get total active halaqoh
        halaqoh_query = text("SELECT * FROM halaqoh")
        halaqoh_data = pd.read_sql(halaqoh_query, conn)
        total_halaqoh = len(halaqoh_data)

    # Display metrics
    with col1:
        st.metric("Total Siswa", total_siswa)
        fig_siswa = px.pie(
            values=siswa_gender.values,
            names=siswa_gender.index,
            title="Distribusi Gender Siswa"
        )
        st.plotly_chart(fig_siswa, use_container_width=True)

    with col2:
        st.metric("Total Pengajar", total_pengajar)
        fig_pengajar = px.pie(
            values=pengajar_gender.values,
            names=pengajar_gender.index,
            title="Distribusi Gender Pengajar"
        )
        st.plotly_chart(fig_pengajar, use_container_width=True)

    with col3:
        st.metric("Total Kelas Aktif", total_kelas)
        st.metric("Total Halaqoh Aktif", total_halaqoh)
        ratio = total_siswa / total_pengajar if total_pengajar > 0 else 0
        st.metric("Rasio Siswa:Pengajar", f"{ratio:.2f}")

except Exception as e:
    st.error(f"Error fetching data: {str(e)}")

# 2. Widget Akademik
st.header("2. Akademik")

# Create two columns for academic metrics
col1, col2 = st.columns(2)

try:
    # Distribution of students per class
    with col1:
        st.subheader("Distribusi Siswa per Kelas")
        kelas_siswa = siswa_data.groupby('kelas_id').size()
        fig_kelas = px.bar(
            x=kelas_siswa.index,
            y=kelas_siswa.values,
            title="Jumlah Siswa per Kelas"
        )
        st.plotly_chart(fig_kelas, use_container_width=True)

    # Distribution of students per halaqoh
    with col2:
        st.subheader("Distribusi Siswa per Halaqoh")
        halaqoh_siswa = siswa_data.groupby('halaqoh_id').size()
        fig_halaqoh = px.bar(
            x=halaqoh_siswa.index,
            y=halaqoh_siswa.values,
            title="Jumlah Siswa per Halaqoh"
        )
        st.plotly_chart(fig_halaqoh, use_container_width=True)

except Exception as e:
    st.error(f"Error creating academic charts: {str(e)}")

# 3. Widget Halaqoh
st.header("3. Monitoring Halaqoh")

# Create two columns for halaqoh metrics
col1, col2 = st.columns(2)

try:
    # Halaqoh capacity analysis
    with col1:
        st.subheader("Kapasitas Halaqoh")
        # Assuming ideal capacity is 10 students per halaqoh
        ideal_capacity = 10
        halaqoh_capacity = pd.DataFrame({
            'Halaqoh': halaqoh_siswa.index,
            'Aktual': halaqoh_siswa.values,
            'Ideal': ideal_capacity
        })
        
        fig_capacity = go.Figure()
        fig_capacity.add_trace(go.Bar(
            name='Aktual',
            x=halaqoh_capacity['Halaqoh'],
            y=halaqoh_capacity['Aktual']
        ))
        fig_capacity.add_trace(go.Scatter(
            name='Ideal',
            x=halaqoh_capacity['Halaqoh'],
            y=halaqoh_capacity['Ideal'],
            mode='lines',
            line=dict(color='red', dash='dash')
        ))
        st.plotly_chart(fig_capacity, use_container_width=True)

    # Halaqoh performance
    with col2:
        st.subheader("Performa Halaqoh")
        # Get setoran data for performance analysis
        with engine.connect() as conn:
            setoran_query = text("SELECT * FROM setoran")
            setoran_df = pd.read_sql(setoran_query, conn)
        
        if not setoran_df.empty:
            # Calculate performance metrics (example: average setoran per halaqoh)
            halaqoh_performance = setoran_df.groupby('siswa_id').size().mean()
            st.metric("Rata-rata Setoran per Siswa", f"{halaqoh_performance:.2f}")
            
            # Create performance trend
            setoran_df['waktu_setoran'] = pd.to_datetime(setoran_df['waktu_setoran'])
            daily_setoran = setoran_df.groupby(setoran_df['waktu_setoran'].dt.date).size()
            
            fig_trend = px.line(
                x=daily_setoran.index,
                y=daily_setoran.values,
                title="Tren Setoran Harian"
            )
            st.plotly_chart(fig_trend, use_container_width=True)
        else:
            st.info("Belum ada data setoran untuk analisis performa")

except Exception as e:
    st.error(f"Error creating halaqoh charts: {str(e)}")

# Add footer
st.markdown("---")
st.markdown("Dashboard MCS © 2024") 