import plotly.express as px

def pie_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, hole=0.3, title=title)
    fig.update_traces(textposition='inside', textinfo='percent+label')
    return fig

def bar_chart(df, x, y, title):
    fig = px.bar(df, x=x, y=y, text_auto=True, title=title)
    fig.update_layout(xaxis_tickangle=-30)
    return fig

def line_chart(df, x, y, title):
    fig = px.line(df, x=x, y=y, markers=True, title=title)
    return fig

def area_chart(df, x, y, color, title):
    fig = px.area(df, x=x, y=y, color=color, title=title)
    return fig

def donut_chart(df, names, values, title):
    fig = px.pie(df, names=names, values=values, hole=0.6, title=title)
    return fig
