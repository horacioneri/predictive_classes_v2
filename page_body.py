import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
import plotly.express as px
import plotly.graph_objects as go
from config import page_titles
from sidebar import sidebar_config

def introduction_text():
    st.header('**What can this app do?**')
    with st.expander('**Click to see explanation**', expanded=False):
        st.write('This app allow users to build a machine learning (ML) model with an end-to-end workflow simple steps:\n')
        for i in range(len(page_titles)-1):
            st.write(f'- {page_titles[i+1]}\n')

    st.header('**How to use the app?**')
    with st.expander('**Click to see explanation**', expanded=False):
        st.write('To engage with the app, you will be able to use the sidebar to make choices that will help prepare and train the machine learning model. Some examples of choices are:\n1. Upload a data set\n2. Select the data imputation methods\n3. Adjust the model training and parameters\nYou will be able to go back and forth to understand the impact of different choices on the results')

    st.header('Data Loading', divider='rainbow')
    if not st.session_state.uploaded:
        st.write('Upload a dataset on the sidebar')
    else:
        st.write('This is your dataset:')
        df = st.session_state.df_original
        st.dataframe(df, height = 300)
        st.write('The last column of the dataset will be considered your target variable') # Review at the end
        st.write('These are the data types identified for your dataset:')
        st.write(df.dtypes)

def exploratory_data_analysis():
    df = st.session_state.df_original
    st.header('Single variable analysis', divider='rainbow')
    col = st.columns(2)
    for c in range(len(col)):
        if c == 0:
            var = st.session_state.var_1
        else:
            var = st.session_state.var_2

        with col[c]:
            st.subheader(var)
            var_data = df[var]
            if var_data.dtype in ['int64', 'float64']:
                st.write(var_data.describe())

                # Visualize the distribution (Histogram with Plotly)
                fig = px.histogram(var_data, nbins=20, title=f'Distribution of {var}')
                fig.update_layout(
                    xaxis_title=var,
                    yaxis_title='Frequency',
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Box plot to detect outliers
                fig = px.box(var_data, title=f'Box plot of {var}')
                fig.update_layout(
                    yaxis_title=var,
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

            else:
                st.write(var_data.value_counts())

                # Bar plot for category distribution
                fig = px.bar(var_data.value_counts().reset_index(), x=var, y='count', 
                            title=f'Count plot of {var}', labels={var: var, 'count': 'Frequency'})
                fig.update_layout(
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)

                # Pie chart for proportions
                fig = px.pie(var_data, names=var_data.value_counts().index, 
                            title=f'Pie chart of {var}', 
                            hole=0.3)
                fig.update_traces(textinfo='percent+label')
                fig.update_layout(
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
                st.plotly_chart(fig, use_container_width=True)
        
    st.header('Two variable analysis', divider='rainbow')
    var_name1 = st.session_state.var_1
    var_name2 = st.session_state.var_2
    var_data1 = df[var_name1]
    var_data2 = df[var_name2]

    # Case 1: Both variables are numerical
    if var_data1.dtype in ['int64', 'float64'] and var_data2.dtype in ['int64', 'float64']:
        # Scatter plot to show relationship
        fig = px.scatter(df, x=var_name1, y=var_name2, trendline="ols", title=f"Scatter plot of {var_name1} vs {var_name2} with linear regression line")
        fig.update_layout(
                    xaxis_title=var_name1, 
                    yaxis_title=var_name2,
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
        st.plotly_chart(fig, use_container_width=True)

        # Correlation coefficient
        corr = var_data1.corr(var_data2)
        print(f"Correlation coefficient between {var_name1} and {var_name2}: {corr}")

    # Case 2: One variable is numerical and the other is categorical
    elif var_data1.dtype in ['int64', 'float64'] and var_data2.dtype in ['object', 'category']:
        # Box plot
        fig = px.box(df, x=var_name2, y=var_name1, title=f"Box plot of {var_name1} by {var_name2}")
        fig.update_layout(
                    xaxis_title=var_name1, 
                    yaxis_title=var_name2,
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
        st.plotly_chart(fig, use_container_width=True)
    
    # Case 3: Both variables are categorical
    elif var_data1.dtype in ['object', 'category'] and var_data2.dtype in ['object', 'category']:
        # Stacked bar plot
        contingency_table = pd.crosstab(df[var_name1], df[var_name2])
        fig = px.bar(contingency_table, barmode='stack', title=f"Stacked bar plot of {var_name1} and {var_name2}")
        fig.update_layout(
                    xaxis_title=var_name1, 
                    yaxis_title='Count',
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
        st.plotly_chart(fig, use_container_width=True)

        # Heatmap of the contingency table
        fig = go.Figure(data=go.Heatmap(z=contingency_table.values, x=contingency_table.columns, y=contingency_table.index,
                                    colorscale='Viridis'))
        fig.update_layout(
                    title=f"Heatmap of {var_name1} vs {var_name2}", 
                    xaxis_title=var_name2, 
                    yaxis_title=var_name1,
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
        st.plotly_chart(fig, use_container_width=True)
    
    # Case 4: Same as 2 but the other way around
    else:
        # Box plot
        fig = px.box(df, x=var_name1, y=var_name2, title=f"Box plot of {var_name2} by {var_name1}")
        fig.update_layout(
                    xaxis_title=var_name2, 
                    yaxis_title=var_name1,
                    template="seaborn",  # Choose a template (e.g., "plotly_dark", "ggplot2", etc.)
                    showlegend=True,
                    legend = dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                )
        st.plotly_chart(fig, use_container_width=True)

    st.header('Correlation analysis', divider='rainbow')
    # Select only numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    
    # Calculate the correlation matrix
    corr_matrix = numeric_df.corr()
    
    # Plot the heatmap
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',  # Seaborn-like diverging colorscale
        colorbar=dict(title="Correlation Coefficient", ticksuffix="", outlinewidth=0),
        zmin=-1, zmax=1,
        hovertemplate="X: %{x}<br>Y: %{y}<br>Correlation: %{z:.2f}<extra></extra>"
    ))

    # Add correlation coefficients as text annotations
    fig.update_traces(
        text=corr_matrix.round(2).values,
        texttemplate="%{text}",  # Format annotations
        textfont=dict(size=10)#,  # Smaller text to avoid clutter
        #hoverinfo='text'
    )

    # Update layout
    fig.update_layout(
        title=dict(
            text="Correlation Matrix of Numeric Variables",
            x=0,  # Left align the title
            xanchor='left'
        ),
        xaxis=dict(
            tickangle=45,
            showgrid=False,  # No gridlines
            zeroline=False,
            showticklabels=True
        ),
        yaxis=dict(
            tickangle=0,
            showgrid=False,  # No gridlines
            zeroline=False,
            showticklabels=True
        ),
        font=dict(
            family="Arial",  # Similar to Seaborn's default
            size=12
        ),
        template="seaborn"  # Use the built-in "seaborn" template
    )

    # Show the plot
    st.plotly_chart(fig, use_container_width=True)