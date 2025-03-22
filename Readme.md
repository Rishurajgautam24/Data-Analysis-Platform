# Data Analysis Platform 🚀

A comprehensive data analysis and visualization platform built with Python and Streamlit that provides interactive data exploration, statistical analysis, and visualization capabilities.

## Features 📊

### 1. Data Management
- Upload CSV and Excel files
- Automatic data type detection
- Missing value analysis and handling
- Data quality assessment

### 2. Feature Analysis
- **Numerical Features**
  - Statistical summaries
  - Distribution analysis
  - Box plots and histograms
- **Categorical Features**
  - Value distributions
  - Frequency analysis
  - Pie charts and bar graphs

### 3. Time Series Analysis
- Automatic time series detection
- Multiple temporal granularities (Daily, Weekly, Monthly, Quarterly, Yearly)
- Pattern analysis and decomposition
- Time-based feature extraction
- Seasonal patterns visualization

### 4. Correlation Analysis
- Interactive correlation matrix
- Feature pair analysis
- Scatter plots with correlation coefficients
- Automatic correlation suggestions

### 5. Advanced Visualizations
- **Plot Types**
  - Bar graphs
  - Line charts
  - Scatter plots
  - Pie charts
  - Box plots
  - Histograms
  - Time series plots
  - Distribution plots
- Automatic plot type suggestions based on data types
- Interactive Plotly-based visualizations

### 6. Statistical Analysis
- **Numerical Statistics**
  - Basic statistics (mean, median, std)
  - Advanced metrics (skewness, kurtosis)
  - Coefficient of variation
  - Range analysis
- **Categorical Statistics**
  - Frequency distributions
  - Mode analysis
  - Unique value counts
- **Temporal Statistics**
  - Date range analysis
  - Time span calculations
  - Temporal pattern detection

## Technical Architecture 🔧

### Core Components
1. **Frontend**: Streamlit-based web interface
2. **Data Processing**: Pandas for data manipulation
3. **Visualization**: Plotly for interactive charts
4. **Statistical Analysis**: NumPy and SciPy

### Project Structure
```
DA_platform/
├── app.py              # Main application file
├── graphs/
│   ├── plotting.py     # Visualization functions
│   └── utils.py        # Utility functions
├── logs/               # Application logs
└── README.md          # Project documentation
```

## Installation 🛠️

1. Clone the repository:
```bash
git clone <repository-url>
cd DA_platform
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Usage 📖

1. **Home Page**
   - Upload your data file (CSV or Excel)
   - Configure OpenAI API key (if needed)

2. **Data Analysis**
   - View data overview
   - Check data quality
   - Analyze data types

3. **Feature Analysis**
   - Select features to analyze
   - View statistical summaries
   - Generate visualizations

4. **Time Series**
   - Analyze temporal patterns
   - Perform time series decomposition
   - Extract time-based features

5. **Correlations**
   - View correlation matrix
   - Analyze feature pairs
   - Generate scatter plots

6. **Visualizations**
   - Create various plot types
   - Get automatic plot suggestions
   - Customize visualizations

7. **Statistics**
   - View detailed statistical analysis
   - Analyze distributions
   - Generate statistical summaries

## Dependencies 📚

- streamlit
- pandas
- numpy
- plotly
- scipy
- python-dotenv
- statsmodels

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License 📝

This project is licensed under the MIT License - see the LICENSE file for details.

## Author ✨

Rishu

## Support 💬

For support and queries, please open an issue in the repository.

---

Made with ❤️ for data analysis enthusiasts