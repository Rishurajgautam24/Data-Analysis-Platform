import os
import streamlit as st
import plotly.express as px
import pandas as pd
from dotenv import load_dotenv
import numpy as np
from datetime import datetime
from graphs.plotting import (plot_bar_graph, plot_line_graph, plot_scatter_plot, 
                             plot_histogram, plot_pie_chart, plot_correlation_matrix, 
                             plot_time_series, plot_box_plot, plot_time_patterns,
                             plot_time_decomposition)
from graphs.utils import (suggest_plot_type, get_column_type, is_categorical, is_numeric,
                        detect_timeseries_columns, extract_time_features)
from io import StringIO
import logging

# Get logger for this module
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)

# Load API key from .env file
load_dotenv()
default_api_key = os.getenv("OPENAI_API_KEY")

# Page Configuration
st.set_page_config(
    page_title="Data Analysis Platform",
    page_icon="📊",
    layout="wide"
)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", 
    ["Home", "Data Analysis", "Feature Analysis", "Time Series", 
     "Correlations", "Visualizations", "Statistics"])

# Load API key and data globally
if 'data' not in st.session_state:
    st.session_state.data = None

# Home Page
if page == "Home":
    st.title("📊 Data Analysis Platform")
    st.markdown("""
    Welcome to the Data Analysis Platform. This tool helps you:
    - Upload and analyze your data
    - Create interactive visualizations
    - Generate statistical insights
    """)
    
    # API Key Section
    with st.expander("OpenAI API Configuration"):
        api_key = st.text_input("Enter your OpenAI API Key:", value=default_api_key, type="password")
        if api_key:
            st.success("API Key loaded successfully!")
        else:
            st.warning("Please enter a valid API Key.")

    # Data Upload Section
    st.header("📁 Upload Your Data")
    uploaded_file = st.file_uploader("Upload your data file (CSV, Excel):", type=["csv", "xlsx"])
    
    if uploaded_file:
        try:
            if uploaded_file.name.endswith(".csv"):
                st.session_state.data = pd.read_csv(uploaded_file)
            else:
                st.session_state.data = pd.read_excel(uploaded_file)
            st.success("Data loaded successfully!")
        except Exception as e:
            st.error(f"Error loading file: {e}")

# Enhanced Data Analysis Page
elif page == "Data Analysis":
    st.title("🔍 Data Analysis")
    if st.session_state.data is not None:
        tab1, tab2, tab3 = st.tabs(["Overview", "Data Quality", "Data Types"])
        
        with tab1:
            st.subheader("Data Preview")
            st.dataframe(st.session_state.data.head())
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Rows", st.session_state.data.shape[0])
                st.metric("Total Columns", st.session_state.data.shape[1])
            with col2:
                st.metric("Missing Values", st.session_state.data.isnull().sum().sum())
                st.metric("Duplicate Rows", st.session_state.data.duplicated().sum())
        
        with tab2:
            st.subheader("Missing Values Analysis")
            missing_df = pd.DataFrame({
                'Column': st.session_state.data.columns,
                'Missing Values': st.session_state.data.isnull().sum(),
                'Missing Percentage': (st.session_state.data.isnull().sum() / len(st.session_state.data) * 100)
            })
            st.dataframe(missing_df)
            
            if st.button("Handle Missing Values"):
                method = st.radio("Select method:", 
                    ["Drop rows", "Fill with mean/mode", "Fill with median"])
                # Add missing value handling logic here
        
        with tab3:
            st.subheader("Data Types Information")
            dtypes_df = pd.DataFrame(st.session_state.data.dtypes, columns=['Data Type'])
            st.dataframe(dtypes_df)

