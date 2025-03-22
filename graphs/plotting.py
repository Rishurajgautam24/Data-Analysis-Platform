import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import logging
from graphs.utils import is_categorical, is_numeric

# Get logger for this module
logger = logging.getLogger(__name__)

class GraphPlotter:
    def plot_bar_graph(self, data: pd.DataFrame, x_axis: str, y_axis: str):
        try:
            if is_categorical(data[x_axis]):
                agg_data = data.groupby(x_axis)[y_axis].mean().sort_values(ascending=False)
                data_sorted = data.set_index(x_axis).loc[agg_data.index].reset_index()
                fig = px.bar(data_sorted, x=x_axis, y=y_axis, 
                             title=f'Bar Graph of {y_axis} vs {x_axis}')
            else:
                fig = px.bar(data, x=x_axis, y=y_axis, 
                             title=f'Bar Graph of {y_axis} vs {x_axis}')
            logger.info("Bar graph created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating bar graph: {e}")
            raise

    def plot_line_graph(self, data: pd.DataFrame, x_axis: str, y_axis: str):
        try:
            fig = px.line(data, x=x_axis, y=y_axis, title=f'Line Graph of {y_axis} vs {x_axis}')
            fig = px.line(data, x=x_axis, y=y_axis, title=f'Line Graph of {y_axis} vs {x_axis}')
            logger.info("Line graph created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating line graph: {e}")
            raise

    def plot_scatter_plot(self, data: pd.DataFrame, x_axis: str, y_axis: str):
        try:
            fig = px.scatter(data, x=x_axis, y=y_axis, title=f'Scatter Plot of {y_axis} vs {x_axis}')
            logger.info("Scatter plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating scatter plot: {e}")
            raise

    def plot_histogram(self, data: pd.DataFrame, column: str):
        try:    
            fig = px.histogram(data, x=column, title=f'Histogram of {column}')
            logger.info("Histogram created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating histogram: {e}")
            raise

    def plot_pie_chart(self, data: pd.DataFrame, cat_column: str, num_column: str):
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")

            if cat_column not in data.columns or num_column not in data.columns:
                raise ValueError(f"Required columns {cat_column} or {num_column} not found in data")

            fig = px.pie(data, 
                        names=cat_column, 
                        values=num_column,
                        title=f'Distribution of {cat_column}')
            logger.info("Pie chart created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating pie chart: {e}")
            raise

    def plot_correlation_matrix(self, corr_matrix: pd.DataFrame):
        try:
            # Round values for display
            corr_matrix = corr_matrix.round(3)
            
            # Create heatmap with text annotations
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix,
                x=corr_matrix.columns,
                y=corr_matrix.columns,
                colorscale='RdBu',
                zmin=-1, zmax=1,
                text=corr_matrix.values,
                texttemplate='%{text}',
                textfont={"size": 10},
                hoverongaps=False,
            ))
            
            # Update layout for better visibility
            fig.update_layout(
                title='Correlation Matrix',
                width=800,
                height=800,
                xaxis={'side': 'bottom'},
                yaxis={'side': 'left'},
            )
            
            logger.info("Correlation matrix created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating correlation matrix: {e}")
            raise

    def plot_time_series(self, data: pd.DataFrame, date_col: str, metric_col: str, freq: str):
        try:
            data[date_col] = pd.to_datetime(data[date_col])
            resampled = data.set_index(date_col)[metric_col].resample(freq).mean()
            fig = px.line(resampled, title=f'Time Series of {metric_col} ({freq})')
            logger.info("Time series plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating time series plot: {e}")
            raise

    def plot_box_plot(self, data: pd.DataFrame, column: str):
        try:
            fig = px.box(data, y=column, title=f'Box Plot of {column}')
            logger.info("Box plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating box plot: {e}")
            raise

    def plot_distribution(self, data: pd.DataFrame, column: str):
        try:
            if not is_numeric(data[column]):
                raise ValueError(f"Column {column} must be numeric for distribution plot")
            
            fig = ff.create_distplot([data[column].dropna()], [column])
            fig.update_layout(title=f'Distribution of {column}')
            logger.info("Distribution plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating distribution plot: {e}")
            raise

    def plot_time_decomposition(self, data: pd.DataFrame, date_col: str, metric_col: str):
        try:
            from statsmodels.tsa.seasonal import seasonal_decompose
            
            # Prepare time series data
            data = data.sort_values(date_col)
            data = data.set_index(pd.to_datetime(data[date_col]))
            series = data[metric_col]
            
            # Perform decomposition
            decomposition = seasonal_decompose(series, period=30)
            
            # Create subplots
            fig = go.Figure()
            
            # Original
            fig.add_trace(go.Scatter(x=series.index, y=series.values, name='Original'))
            # Trend
            fig.add_trace(go.Scatter(x=series.index, y=decomposition.trend, name='Trend'))
            # Seasonal
            fig.add_trace(go.Scatter(x=series.index, y=decomposition.seasonal, name='Seasonal'))
            # Residual
            fig.add_trace(go.Scatter(x=series.index, y=decomposition.resid, name='Residual'))
            
            fig.update_layout(title='Time Series Decomposition',
                             height=800,
                             showlegend=True)
            
            logger.info("Time series decomposition plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating time series decomposition: {e}")
            raise

    def plot_time_patterns(self, data: pd.DataFrame, date_col: str, metric_col: str):
        try:
            # Validate inputs
            if date_col not in data.columns:
                raise KeyError(f"Date column '{date_col}' not found in data")
            if metric_col not in data.columns:
                raise KeyError(f"Metric column '{metric_col}' not found in data")
                
            # Convert to datetime and validate
            data = data.copy()  # Create copy to avoid modifying original
            data[date_col] = pd.to_datetime(data[date_col])
            
            # Create subplots for different patterns
            fig = go.Figure()
            
            # Daily pattern - only if hourly data exists
            if data[date_col].dt.hour.nunique() > 1:
                daily_avg = data.groupby(data[date_col].dt.hour)[metric_col].mean()
                fig.add_trace(go.Scatter(x=daily_avg.index, y=daily_avg.values, name='Daily Pattern'))
            
            # Weekly pattern
            weekly_avg = data.groupby(data[date_col].dt.dayofweek)[metric_col].mean()
            fig.add_trace(go.Scatter(x=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                                    y=weekly_avg.values, name='Weekly Pattern'))
            
            # Monthly pattern
            monthly_avg = data.groupby(data[date_col].dt.month)[metric_col].mean()
            fig.add_trace(go.Scatter(x=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
                                    y=monthly_avg.values, name='Monthly Pattern'))

            
            fig.update_layout(
                title='Time Series Patterns',
                showlegend=True,
                xaxis_title='Time Period',
                yaxis_title=f'Average {metric_col}'
            )
            
            logger.info("Time patterns plot created successfully")
            return fig
        except Exception as e:
            logger.error(f"Error creating time patterns plot: {e}")
            raise

    def create_pie_chart(self, data, column):
        try:
            # Add validation for pie chart data
            value_counts = data[column].value_counts()
            if len(value_counts) > 10:  # Limit number of unique values
                raise ValueError(f"Column {column} has too many unique values for a pie chart")
                
            if not data[column].dtype in ['object', 'category']:
                raise ValueError(f"Column {column} must be categorical for a pie chart")
                
            plt.figure()
            plt.pie(value_counts.values, labels=value_counts.index, autopct='%1.1f%%')
            plt.title(f'Distribution of {column}')
            return True
        except Exception as e:
            logging.error(f"Error creating pie chart: {str(e)}")
            return False

    def create_time_series_plot(self, data, time_column, value_column):
        try:
            # Validate time column
            if not pd.api.types.is_datetime64_any_dtype(data[time_column]):
                data[time_column] = pd.to_datetime(data[time_column])
            
            # Validate value column
            if not pd.api.types.is_numeric_dtype(data[value_column]):
                raise ValueError(f"Column {value_column} must be numeric for time series plot")
                
            plt.figure()
            plt.plot(data[time_column], data[value_column])
            plt.title(f'{value_column} over Time')
            plt.xticks(rotation=45)
            return True
        except Exception as e:
            logging.error(f"Error creating time series plot: {str(e)}")
            return False

