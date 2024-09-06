import streamlit as st
import numpy as np
import subprocess
import sys

# Function to install packages
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import required libraries, install if not available
try:
    import plotly.graph_objects as go
except ImportError:
    install('plotly')
    import plotly.graph_objects as go

try:
    from bokeh.plotting import figure, show
    from bokeh.io import output_notebook
except ImportError:
    install('bokeh')
    from bokeh.plotting import figure, show
    from bokeh.io import output_notebook

# Function to calculate compound interest
def calculate_compound_interest(principal, rate, time):
    amount = principal * (1 + rate) ** time
    return amount

# Function to adjust for inflation
def adjust_for_inflation(amount, inflation_rate, time):
    adjusted_amount = amount * (1 + inflation_rate) ** time
    return adjusted_amount

# Function to calculate present value
def calculate_present_value(inflation_adjusted_amount, inflation_rate, time):
    present_value = inflation_adjusted_amount / (1 + inflation_rate) ** time
    return present_value

# Streamlit app
st.title("Compound Interest and Inflation Adjustment Calculator")

# User inputs
principal = st.number_input("Enter the principal amount ($):", min_value=0.0, value=1000.0)
interest_rate = st.number_input("Enter the annual interest rate (%):", min_value=0.0, value=5.0) / 100
inflation_rate = st.number_input("Enter the annual inflation rate (%):", min_value=0.0, value=3.0) / 100
time_period = st.number_input("Enter the time period (years):", min_value=1, value=10)

# Calculate values
amounts = [calculate_compound_interest(principal, interest_rate, t) for t in range(time_period + 1)]
adjusted_amounts = [adjust_for_inflation(amount, inflation_rate, t) for t, amount in enumerate(amounts)]
present_values = [calculate_present_value(adjusted_amount, inflation_rate, t) for t, adjusted_amount in enumerate(adjusted_amounts)]

# Dropdown for selecting graph type
graph_type = st.selectbox("Select Graph Type:", ["Plotly", "Matplotlib", "Bokeh"])

# Plotting with selected library
if graph_type == "Plotly":
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(time_period + 1)), y=amounts, mode='lines+markers', name='Future Value with Compound Interest'))
    fig.add_trace(go.Scatter(x=list(range(time_period + 1)), y=adjusted_amounts, mode='lines+markers', name='Inflation Adjusted Amount'))
    fig.add_trace(go.Scatter(x=list(range(time_period + 1)), y=present_values, mode='lines+markers', name='Present Value of Inflation Adjusted Amount'))
    
    fig.update_layout(title='Compound Interest, Inflation Adjustment, and Present Value',
                      xaxis_title='Years',
                      yaxis_title='Amount ($)',
                      legend_title='Legend')
    st.plotly_chart(fig)

elif graph_type == "Matplotlib":
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot(range(time_period + 1), amounts, label='Future Value with Compound Interest', marker='o')
    ax.plot(range(time_period + 1), adjusted_amounts, label='Inflation Adjusted Amount', marker='o')
    ax.plot(range(time_period + 1), present_values, label='Present Value of Inflation Adjusted Amount', marker='o')

    ax.set_title('Compound Interest, Inflation Adjustment, and Present Value')
    ax.set_xlabel('Years')
    ax.set_ylabel('Amount ($)')
    ax.legend()
    ax.grid()
    st.pyplot(fig)

elif graph_type == "Bokeh":
    p = figure(title="Compound Interest, Inflation Adjustment, and Present Value", x_axis_label='Years', y_axis_label='Amount ($)')
    p.line(range(time_period + 1), amounts, legend_label='Future Value with Compound Interest', line_width=2, color='blue')
    p.line(range(time_period + 1), adjusted_amounts, legend_label='Inflation Adjusted Amount', line_width=2, color='orange')
    p.line(range(time_period + 1), present_values, legend_label='Present Value of Inflation Adjusted Amount', line_width=2, color='green')

    st.bokeh_chart(p)

# Display results
st.subheader("Results")
st.write(f"Future Value with Compound Interest after {time_period} years: ${amounts[-1]:.2f}")
st.write(f"Inflation Adjusted Amount after {time_period} years: ${adjusted_amounts[-1]:.2f}")
st.write(f"Present Value of Inflation Adjusted Amount: ${present_values[-1]:.2f}")