# Updated Feature Analysis Page
elif page == "Feature Analysis":
    st.title("🎯 Feature Analysis")
    if st.session_state.data is not None:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Numerical Features")
            num_cols = st.session_state.data.select_dtypes(include=['number']).columns
            if len(num_cols) > 0:
                selected_num = st.selectbox("Select numerical feature:", num_cols)
                st.write("Statistical Summary:")
                st.write(st.session_state.data[selected_num].describe())
                
                # Suggest appropriate plots
                suggested_plots = suggest_plot_type(st.session_state.data[selected_num])
                plot_type = st.selectbox("Select Plot Type:", suggested_plots)
                
                if plot_type == "Box Plot":
                    fig = plot_box_plot(st.session_state.data, selected_num)
                elif plot_type == "Histogram":
                    fig = plot_histogram(st.session_state.data, selected_num)
                st.plotly_chart(fig)
        
        with col2:
            st.subheader("Categorical Features")
            # Filter for categorical columns based on cardinality
            cat_cols = [col for col in st.session_state.data.columns 
                       if is_categorical(st.session_state.data[col])]
            
            if len(cat_cols) > 0:
                selected_cat = st.selectbox("Select categorical feature:", cat_cols)
                
                # Show category statistics
                value_counts = st.session_state.data[selected_cat].value_counts().reset_index()
                value_counts.columns = [selected_cat, 'count']
                
                st.write("Category Distribution:")
                st.write(value_counts)
                
                # Try to plot pie chart, fall back to bar chart if not suitable
                try:
                    fig = plot_pie_chart(value_counts, selected_cat, 'count')
                except ValueError as e:
                    st.warning(str(e))
                    fig = plot_bar_graph(value_counts, selected_cat, 'count')
                
                st.plotly_chart(fig)

# Update the Time Series page section
elif page == "Time Series":
    st.title("📅 Time Series Analysis")
    if st.session_state.data is not None:
        # Detect time series columns
        date_cols = detect_timeseries_columns(st.session_state.data)
        
        if date_cols:
            try:
                # Time series analysis options
                analysis_type = st.sidebar.selectbox(
                    "Analysis Type",
                    ["Time Series Plot", "Patterns Analysis", "Decomposition", "Time Features"]
                )
                
                date_col = st.selectbox("Select date column:", date_cols)
                metric_col = st.selectbox("Select metric:", 
                    st.session_state.data.select_dtypes(include=['number']).columns)
                
                if not metric_col:
                    st.warning("No numeric columns found for analysis")
                else:
                    if analysis_type == "Time Series Plot":
                        freq = st.selectbox("Select frequency:", 
                            ["Daily", "Weekly", "Monthly", "Quarterly", "Yearly"])
                        freq_map = {
                            "Daily": "D", "Weekly": "W", "Monthly": "M",
                            "Quarterly": "Q", "Yearly": "Y"
                        }
                        fig = plot_time_series(st.session_state.data, date_col, 
                                             metric_col, freq_map[freq])
                        st.plotly_chart(fig)
                    
                    elif analysis_type == "Patterns Analysis":
                        try:
                            fig = plot_time_patterns(st.session_state.data, date_col, metric_col)
                            st.plotly_chart(fig)
                        except Exception as e:
                            st.error(f"Error creating patterns plot: {str(e)}")
                    
                    elif analysis_type == "Decomposition":
                        try:
                            fig = plot_time_decomposition(st.session_state.data, date_col, metric_col)
                            st.plotly_chart(fig)
                        except Exception as e:
                            st.error(f"Error creating decomposition plot: {str(e)}")
                    
                    elif analysis_type == "Time Features":
                        st.subheader("Time-based Features")
                        time_features = extract_time_features(st.session_state.data[date_col])
                        st.write(time_features.head())
                        
                        if st.button("Download Time Features"):
                            csv = time_features.to_csv(index=False)
                            st.download_button(
                                "Download CSV",
                                csv,
                                "time_features.csv",
                                "text/csv",
                                key='download-time-features'
                            )
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("No time series columns detected in the dataset.")
    else:
        st.warning("Please upload data in the Home page first!")

