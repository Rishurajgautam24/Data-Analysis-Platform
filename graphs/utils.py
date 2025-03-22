import pandas as pd
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

# Clear previous log file contents
open('logs/data_analysis.log', 'w').close()

# Configure logging to write to file
logging.basicConfig(
    filename='logs/data_analysis.log',
    filemode='w',  # 'w' mode overwrites the file each time
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Get logger for this module
logger = logging.getLogger(__name__)

def is_numeric(series: pd.Series) -> bool:
    """Enhanced numeric type detection"""
    if pd.api.types.is_numeric_dtype(series):
        return True
    try:
        pd.to_numeric(series)
        logger.info(f"Converted series to numeric: {series.name}")
        return True
    except (ValueError, TypeError):
        return False

def is_categorical(series: pd.Series) -> bool:
    if pd.api.types.is_object_dtype(series):
        unique_ratio = series.nunique() / len(series)
        result = unique_ratio < 0.05  # Less than 5% unique values
        logger.info(f"Checked if series is categorical: {result}")
        return result
    return False

def is_datetime(series: pd.Series) -> bool:
    result = pd.api.types.is_datetime64_any_dtype(series)
    logger.info(f"Checked if series is datetime: {result}")
    return result

def is_suitable_for_pie_chart(series):
    # Add validation for pie chart suitability
    if not is_categorical(series):
        return False
    unique_values = series.nunique()
    return unique_values <= 10 and unique_values > 1

def validate_time_series(data, column):
    try:
        if pd.api.types.is_datetime64_any_dtype(data[column]):
            return True
        # Try converting to datetime
        pd.to_datetime(data[column])
        return True
    except:
        return False

def suggest_plot_type(x_series: pd.Series, y_series: pd.Series = None) -> list:
    plots = []
    if y_series is None:
        if is_numeric(x_series):
            plots.extend(["Histogram", "Box Plot"])
        elif is_categorical(x_series):
            plots.append("Pie Chart")
        logger.info(f"Suggested plot types for single series: {plots}")
        return plots
    
    if is_numeric(x_series) and is_numeric(y_series):
        plots.extend(["Scatter Plot", "Line Graph"])
        if x_series.nunique() < 50:  # Not too many unique values
            plots.append("Bar Graph")
    elif is_categorical(x_series) and is_numeric(y_series):
        plots.extend(["Bar Graph", "Box Plot"])
    
    logger.info(f"Suggested plot types for paired series: {plots}")
    return plots

def get_column_type(series: pd.Series) -> str:
    if is_numeric(series):
        col_type = "numeric"
    elif is_datetime(series):
        col_type = "datetime"
    elif is_categorical(series):
        col_type = "categorical"
    else:
        col_type = "text"
    logger.info(f"Determined column type: {col_type}")
    return col_type

def detect_timeseries_columns(df: pd.DataFrame) -> list:
    """Detect possible time series columns including string dates."""
    timeseries_cols = []
    for col in df.columns:
        try:
            # Try converting to datetime
            pd.to_datetime(df[col])
            timeseries_cols.append(col)
            logger.info(f"Detected time series column: {col}")
        except:
            continue
    return timeseries_cols

def extract_time_features(series: pd.Series) -> pd.DataFrame:
    """Extract time-based features from a datetime series."""
    df = pd.DataFrame()
    series = pd.to_datetime(series)
    
    df['year'] = series.dt.year
    df['month'] = series.dt.month
    df['day'] = series.dt.day
    df['day_of_week'] = series.dt.dayofweek
    df['quarter'] = series.dt.quarter
    df['is_weekend'] = series.dt.dayofweek > 4
    df['hour'] = series.dt.hour if series.dt.hour.nunique() > 1 else None
    
    # Remove columns with all None values
    df = df.dropna(axis=1, how='all')
    
    logger.info(f"Extracted time features: {df.columns.tolist()}")
    return df
