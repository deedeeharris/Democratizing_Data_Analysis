# @title START HERE: Run me. Upload your data file. Press the "Copy" button. { display-mode: "form" }

from google.colab import files
from IPython.display import HTML, Javascript, clear_output  # Import the clear_output function
import pandas as pd
import os
# Data manipulation and analysis
import pandas as pd
import numpy as np

# Data visualization
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

# Statistical analysis
from scipy import stats

# Interactive data visualization (optional, but useful for complex plots)
import plotly.express as px
import plotly.graph_objects as go

# Geospatial visualization (if working with geospatial data)
import geopandas as gpd

# Time series analysis (if working with time series data)
import statsmodels.api as sm

# Machine learning tools (if doing predictive analysis)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def upload_csv_or_excel():
    try:
        print("Please upload a CSV or Excel (or SPSS sav/zsav) file:")
        print("\n\n")
        uploaded = files.upload()


        for file_name, file_content in uploaded.items():
            if file_name.endswith('.csv'):
                df = pd.read_csv(file_name)
                file_type = "CSV"
            elif file_name.endswith('.xlsx') or file_name.endswith('.xls'):
                df = pd.read_excel(file_name)
                file_type = "Excel"
            elif file_name.endswith('.zsav') or file_name.endswith('.sav'):
                df = pd.read_spss(file_name)
                file_type = "SPSS"
                # Save the DataFrame with the same name as the original file
                file_name = file_name.replace('.zsav', '.csv').replace('.sav', '.csv')
                df.to_csv(file_name, index=False)
                print(f"DataFrame from {file_type} saved as CSV:", file_name)
            else:
                print(f"Unsupported file format for {file_name}. Only CSV and Excel files are supported.")
                return

            # Get the full file path
            file_path = os.path.abspath(file_name)

            print("\n\n")

            prompt = f"""
Act as a senior Python Data Analyst. You will be provided with a file path of a xlsx/xls file or a csv file, and information regarding it.
Your task is to generate Python code according to the user's request, related to data analysis and visualization.
You should return the entire code in one message. Please note that you should not return any additional explanations or markdown text,
only the Python code with detailed comments. If the dataset contains Hebrew words, then from bidi.algorithm import get_display, and use it only when plotting seaborn figure titles, axis titles, x and y ticks, etc.
When the user asks to download a file, then from google.colab import files.download. Think step by step.
This is the path to my file: "{file_path}"
Wait for your first task. Just wait, don't do a thing. Say: I'm waiting for your first questions.
"""

            summary_statistics = df.describe()
            missing_values = df.isnull().sum()
            df_info = df.info()
            df_cols = df.columns
            df_head = df.head()
            df_dtypes = df.dtypes

            # Generate the JavaScript code to copy the output to the clipboard
            js_code = f'''
            function copyToClipboard() {{
                const textToCopy = `{prompt}\n\nColumns:\\n{df_cols}\n\\nData Types:\\n{df_dtypes}\n\\nSample Data:\\n{df_head}\n\\n
Summary Statistics:\\n{summary_statistics}\n\\nFile info:\\n{df_info}\n\\nMissing Values:\\n{missing_values}`;
                navigator.clipboard.writeText(textToCopy);
                alert('Output copied to clipboard!');
            }}
            '''

            # Clear the output on the screen before displaying the button
            clear_output()

            print("\n\n")

            # Display the copy button using HTML and JavaScript
            display(HTML('<button onclick="copyToClipboard()">Click Here to Copy, and paste in the ChatGPT window.</button>'))
            display(Javascript(js_code))

            return df

    except Exception as e:
        print("An error occurred:", str(e))