# New Correlations Page
elif page == "Correlations":
    st.title("🔗 Correlation Analysis")
    if st.session_state.data is not None:
        # Find all numeric columns including those that can be converted
        numeric_cols = []
        for col in st.session_state.data.columns:
            try:
                if is_numeric(st.session_state.data[col]):
                    numeric_cols.append(col)
                    if not pd.api.types.is_numeric_dtype(st.session_state.data[col]):
                        # Convert column to numeric if it's not already
                        st.session_state.data[col] = pd.to_numeric(st.session_state.data[col])
            except Exception as e:
                logger.warning(f"Could not convert column {col} to numeric: {e}")
        
        if len(numeric_cols) > 1:  # Need at least 2 columns for correlation
            # Create correlation matrix
            corr_matrix = st.session_state.data[numeric_cols].corr()
            
            # Display correlation heatmap
            fig = plot_correlation_matrix(corr_matrix)
            st.plotly_chart(fig)
            
            # Feature pair analysis
            st.subheader("Feature Pair Analysis")
            col1, col2 = st.columns(2)
            with col1:
                feat1 = st.selectbox("Select first feature:", numeric_cols)
            with col2:
                feat2 = st.selectbox("Select second feature:", numeric_cols)
            
            if feat1 and feat2:
                fig = plot_scatter_plot(st.session_state.data, feat1, feat2)
                st.plotly_chart(fig)
                
                # Display correlation coefficient
                corr_value = corr_matrix.loc[feat1, feat2]
                st.info(f"Correlation coefficient between {feat1} and {feat2}: {corr_value:.3f}")
        else:
            st.warning("Not enough numeric columns found for correlation analysis (minimum 2 required)")
    else:
        st.warning("Please upload data in the Home page first!")

# Updated Visualizations Page
elif page == "Visualizations":
    st.title("📈 Data Visualizations")
    if st.session_state.data is not None:
        # First, let user select columns
        col1, col2 = st.columns(2)
        with col1:
            x_column = st.selectbox("Select X-axis column:", st.session_state.data.columns)
        with col2:
            y_column = st.selectbox("Select Y-axis column (optional):", 
                                  ['None'] + list(st.session_state.data.columns))
        
        # Get suggested plot types based on data
        if y_column == 'None':
            suggested_plots = suggest_plot_type(st.session_state.data[x_column])
        else:
            suggested_plots = suggest_plot_type(
                st.session_state.data[x_column], 
                st.session_state.data[y_column]
            )
        
        if suggested_plots:
            plot_type = st.selectbox("Suggested Plot Types:", suggested_plots)
            
            try:
                if plot_type == "Pie Chart":
                    # Create a DataFrame with value counts for the pie chart
                    value_counts = st.session_state.data[x_column].value_counts()
                    plot_data = pd.DataFrame({
                        'category': value_counts.index,
                        'count': value_counts.values
                    })
                    fig = plot_pie_chart(plot_data, 'category', 'count')
                elif plot_type == "Bar Graph":
                    fig = plot_bar_graph(st.session_state.data, x_column, 
                                       y_column if y_column != 'None' else x_column)
                elif plot_type == "Scatter Plot":
                    fig = plot_scatter_plot(st.session_state.data, x_column, y_column)
                elif plot_type == "Box Plot":
                    fig = plot_box_plot(st.session_state.data, 
                                      y_column if y_column != 'None' else x_column)
                elif plot_type == "Histogram":
                    fig = plot_histogram(st.session_state.data, x_column)
                
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating plot: {str(e)}")
        else:
            st.warning("No suitable plots available for selected data types")