# Create standalone functions that use GraphPlotter class
_plotter = GraphPlotter()

def plot_bar_graph(data: pd.DataFrame, x_axis: str, y_axis: str):
    return _plotter.plot_bar_graph(data, x_axis, y_axis)

def plot_line_graph(data: pd.DataFrame, x_axis: str, y_axis: str):
    return _plotter.plot_line_graph(data, x_axis, y_axis)

def plot_scatter_plot(data: pd.DataFrame, x_axis: str, y_axis: str):
    return _plotter.plot_scatter_plot(data, x_axis, y_axis)

def plot_histogram(data: pd.DataFrame, column: str):
    return _plotter.plot_histogram(data, column)

def plot_pie_chart(data: pd.DataFrame, cat_column: str, num_column: str = None):
    return _plotter.plot_pie_chart(data, cat_column, num_column)

def plot_correlation_matrix(corr_matrix: pd.DataFrame):
    return _plotter.plot_correlation_matrix(corr_matrix)

def plot_time_series(data: pd.DataFrame, date_col: str, metric_col: str, freq: str):
    return _plotter.plot_time_series(data, date_col, metric_col, freq)

def plot_box_plot(data: pd.DataFrame, column: str):
    return _plotter.plot_box_plot(data, column)

def plot_distribution(data: pd.DataFrame, column: str):
    return _plotter.plot_distribution(data, column)

def plot_time_decomposition(data: pd.DataFrame, date_col: str, metric_col: str):
    return _plotter.plot_time_decomposition(data, date_col, metric_col)

def plot_time_patterns(data: pd.DataFrame, date_col: str, metric_col: str):
    return _plotter.plot_time_patterns(data, date_col, metric_col)
