import streamlit as st
import plotly.express as px
from utils.filters import load_data, sidebar_filters

st.title("🔍 Custom Data Explorer")

df = sidebar_filters(load_data())

cols = st.columns(3)
x_axis = cols[0].selectbox("Select X-axis", df.columns)
y_axis = cols[1].selectbox("Select Y-axis", df.columns)
color = cols[2].selectbox("Color by", [None] + df.columns.tolist())

chart_type = st.radio("Chart Type", ["Bar", "Line", "Area", "Pie", "Donut"])

if chart_type == "Bar":
    fig = px.bar(df, x=x_axis, y=y_axis, color=color, title=f"{y_axis} by {x_axis}")
elif chart_type == "Line":
    fig = px.line(df, x=x_axis, y=y_axis, color=color, markers=True)
elif chart_type == "Area":
    fig = px.area(df, x=x_axis, y=y_axis, color=color)
elif chart_type == "Pie":
    fig = px.pie(df, names=x_axis, values=y_axis, title=f"{y_axis} Distribution by {x_axis}")
elif chart_type == "Donut":
    fig = px.pie(df, names=x_axis, values=y_axis, hole=0.5, title=f"{y_axis} Distribution by {x_axis}")

st.plotly_chart(fig, use_container_width=True)