# Statistics Page
elif page == "Statistics":
    st.title("📊 Statistical Analysis")
    if st.session_state.data is not None:
        tabs = st.tabs(["Numerical Stats", "Categorical Stats", "Datetime Stats", "Distribution"])
        
        with tabs[0]:
            st.subheader("Numerical Statistics")
            num_cols = st.session_state.data.select_dtypes(include=['number']).columns
            
            if len(num_cols) > 0:
                # Enhanced numerical statistics
                num_stats = st.session_state.data[num_cols].agg([
                    'count', 'mean', 'std', 'min', 
                    lambda x: x.quantile(0.25),
                    'median',
                    lambda x: x.quantile(0.75),
                    'max', 'skew', 'kurtosis'
                ]).round(2)
                
                num_stats.index = ['Count', 'Mean', 'Std Dev', 'Min', '25%', 'Median', 
                                 '75%', 'Max', 'Skewness', 'Kurtosis']
                
                st.dataframe(num_stats)
                
                # Additional metrics
                for col in num_cols:
                    with st.expander(f"Detailed Analysis - {col}"):
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Coefficient of Variation", 
                                    f"{(st.session_state.data[col].std() / st.session_state.data[col].mean() * 100):.2f}%")
                            st.metric("Range", 
                                    f"{st.session_state.data[col].max() - st.session_state.data[col].min():.2f}")
                        with col2:
                            st.metric("Missing Values", 
                                    f"{st.session_state.data[col].isnull().sum()} ({st.session_state.data[col].isnull().mean()*100:.1f}%)")
                            st.metric("Unique Values", 
                                    st.session_state.data[col].nunique())
            else:
                st.warning("No numerical columns found in the dataset")
        
        with tabs[1]:
            st.subheader("Categorical Statistics")
            # Include object and category dtypes
            cat_cols = st.session_state.data.select_dtypes(include=['object', 'category']).columns
            
            if len(cat_cols) > 0:
                for col in cat_cols:
                    with st.expander(f"Category Analysis - {col}"):
                        value_counts = st.session_state.data[col].value_counts()
                        value_percentages = st.session_state.data[col].value_counts(normalize=True)
                        
                        # Create summary dataframe
                        cat_summary = pd.DataFrame({
                            'Count': value_counts,
                            'Percentage': value_percentages * 100
                        }).round(2)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Unique Values", len(value_counts))
                            st.metric("Missing Values", 
                                    f"{st.session_state.data[col].isnull().sum()} ({st.session_state.data[col].isnull().mean()*100:.1f}%)")
                        
                        with col2:
                            st.metric("Mode", value_counts.index[0])
                            st.metric("Mode Frequency", f"{value_percentages.iloc[0]*100:.1f}%")
                        
                        st.write("Value Distribution:")
                        st.dataframe(cat_summary)
                        
                        # Plot distribution with value counts data
                        try:
                            if len(value_counts) <= 10:
                                fig = px.pie(values=value_counts.values, 
                                           names=value_counts.index,
                                           title=f'Distribution of {col}')
                            else:
                                # Create DataFrame for bar plot
                                plot_df = pd.DataFrame({
                                    'Category': value_counts.index,
                                    'Count': value_counts.values
                                })
                                fig = plot_bar_graph(plot_df, 'Category', 'Count')
                            st.plotly_chart(fig)
                        except Exception as e:
                            st.error(f"Error creating plot for {col}: {str(e)}")
            else:
                st.warning("No categorical columns found in the dataset")
        
        with tabs[2]:
            st.subheader("Datetime Statistics")
            date_cols = detect_timeseries_columns(st.session_state.data)
            
            if date_cols:
                for col in date_cols:
                    with st.expander(f"Temporal Analysis - {col}"):
                        dates = pd.to_datetime(st.session_state.data[col])
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Date Range", f"{dates.min().date()} to {dates.max().date()}")
                            st.metric("Time Span", f"{(dates.max() - dates.min()).days} days")
                        
                        with col2:
                            st.metric("Missing Values", 
                                    f"{dates.isnull().sum()} ({dates.isnull().mean()*100:.1f}%)")
                            st.metric("Unique Dates", dates.nunique())
                        
                        # Temporal patterns
                        time_features = extract_time_features(dates)
                        st.write("Temporal Distribution:")
                        st.dataframe(time_features.describe().round(2))
            else:
                st.warning("No datetime columns found in the dataset")
        
        with tabs[3]:
            st.subheader("Distribution Analysis")
            num_cols = st.session_state.data.select_dtypes(include=['number']).columns
            
            if len(num_cols) > 0:
                selected_col = st.selectbox("Select column for distribution analysis:", num_cols)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = plot_histogram(st.session_state.data, selected_col)
                    st.plotly_chart(fig)
                
                with col2:
                    fig = plot_box_plot(st.session_state.data, selected_col)
                    st.plotly_chart(fig)
                
                # Distribution statistics
                data = st.session_state.data[selected_col].dropna()
                st.write("Distribution Metrics:")
                metrics_df = pd.DataFrame({
                    'Metric': ['Skewness', 'Kurtosis', 'Mean', 'Median', 'Mode'],
                    'Value': [
                        f"{data.skew():.2f}",
                        f"{data.kurtosis():.2f}",
                        f"{data.mean():.2f}",
                        f"{data.median():.2f}",
                        f"{data.mode().iloc[0]:.2f}"
                    ]
                })
                st.dataframe(metrics_df)
            else:
                st.warning("No numerical columns found for distribution analysis")
    else:
        st.warning("Please upload data in the Home page first!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("Developed By Rishu")
