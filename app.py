import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Set page configuration
st.set_page_config(page_title="App Review Analysis Tool", layout="wide")

# App purpose and column description
st.title("App Review Analysis Tool")
st.write("""
This tool analyzes app reviews data to identify trends, topics, and issues over time.
The analysis requires a CSV file with the following columns:
- **reviewId**: Unique identifier for each review
- **review**: The full text of the review
- **score**: Numerical rating (1-5)
- **datetime**: The date/time when the review was submitted
- **topic**: The main topic category of the review
- **problem**: Description of the specific problem
- **sentiment**: Sentiment of the review (positive, negative, neutral)
- **issue**: Specific issue identified in the review
- **company**: Company or app name
""")

# File upload section
st.header("1. Upload CSV File")
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read the data
    df = pd.read_csv(uploaded_file)
    
    # Preview the data
    st.header("2. Data Preview")
    st.dataframe(df.head())
    
    # Check if data contains required columns
    required_columns = ['topic', 'issue', 'datetime', 'company']
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Missing required columns: {', '.join(missing_columns)}")
    else:
        # Convert datetime to datetime format if it's not already
        if pd.api.types.is_object_dtype(df['datetime']):
            try:
                df['datetime'] = pd.to_datetime(df['datetime'])
                # Extract month and year for trend analysis
                df['month_year'] = df['datetime'].dt.strftime('%Y-%m')
            except Exception as e:
                st.error(f"Error converting datetime column: {e}")
        
        # User confirmation
        st.header("3. Confirm Data")
        confirm = st.radio("Are you happy with this data?", ("Yes", "No"), index=1)
        
        if confirm == "Yes":
            st.header("4. Analysis")
            
            # Create tabs for different analyses
            tab1, tab2 = st.tabs(["Topic Analysis", "Issue Analysis by Topic"])
            
            with tab1:
                # Topic Analysis
                st.subheader("Topic Analysis")
                
                # Get topic counts by month
                topic_counts = df.groupby(['month_year', 'topic']).size().reset_index(name='count')
                
                # Calculate percentages
                total_by_month = topic_counts.groupby('month_year')['count'].sum().reset_index()
                topic_counts = topic_counts.merge(total_by_month, on='month_year', suffixes=('', '_total'))
                topic_counts['percentage'] = (topic_counts['count'] / topic_counts['count_total']) * 100
                
                # Sort months chronologically
                all_months = sorted(topic_counts['month_year'].unique())
                topic_counts['month_year'] = pd.Categorical(topic_counts['month_year'], categories=all_months, ordered=True)
                
                # Visualization options
                st.write("Select visualization type:")
                viz_type = st.radio("Chart Type", ["Trended Chart", "Bar Chart", "Pie Chart"], horizontal=True)
                
                if viz_type == "Trended Chart":
                    # Metric selection (Count or Percentage)
                    metric = st.radio("Metric", ["Count", "Percentage"], horizontal=True)
                    
                    if metric == "Count":
                        # Line chart for counts
                        fig = px.line(
                            topic_counts, 
                            x='month_year', 
                            y='count', 
                            color='topic',
                            title='Topic Trends Over Time (Count)',
                            labels={'month_year': 'Month', 'count': 'Count', 'topic': 'Topic'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Code to recreate the chart
                        st.subheader("Python code to recreate this chart:")
                        code = '''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
topic_counts = df.groupby(['month_year', 'topic']).size().reset_index(name='count')

# Sort months chronologically
all_months = sorted(topic_counts['month_year'].unique())
topic_counts['month_year'] = pd.Categorical(topic_counts['month_year'], categories=all_months, ordered=True)

# Create the line chart
fig = px.line(
    topic_counts, 
    x='month_year', 
    y='count', 
    color='topic',
    title='Topic Trends Over Time (Count)',
    labels={'month_year': 'Month', 'count': 'Count', 'topic': 'Topic'}
)
fig.show()
'''
                        st.code(code, language='python')
                        
                    else:  # Percentage
                        # Stacked area chart for percentages
                        fig = px.area(
                            topic_counts, 
                            x='month_year', 
                            y='percentage', 
                            color='topic',
                            title='Topic Trends Over Time (Percentage)',
                            labels={'month_year': 'Month', 'percentage': 'Percentage', 'topic': 'Topic'},
                            groupnorm='percent'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Code to recreate the chart
                        st.subheader("Python code to recreate this chart:")
                        code = '''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
topic_counts = df.groupby(['month_year', 'topic']).size().reset_index(name='count')

# Calculate percentages
total_by_month = topic_counts.groupby('month_year')['count'].sum().reset_index()
topic_counts = topic_counts.merge(total_by_month, on='month_year', suffixes=('', '_total'))
topic_counts['percentage'] = (topic_counts['count'] / topic_counts['count_total']) * 100

# Sort months chronologically
all_months = sorted(topic_counts['month_year'].unique())
topic_counts['month_year'] = pd.Categorical(topic_counts['month_year'], categories=all_months, ordered=True)

# Create the stacked area chart
fig = px.area(
    topic_counts, 
    x='month_year', 
    y='percentage', 
    color='topic',
    title='Topic Trends Over Time (Percentage)',
    labels={'month_year': 'Month', 'percentage': 'Percentage', 'topic': 'Topic'},
    groupnorm='percent'
)
fig.show()
'''
                        st.code(code, language='python')
                
                elif viz_type == "Bar Chart":
                    # Aggregated topic counts overall
                    topic_overall = df.groupby('topic').size().reset_index(name='count')
                    
                    # Sorting options for bar chart
                    sort_option = st.radio("Sort By", ["Count (Ascending)", "Count (Descending)", "Alphabetical"], horizontal=True)
                    
                    if sort_option == "Count (Ascending)":
                        topic_overall = topic_overall.sort_values('count')
                    elif sort_option == "Count (Descending)":
                        topic_overall = topic_overall.sort_values('count', ascending=False)
                    else:  # Alphabetical
                        topic_overall = topic_overall.sort_values('topic')
                    
                    # Create bar chart
                    fig = px.bar(
                        topic_overall, 
                        x='topic', 
                        y='count',
                        color='topic',
                        title='Topics by Count',
                        labels={'topic': 'Topic', 'count': 'Count'},
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Code to recreate the chart
                    st.subheader("Python code to recreate this chart:")
                    code = f'''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
topic_overall = df.groupby('topic').size().reset_index(name='count')

# Sorting by {sort_option.lower()}
'''
                    if sort_option == "Count (Ascending)":
                        code += "topic_overall = topic_overall.sort_values('count')"
                    elif sort_option == "Count (Descending)":
                        code += "topic_overall = topic_overall.sort_values('count', ascending=False)"
                    else:  # Alphabetical
                        code += "topic_overall = topic_overall.sort_values('topic')"
                    
                    code += '''

# Create bar chart
fig = px.bar(
    topic_overall, 
    x='topic', 
    y='count',
    color='topic',
    title='Topics by Count',
    labels={'topic': 'Topic', 'count': 'Count'},
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig.show()
'''
                    st.code(code, language='python')
                
                else:  # Pie Chart
                    # Topic counts for pie chart
                    topic_counts_overall = df.groupby('topic').size().reset_index(name='count')
                    topic_counts_overall = topic_counts_overall.sort_values('count', ascending=False)
                    
                    # Slider for number of topics to show
                    max_topics = len(topic_counts_overall)
                    num_topics = st.slider("Number of topics to show", min_value=1, max_value=max_topics, value=min(5, max_topics))
                    
                    # Prepare data for pie chart with "Other" category
                    if num_topics < max_topics:
                        top_topics = topic_counts_overall.head(num_topics)
                        other_count = topic_counts_overall.iloc[num_topics:]['count'].sum()
                        
                        # Add "Other" category
                        other_row = pd.DataFrame({'topic': ['Other'], 'count': [other_count]})
                        pie_data = pd.concat([top_topics, other_row], ignore_index=True)
                    else:
                        pie_data = topic_counts_overall
                    
                    # Create pie chart
                    fig = px.pie(
                        pie_data, 
                        values='count', 
                        names='topic',
                        title='Distribution of Topics',
                        color_discrete_sequence=px.colors.qualitative.Bold
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Code to recreate the chart
                    st.subheader("Python code to recreate this chart:")
                    code = f'''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
topic_counts_overall = df.groupby('topic').size().reset_index(name='count')
topic_counts_overall = topic_counts_overall.sort_values('count', ascending=False)

# Number of topics to show
num_topics = {num_topics}

# Prepare data for pie chart with "Other" category
if num_topics < len(topic_counts_overall):
    top_topics = topic_counts_overall.head(num_topics)
    other_count = topic_counts_overall.iloc[num_topics:]['count'].sum()
    
    # Add "Other" category
    other_row = pd.DataFrame({{'topic': ['Other'], 'count': [other_count]}})
    pie_data = pd.concat([top_topics, other_row], ignore_index=True)
else:
    pie_data = topic_counts_overall

# Create pie chart
fig = px.pie(
    pie_data, 
    values='count', 
    names='topic',
    title='Distribution of Topics',
    color_discrete_sequence=px.colors.qualitative.Bold
)
fig.show()
'''
                    st.code(code, language='python')
            
            with tab2:
                # Issue Analysis by Selected Topic
                st.subheader("Issue Analysis by Topic")
                
                # Topic selection
                topics = sorted(df['topic'].unique())
                selected_topic = st.selectbox("Select a topic", topics)
                
                # Filter data for selected topic
                topic_df = df[df['topic'] == selected_topic]
                
                # Group issues by month
                issue_counts = topic_df.groupby(['month_year', 'issue']).size().reset_index(name='count')
                
                # Calculate percentages
                total_by_month = issue_counts.groupby('month_year')['count'].sum().reset_index()
                issue_counts = issue_counts.merge(total_by_month, on='month_year', suffixes=('', '_total'))
                issue_counts['percentage'] = (issue_counts['count'] / issue_counts['count_total']) * 100
                
                # Sort months chronologically
                all_months = sorted(issue_counts['month_year'].unique())
                issue_counts['month_year'] = pd.Categorical(issue_counts['month_year'], categories=all_months, ordered=True)
                
                # Metric selection (Count or Percentage)
                metric = st.radio("Metric for Issue Analysis", ["Count", "Percentage"], horizontal=True)
                
                if metric == "Count":
                    # Line chart for counts
                    if not issue_counts.empty:
                        fig = px.line(
                            issue_counts, 
                            x='month_year', 
                            y='count', 
                            color='issue',
                            title=f'Issue Trends for {selected_topic} (Count)',
                            labels={'month_year': 'Month', 'count': 'Count', 'issue': 'Issue'}
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Code to recreate the chart
                        st.subheader("Python code to recreate this chart:")
                        code = f'''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
# Filter data for selected topic
topic_df = df[df['topic'] == '{selected_topic}']

# Group issues by month
issue_counts = topic_df.groupby(['month_year', 'issue']).size().reset_index(name='count')

# Sort months chronologically
all_months = sorted(issue_counts['month_year'].unique())
issue_counts['month_year'] = pd.Categorical(issue_counts['month_year'], categories=all_months, ordered=True)

# Create line chart
fig = px.line(
    issue_counts, 
    x='month_year', 
    y='count', 
    color='issue',
    title='Issue Trends for {selected_topic} (Count)',
    labels={{'month_year': 'Month', 'count': 'Count', 'issue': 'Issue'}}
)
fig.show()
'''
                        st.code(code, language='python')
                    else:
                        st.warning(f"No issues found for topic: {selected_topic}")
                
                else:  # Percentage
                    # Stacked area chart for percentages
                    if not issue_counts.empty:
                        fig = px.area(
                            issue_counts, 
                            x='month_year', 
                            y='percentage', 
                            color='issue',
                            title=f'Issue Trends for {selected_topic} (Percentage)',
                            labels={'month_year': 'Month', 'percentage': 'Percentage', 'issue': 'Issue'},
                            groupnorm='percent'
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Code to recreate the chart
                        st.subheader("Python code to recreate this chart:")
                        code = f'''
import pandas as pd
import plotly.express as px

# Assuming df is your dataframe with the data
# Filter data for selected topic
topic_df = df[df['topic'] == '{selected_topic}']

# Group issues by month
issue_counts = topic_df.groupby(['month_year', 'issue']).size().reset_index(name='count')

# Calculate percentages
total_by_month = issue_counts.groupby('month_year')['count'].sum().reset_index()
issue_counts = issue_counts.merge(total_by_month, on='month_year', suffixes=('', '_total'))
issue_counts['percentage'] = (issue_counts['count'] / issue_counts['count_total']) * 100

# Sort months chronologically
all_months = sorted(issue_counts['month_year'].unique())
issue_counts['month_year'] = pd.Categorical(issue_counts['month_year'], categories=all_months, ordered=True)

# Create stacked area chart
fig = px.area(
    issue_counts, 
    x='month_year', 
    y='percentage', 
    color='issue',
    title='Issue Trends for {selected_topic} (Percentage)',
    labels={{'month_year': 'Month', 'percentage': 'Percentage', 'issue': 'Issue'}},
    groupnorm='percent'
)
fig.show()
'''
                        st.code(code, language='python')
                    else:
                        st.warning(f"No issues found for topic: {selected_topic}")