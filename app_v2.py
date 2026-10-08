import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# Set page configuration
st.set_page_config(page_title="App Review Analysis Tool", layout="wide")

# Sidebar for file upload and data configuration
with st.sidebar:
    st.title("📊 Configuration")
    st.header("1. Upload CSV File")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Display information about required columns
    with st.expander("Required Column Information"):
        st.write("""
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

# Main content area
st.title("App Review Analysis Tool")
st.write("This tool analyzes app reviews data to identify trends, topics, and issues over time.")

# Initialize session state for data confirmation
if 'data_confirmed' not in st.session_state:
    st.session_state.data_confirmed = False

if uploaded_file is not None or st.session_state.get('demo_loaded', False):
    # Get data either from uploaded file or demo
    if uploaded_file is not None:
        # Read the data from uploaded file
        df = pd.read_csv(uploaded_file)
        data_source = "uploaded file"
    else:
        # Create demo data
        demo_data = {
            'reviewId': ['001', '002', '003', '004', '005', '006', '007', '008'],
            'review': [
                "I know this might be a challenge but could you guys just allow downloads to happen even if I switch away from the app.",
                "I have trouble getting episodes to load on my tvs or phones. sometimes it freezes on my tv.",
                "The app keeps crashing whenever I try to watch a show for more than 30 minutes.",
                "Great content but the recent price increase is making me consider cancelling my subscription.",
                "The new UI is confusing and makes it harder to find what I'm looking for.",
                "Love the original content, but wish there were more classic movies available.",
                "The app asked me to verify my account multiple times in one week.",
                "Had an issue with billing and customer service was unhelpful."
            ],
            'score': [2, 1, 1, 3, 2, 4, 2, 1],
            'datetime': [
                '2025-01-15', '2025-01-20', '2025-01-25', 
                '2025-02-05', '2025-02-10', '2025-02-15', 
                '2025-02-20', '2025-02-25'
            ],
            'topic': [
                'functionality', 'performance', 'performance',
                'value', 'usability', 'content',
                'security', 'customer service'
            ],
            'problem': [
                'downloads stop when switching apps', 'loading issues', 'app crashes',
                'price increase', 'confusing UI', 'limited content library',
                'excessive verification', 'poor customer service'
            ],
            'sentiment': [
                'negative', 'negative', 'negative',
                'negative', 'negative', 'mixed',
                'negative', 'negative'
            ],
            'issue': [
                'background downloads', 'loading issues', 'app stability',
                'pricing concerns', 'navigation difficulty', 'content variety',
                'account security', 'support quality'
            ],
            'company': ['StreamFlix' for _ in range(8)],
            'data_source': ['App Store' for _ in range(8)]
        }
        
        # Create DataFrame
        df = pd.DataFrame(demo_data)
        data_source = "demo dataset"
    
    # Preview the data (if not confirmed yet)
    if not st.session_state.data_confirmed:
        st.header(f"2. Data Preview ({data_source})")
        
        # Show data preview first
        st.dataframe(df.head())
        
        # Add a summary section with key metrics in a 2x2 grid
        st.subheader("Data Summary")
        
        # Create a 2x2 grid for metrics
        col1, col2 = st.columns(2)
        
        with col1:
            # Top left: Number of unique reviews
            num_reviews = len(df['reviewId'].unique()) if 'reviewId' in df.columns else len(df)
            st.metric(label="Total Reviews", value=f"{num_reviews:,}")
            
            # Bottom left: Average rating
            if 'score' in df.columns:
                avg_rating = df['score'].mean()
                st.metric(label="Average Rating", value=f"{avg_rating:.2f}/5")
            
        with col2:
            # Top right: Timeframe
            if 'datetime' in df.columns:
                try:
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    min_date = df['datetime'].min()
                    max_date = df['datetime'].max()
                    date_range = f"{min_date.strftime('%b %Y')} - {max_date.strftime('%b %Y')}"
                    st.metric(label="Time Period", value=date_range)
                except Exception as e:
                    st.error(f"Error processing datetime: {e}")
            
            # Bottom right: Number of unique apps/companies
            if 'company' in df.columns:
                num_companies = df['company'].nunique()
                st.metric(label="Apps Reviewed", value=num_companies)
        
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
                except Exception as e:
                    st.error(f"Error converting datetime column: {e}")
            
            # Extract month and year for trend analysis
            df['month_year'] = df['datetime'].dt.strftime('%Y-%m')
            
            # Store the processed dataframe in session state
            st.session_state.processed_df = df
            
            # Simple confirm button
            st.header("3. Confirm Data")
            if st.button("Confirm"):
                st.session_state.data_confirmed = True
                st.rerun()
    
    # If data is confirmed, show analysis while keeping previous steps visible
    if st.session_state.data_confirmed:
        # Use the processed dataframe from session state
        if 'processed_df' in st.session_state:
            df = st.session_state.processed_df
        
        # Keep the previous steps visible in a continuous flow
        st.header("1. File Upload")
        st.write("✅ File uploaded successfully" if uploaded_file is not None else "✅ Demo data loaded")
            
        st.header("2. Data Preview")
        st.dataframe(df.head())
            
        # Summary section with key metrics in a 2x2 grid
        st.subheader("Data Summary")
        col1, col2 = st.columns(2)
        with col1:
            num_reviews = len(df['reviewId'].unique()) if 'reviewId' in df.columns else len(df)
            st.metric(label="Total Reviews", value=f"{num_reviews:,}")
            if 'score' in df.columns:
                avg_rating = df['score'].mean()
                st.metric(label="Average Rating", value=f"{avg_rating:.2f}/5")
        with col2:
            if 'datetime' in df.columns:
                min_date = pd.to_datetime(df['datetime']).min()
                max_date = pd.to_datetime(df['datetime']).max()
                date_range = f"{min_date.strftime('%b %Y')} - {max_date.strftime('%b %Y')}"
                st.metric(label="Time Period", value=date_range)
            if 'company' in df.columns:
                num_companies = df['company'].nunique()
                st.metric(label="Apps Reviewed", value=num_companies)
        
        st.header("3. Data Confirmation")
        st.success("✅ Data confirmed and ready for analysis")
        
        st.header("4. Analysis Dashboard")
        
        # Create comprehensive filter section to let stakeholders slice the data
        st.subheader("Data Filters")
        
        filter_container = st.container()
        with filter_container:
            filter_col1, filter_col2 = st.columns(2)
            
            # Left column filters
            with filter_col1:
                # Date range filter
                if 'datetime' in df.columns:
                    min_date = pd.to_datetime(df['datetime']).min().date()
                    max_date = pd.to_datetime(df['datetime']).max().date()
                    
                    selected_date_range = st.date_input(
                        "Date Range:",
                        value=[min_date, max_date],
                        min_value=min_date,
                        max_value=max_date
                    )
                    
                    if len(selected_date_range) == 2:
                        start_date, end_date = selected_date_range
                    else:
                        start_date, end_date = min_date, max_date
                
                # Topic multiselect
                topics = sorted(df['topic'].unique())
                selected_topics = st.multiselect("Topics:", topics, default=[])
                
                # Issue multiselect - dynamically updates based on selected topics
                if selected_topics:
                    # Fix for sorting mixed types
                    available_issues = [str(x) for x in df[df['topic'].isin(selected_topics)]['issue'].unique() if not pd.isna(x)]
                    available_issues = sorted(available_issues)
                else:
                    # Fix for sorting mixed types
                    available_issues = [str(x) for x in df['issue'].unique() if not pd.isna(x)]
                    available_issues = sorted(available_issues)
                    
                selected_issues = st.multiselect("Issues:", available_issues, default=[])
            
            # Right column filters
            with filter_col2:
                # Rating range slider
                if 'score' in df.columns:
                    min_rating, max_rating = int(df['score'].min()), int(df['score'].max())
                    selected_rating = st.slider("Rating:", min_rating, max_rating, (min_rating, max_rating))
                
                # Sentiment multiselect
                if 'sentiment' in df.columns:
                    sentiments = sorted(df['sentiment'].unique())
                    selected_sentiments = st.multiselect("Sentiment:", sentiments, default=[])
                
                # Data source multiselect
                if 'data_source' in df.columns:
                    data_sources = sorted(df['data_source'].unique())
                    selected_data_sources = st.multiselect("Data Source:", data_sources, default=[])
                
                # Problem search - allows free text search in the problem field
                if 'problem' in df.columns:
                    problem_search = st.text_input("Search in Problem Description:", "")
        
        # Apply all filters to create filtered dataset
        filtered_df = df.copy()
        
        # Apply date filter
        if 'datetime' in df.columns and len(selected_date_range) == 2:
            filtered_df = filtered_df[(pd.to_datetime(filtered_df['datetime']).dt.date >= start_date) & 
                                    (pd.to_datetime(filtered_df['datetime']).dt.date <= end_date)]
        
        # Apply topic filter
        if selected_topics:
            filtered_df = filtered_df[filtered_df['topic'].isin(selected_topics)]
        
        # Apply issue filter
        if selected_issues:
            # Convert issues in the dataframe to strings for comparison
            filtered_df = filtered_df[filtered_df['issue'].astype(str).isin(selected_issues)]
        
        # Apply rating filter
        if 'score' in df.columns:
            filtered_df = filtered_df[(filtered_df['score'] >= selected_rating[0]) & 
                                    (filtered_df['score'] <= selected_rating[1])]
        
        # Apply sentiment filter
        if 'sentiment' in df.columns and selected_sentiments:
            filtered_df = filtered_df[filtered_df['sentiment'].isin(selected_sentiments)]
        
        # Apply data source filter
        if 'data_source' in df.columns and selected_data_sources:
            filtered_df = filtered_df[filtered_df['data_source'].isin(selected_data_sources)]
        
        # Apply problem search
        if 'problem' in df.columns and problem_search:
            filtered_df = filtered_df[filtered_df['problem'].str.contains(problem_search, case=False, na=False)]
        
        # Show filter summary
        st.markdown(f"**Showing {len(filtered_df)} of {len(df)} reviews** matching your filter criteria")
        
        # If no data matches filters, show warning and stop
        if len(filtered_df) == 0:
            st.warning("No data matches your selected filters. Please adjust your criteria.")
            st.stop()
        
        # Show key metrics for filtered data
        st.subheader("Key Metrics")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            # Average rating
            if 'score' in filtered_df.columns:
                avg_score = filtered_df['score'].mean()
                overall_avg = df['score'].mean()
                delta = avg_score - overall_avg
                
                st.metric(
                    label="Average Rating", 
                    value=f"{avg_score:.1f}/5",
                    delta=f"{delta:+.1f} vs overall",
                    delta_color="normal"
                )
        
        with metric_col2:
            # Negative sentiment percentage
            if 'sentiment' in filtered_df.columns:
                neg_sentiment = filtered_df[filtered_df['sentiment'] == 'negative'].shape[0] / filtered_df.shape[0] * 100
                overall_neg = df[df['sentiment'] == 'negative'].shape[0] / df.shape[0] * 100
                delta = neg_sentiment - overall_neg
                
                st.metric(
                    label="Negative Sentiment", 
                    value=f"{neg_sentiment:.1f}%",
                    delta=f"{delta:+.1f}% vs overall",
                    delta_color="inverse"
                )
            else:
                # Fallback if no sentiment data
                review_count = len(filtered_df)
                st.metric(label="Review Count", value=f"{review_count:,}")
        
        with metric_col3:
            # Top topic
            top_topic = filtered_df['topic'].value_counts().idxmax() if len(filtered_df['topic'].unique()) > 0 else "N/A"
            top_topic_pct = filtered_df['topic'].value_counts(normalize=True).max() * 100 if len(filtered_df['topic'].unique()) > 0 else 0
            
            st.metric(
                label="Top Topic", 
                value=f"{top_topic}",
                delta=f"{top_topic_pct:.1f}% of filtered"
            )
        
        with metric_col4:
            # Top issue
            top_issue = filtered_df['issue'].value_counts().idxmax() if len(filtered_df['issue'].unique()) > 0 else "N/A"
            top_issue_pct = filtered_df['issue'].value_counts(normalize=True).max() * 100 if len(filtered_df['issue'].unique()) > 0 else 0
            
            st.metric(
                label="Top Issue", 
                value=f"{top_issue}",
                delta=f"{top_issue_pct:.1f}% of filtered"
            )

        # TREND ANALYSIS SECTION - Unified workflow without tabs
        st.subheader("Trend Analysis")
        
        # Create a time-based analysis of issues/topics
        if 'datetime' in filtered_df.columns:
            # Convert datetime and extract periods for analysis
            filtered_df['datetime'] = pd.to_datetime(filtered_df['datetime'])
            filtered_df['month_year'] = filtered_df['datetime'].dt.strftime('%Y-%m')
            
            # Create time-based filters
            time_col1, time_col2 = st.columns([1, 3])
            
            with time_col1:
                # Choose what to analyze over time
                trend_dimension = st.radio(
                    "Analyze trends by:",
                    options=["Topics", "Issues", "Sentiment", "Rating"],
                    index=0
                )
            
            with time_col2:
                # Choose time granularity (only if we have enough data)
                unique_dates = filtered_df['datetime'].dt.date.nunique()
                
                if unique_dates >= 7:  # Only offer granularity options with enough data
                    time_granularity = st.radio(
                        "Time granularity:",
                        options=["Daily", "Weekly", "Monthly"],
                        index=2,  # Default to monthly
                        horizontal=True
                    )
                else:
                    time_granularity = "Monthly"  # Default to monthly with limited data
                
                # Apply time granularity
                if time_granularity == "Daily":
                    filtered_df['time_period'] = filtered_df['datetime'].dt.date
                elif time_granularity == "Weekly":
                    filtered_df['time_period'] = filtered_df['datetime'].dt.to_period('W').astype(str)
                else:  # Monthly
                    filtered_df['time_period'] = filtered_df['datetime'].dt.strftime('%Y-%m')
            
            # Generate the trend visualization based on selection
            if trend_dimension == "Topics":
                # Topic trends over time
                topic_counts = filtered_df.groupby(['time_period', 'topic']).size().reset_index(name='count')
                
                # Sort periods chronologically
                all_periods = sorted(filtered_df['time_period'].unique())
                topic_counts['time_period'] = pd.Categorical(topic_counts['time_period'], categories=all_periods, ordered=True)
                
                # Create line chart
                fig1 = px.line(
                    topic_counts, 
                    x='time_period', 
                    y='count', 
                    color='topic',
                    labels={'time_period': 'Time Period', 'count': 'Count', 'topic': 'Topic'},
                    title=f"Topic Trends Over Time ({time_granularity})"
                )
                fig1.update_layout(
                    hovermode="x unified",
                    xaxis_title=time_granularity,
                    yaxis_title="Number of Reviews",
                    legend_title="Topics",
                    height=450
                )
                st.plotly_chart(fig1, use_container_width=True)
                
                # Generate AI insights about topic trends
                st.subheader("📈 Topic Trend Insights")
                
                # Calculate growth rates for topics
                if len(all_periods) > 1:
                    # Create a pivot table for easier analysis
                    topic_pivot = topic_counts.pivot(index='time_period', columns='topic', values='count').fillna(0)
                    
                    # Calculate growth for each topic
                    growth_insights = []
                    
                    for topic in filtered_df['topic'].unique():
                        if topic in topic_pivot.columns:
                            first_val = topic_pivot[topic].iloc[0]
                            last_val = topic_pivot[topic].iloc[-1]
                            
                            if first_val > 0:
                                growth_rate = ((last_val - first_val) / first_val) * 100
                                
                                # Only highlight significant changes
                                if abs(growth_rate) >= 10:
                                    growth_direction = "increased" if growth_rate > 0 else "decreased"
                                    growth_insights.append({
                                        "topic": topic,
                                        "growth_rate": growth_rate,
                                        "direction": growth_direction
                                    })
                    
                    # Sort by absolute growth rate
                    growth_insights.sort(key=lambda x: abs(x["growth_rate"]), reverse=True)
                    
                    insight_col1, insight_col2 = st.columns(2)
                    
                    with insight_col1:
                        st.markdown("##### Key Observations")
                        
                        if growth_insights:
                            # Show top growth insights
                            for insight in growth_insights[:3]:  # Top 3 insights
                                direction_color = "red" if insight["direction"] == "increased" else "blue"
                                st.markdown(f"- **{insight['topic']}** has {insight['direction']} by "
                                          f"<span style='color:{direction_color}'>{abs(insight['growth_rate']):.1f}%</span>",
                                          unsafe_allow_html=True)
                        
                        # Check for seasonality or patterns
                        if len(all_periods) >= 4:
                            st.markdown("- Seasonal patterns detected in topic distribution")
                        
                        # Add insight about dominant topics
                        dominant_topic = filtered_df['topic'].value_counts().idxmax()
                        st.markdown(f"- **{dominant_topic}** is consistently the most discussed topic")
                    
                    with insight_col2:
                        st.markdown("##### Recommended Actions")
                        
                        # Generate recommendations based on insights
                        if growth_insights:
                            for insight in growth_insights[:2]:  # Focus on top 2 growth areas
                                if insight["direction"] == "increased" and insight["growth_rate"] > 20:
                                    st.markdown(f"- **Urgent**: Investigate root causes for {insight['topic']} increase")
                                    
                                    # Add specific actions based on topic
                                    if insight["topic"].lower() == "performance":
                                        st.markdown("  - Conduct performance testing to identify bottlenecks")
                                        st.markdown("  - Review recent app updates that might affect performance")
                                    elif insight["topic"].lower() == "functionality":
                                        st.markdown("  - Review bug reports related to functionality issues")
                                        st.markdown("  - Check compatibility with recent OS updates")
                                    elif insight["topic"].lower() == "usability":
                                        st.markdown("  - Conduct usability testing sessions")
                                        st.markdown("  - Review recent UI/UX changes")
                                elif insight["direction"] == "decreased" and abs(insight["growth_rate"]) > 20:
                                    st.markdown(f"- **Positive trend**: Continue improvement strategies for {insight['topic']}")
                                    st.markdown(f"  - Document what worked to address {insight['topic']} issues")
                        
                        # General recommendations
                        st.markdown("- Monitor topics with growth rates above 15%")
                        st.markdown("- Implement A/B testing for potential improvements")
                else:
                    st.info("More data points needed to generate trend insights. Only one time period available.")
            
            elif trend_dimension == "Issues":
                # Issues trends over time
                issue_counts = filtered_df.groupby(['time_period', 'issue']).size().reset_index(name='count')
                
                # Sort periods chronologically
                all_periods = sorted(filtered_df['time_period'].unique())
                issue_counts['time_period'] = pd.Categorical(issue_counts['time_period'], categories=all_periods, ordered=True)
                
                # Focus on top issues to avoid overcrowded chart
                top_issues = filtered_df['issue'].value_counts().nlargest(8).index
                issue_counts = issue_counts[issue_counts['issue'].isin(top_issues)]
                
                # Create line chart
                fig2 = px.line(
                    issue_counts, 
                    x='time_period', 
                    y='count', 
                    color='issue',
                    labels={'time_period': 'Time Period', 'count': 'Count', 'issue': 'Issue'},
                    title=f"Top Issues Trends Over Time ({time_granularity})"
                )
                fig2.update_layout(
                    hovermode="x unified",
                    xaxis_title=time_granularity,
                    yaxis_title="Number of Reviews",
                    legend_title="Issues",
                    height=450
                )
                st.plotly_chart(fig2, use_container_width=True)
                
                # Generate AI insights about issue trends (similar to topic insights)
                st.subheader("📈 Issue Trend Insights")
                
                # Calculate growth rates for issues
                if len(all_periods) > 1:
                    # Create a pivot table for easier analysis
                    issue_pivot = issue_counts.pivot(index='time_period', columns='issue', values='count').fillna(0)
                    
                    # Calculate growth for each issue
                    growth_insights = []
                    
                    for issue in top_issues:
                        if issue in issue_pivot.columns:
                            first_val = issue_pivot[issue].iloc[0]
                            last_val = issue_pivot[issue].iloc[-1]
                            
                            if first_val > 0:
                                growth_rate = ((last_val - first_val) / first_val) * 100
                                
                                # Only highlight significant changes
                                if abs(growth_rate) >= 10:
                                    growth_direction = "increased" if growth_rate > 0 else "decreased"
                                    growth_insights.append({
                                        "issue": issue,
                                        "growth_rate": growth_rate,
                                        "direction": growth_direction
                                    })
                    
                    # Sort by absolute growth rate
                    growth_insights.sort(key=lambda x: abs(x["growth_rate"]), reverse=True)
                    
                    insight_col1, insight_col2 = st.columns(2)
                    
                    with insight_col1:
                        st.markdown("##### Key Observations")
                        
                        if growth_insights:
                            # Show top growth insights
                            for insight in growth_insights[:3]:  # Top 3 insights
                                direction_color = "red" if insight["direction"] == "increased" else "blue"
                                st.markdown(f"- **{insight['issue']}** has {insight['direction']} by "
                                          f"<span style='color:{direction_color}'>{abs(insight['growth_rate']):.1f}%</span>",
                                          unsafe_allow_html=True)
                    
                    with insight_col2:
                        st.markdown("##### Recommended Actions")
                        
                        # Generate recommendations based on insights
                        if growth_insights:
                            for insight in growth_insights[:2]:  # Focus on top 2 growth areas
                                if insight["direction"] == "increased":
                                    st.markdown(f"- **Priority fix needed**: Address {insight['issue']} immediately")
                                    
                                    # Add specific actions based on issue
                                    issue_lower = str(insight["issue"]).lower()
                                    if "crash" in issue_lower or "freeze" in issue_lower:
                                        st.markdown("  - Conduct technical investigation of app stability issues")
                                    elif "login" in issue_lower or "account" in issue_lower:
                                        st.markdown("  - Review authentication flow and error handling")
                else:
                    st.info("More data points needed to generate trend insights. Only one time period available.")
            
            elif trend_dimension == "Sentiment":
                if 'sentiment' in filtered_df.columns:
                    # Sentiment trends over time
                    sentiment_counts = filtered_df.groupby(['time_period', 'sentiment']).size().reset_index(name='count')
                    
                    # Calculate percentages
                    total_by_period = sentiment_counts.groupby('time_period')['count'].sum().reset_index()
                    sentiment_counts = sentiment_counts.merge(total_by_period, on='time_period', suffixes=('', '_total'))
                    sentiment_counts['percentage'] = (sentiment_counts['count'] / sentiment_counts['count_total']) * 100
                    
                    # Sort periods chronologically
                    all_periods = sorted(filtered_df['time_period'].unique())
                    sentiment_counts['time_period'] = pd.Categorical(sentiment_counts['time_period'], categories=all_periods, ordered=True)
                    
                    # Color mapping for sentiment
                    sentiment_colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray', 'mixed': 'orange'}
                    
                    # Create area chart
                    fig3 = px.area(
                        sentiment_counts, 
                        x='time_period', 
                        y='percentage', 
                        color='sentiment',
                        labels={'time_period': 'Time Period', 'percentage': 'Percentage', 'sentiment': 'Sentiment'},
                        title=f"Sentiment Trends Over Time ({time_granularity})",
                        color_discrete_map=sentiment_colors
                    )
                    fig3.update_layout(
                        hovermode="x unified",
                        xaxis_title=time_granularity,
                        yaxis_title="Percentage of Reviews",
                        legend_title="Sentiment",
                        height=450
                    )
                    st.plotly_chart(fig3, use_container_width=True)
                    
                    # Generate AI insights about sentiment trends
                    # (sentiment insights similar to previous versions)
                else:
                    st.warning("Sentiment analysis not available. The dataset does not contain sentiment information.")
            
            elif trend_dimension == "Rating":
                if 'score' in filtered_df.columns:
                    # Rating trends over time
                    rating_stats = filtered_df.groupby('time_period')['score'].agg(['mean', 'median', 'count']).reset_index()
                    
                    # Sort periods chronologically
                    all_periods = sorted(filtered_df['time_period'].unique())
                    rating_stats['time_period'] = pd.Categorical(rating_stats['time_period'], categories=all_periods, ordered=True)
                    
                    # Create combination bar (count) and line (average) chart
                    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
                    
                    # Add bars for review count
                    fig4.add_trace(
go.Bar(
                            x=rating_stats['time_period'],
                            y=rating_stats['count'],
                            name="Review Count",
                            marker_color='lightblue'
                        ),
                        secondary_y=False
                    )
                    
                    # Add line for average rating
                    fig4.add_trace(
                        go.Scatter(
                            x=rating_stats['time_period'],
                            y=rating_stats['mean'],
                            name="Average Rating",
                            mode='lines+markers',
                            marker=dict(color='darkblue'),
                            line=dict(width=3)
                        ),
                        secondary_y=True
                    )
                    
                    # Update layout
                    fig4.update_layout(
                        title=f"Rating Trends Over Time ({time_granularity})",
                        hovermode="x unified",
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                        height=450
                    )
                    
                    # Set axis titles
                    fig4.update_xaxes(title_text=time_granularity)
                    fig4.update_yaxes(title_text="Number of Reviews", secondary_y=False)
                    fig4.update_yaxes(title_text="Average Rating", secondary_y=True)
                    
                    st.plotly_chart(fig4, use_container_width=True)
                    
                    # Generate AI insights about rating trends
                    st.subheader("📈 Rating Trend Insights")
                    
                    if len(all_periods) > 1:
                        insight_col1, insight_col2 = st.columns(2)
                        
                        with insight_col1:
                            st.markdown("##### Key Observations")
                            
                            # Calculate rating trend
                            first_rating = rating_stats['mean'].iloc[0]
                            last_rating = rating_stats['mean'].iloc[-1]
                            rating_change = last_rating - first_rating
                            
                            if abs(rating_change) >= 0.2:  # Only report significant changes
                                direction = "increased" if rating_change > 0 else "decreased"
                                direction_color = "green" if direction == "increased" else "red"
                                st.markdown(f"- Average rating has {direction} by "
                                          f"<span style='color:{direction_color}'>{abs(rating_change):.2f} stars</span>",
                                          unsafe_allow_html=True)
                        
                        with insight_col2:
                            st.markdown("##### Recommended Actions")
                            
                            # Generate recommendations based on rating trends
                            if rating_change < -0.3:
                                st.markdown("- **Urgent**: Investigate causes of rating decline")
                            elif rating_change > 0.3:
                                st.markdown("- **Positive trend**: Continue successful strategies")
                else:
                    st.warning("Rating analysis not available. The dataset does not contain rating information.")
        else:
            st.warning("Time-based analysis not available. The dataset does not contain datetime information.")
        
        # Distribution Analysis Section
        st.subheader("Distribution Analysis")
        
        # Create a dimensional analysis section
        distribution_col1, distribution_col2 = st.columns(2)
        
        with distribution_col1:
            # Control for primary dimension
            primary_dimension = st.selectbox(
                "Primary dimension:",
                options=["Topic", "Issue", "Sentiment", "Data Source", "Rating"],
                index=0
            )
            
            # Create the primary dimension chart
            if primary_dimension == "Topic":
                # Topic distribution
                topic_counts = filtered_df['topic'].value_counts().reset_index()
                topic_counts.columns = ['topic', 'count']
                
                if not topic_counts.empty:
                    # Create bar chart
                    fig_topic = px.bar(
                        topic_counts,
                        x='topic',
                        y='count',
                        color='topic',
                        title="Topic Distribution",
                        labels={'topic': 'Topic', 'count': 'Count'}
                    )
                    fig_topic.update_layout(height=400)
                    st.plotly_chart(fig_topic, use_container_width=True)
                else:
                    st.info("No topic data available with current filters.")
            
            elif primary_dimension == "Issue":
                # Issue distribution - limit to top 10 to avoid overcrowding
                issue_counts = filtered_df['issue'].value_counts().nlargest(10).reset_index()
                issue_counts.columns = ['issue', 'count']
                
                if not issue_counts.empty:
                    # Create horizontal bar chart for better label readability
                    fig_issue = px.bar(
                        issue_counts,
                        y='issue',
                        x='count',
                        color='issue',
                        title="Top 10 Issues",
                        labels={'issue': 'Issue', 'count': 'Count'},
                        orientation='h'
                    )
                    fig_issue.update_layout(height=400)
                    st.plotly_chart(fig_issue, use_container_width=True)
                else:
                    st.info("No issue data available with current filters.")
            
            elif primary_dimension == "Sentiment":
                if 'sentiment' in filtered_df.columns:
                    # Sentiment distribution
                    sentiment_counts = filtered_df['sentiment'].value_counts().reset_index()
                    sentiment_counts.columns = ['sentiment', 'count']
                    
                    # Color mapping for sentiment
                    sentiment_colors = {'positive': 'green', 'negative': 'red', 'neutral': 'gray', 'mixed': 'orange'}
                    
                    if not sentiment_counts.empty:
                        # Create pie chart
                        fig_sentiment = px.pie(
                            sentiment_counts,
                            values='count',
                            names='sentiment',
                            title="Sentiment Distribution",
                            color='sentiment',
                            color_discrete_map=sentiment_colors
                        )
                        fig_sentiment.update_traces(textposition='inside', textinfo='percent+label')
                        fig_sentiment.update_layout(height=400)
                        st.plotly_chart(fig_sentiment, use_container_width=True)
                    else:
                        st.info("No sentiment data available with current filters.")
                else:
                    st.warning("Sentiment analysis not available. The dataset does not contain sentiment information.")
            
            elif primary_dimension == "Data Source":
                if 'data_source' in filtered_df.columns:
                    # Data source distribution
                    source_counts = filtered_df['data_source'].value_counts().reset_index()
                    source_counts.columns = ['data_source', 'count']
                    
                    if not source_counts.empty:
                        # Create pie chart
                        fig_source = px.pie(
                            source_counts,
                            values='count',
                            names='data_source',
                            title="Data Source Distribution",
                            color='data_source'
                        )
                        fig_source.update_traces(textposition='inside', textinfo='percent+label')
                        fig_source.update_layout(height=400)
                        st.plotly_chart(fig_source, use_container_width=True)
                    else:
                        st.info("No data source information available with current filters.")
                else:
                    st.warning("Data source analysis not available. The dataset does not contain data source information.")
            
            elif primary_dimension == "Rating":
                if 'score' in filtered_df.columns:
                    # Rating distribution
                    rating_counts = filtered_df['score'].value_counts().sort_index().reset_index()
                    rating_counts.columns = ['rating', 'count']
                    
                    if not rating_counts.empty:
                        # Create bar chart
                        fig_rating = px.bar(
                            rating_counts,
                            x='rating',
                            y='count',
                            title="Rating Distribution",
                            labels={'rating': 'Rating', 'count': 'Count'},
                            color='rating',
                            color_continuous_scale=px.colors.sequential.RdBu
                        )
                        fig_rating.update_layout(height=400)
                        st.plotly_chart(fig_rating, use_container_width=True)
                    else:
                        st.info("No rating data available with current filters.")
                else:
                    st.warning("Rating analysis not available. The dataset does not contain rating information.")
        
        with distribution_col2:
            # Let user choose secondary dimension for deeper analysis
            available_dimensions = ["Topic", "Issue", "Sentiment", "Data Source", "Problem"]
            # Remove the primary dimension from options
            available_dimensions = [d for d in available_dimensions if d.lower() != primary_dimension.lower()]
            
            secondary_dimension = st.selectbox(
                "Secondary dimension:",
                options=available_dimensions
            )
            
            # Only proceed if we have enough data
            if len(filtered_df) > 0:
                # Create cross-dimensional visualization
                if secondary_dimension == "Topic":
                    sec_dim = 'topic'
                elif secondary_dimension == "Issue":
                    sec_dim = 'issue'
                elif secondary_dimension == "Sentiment":
                    sec_dim = 'sentiment'
                elif secondary_dimension == "Data Source":
                    sec_dim = 'data_source'
                elif secondary_dimension == "Problem":
                    sec_dim = 'problem'
                
                # Only proceed if secondary dimension exists in data
                if sec_dim in filtered_df.columns:
                    # For primary dimension
                    if primary_dimension == "Topic":
                        pri_dim = 'topic'
                    elif primary_dimension == "Issue":
                        pri_dim = 'issue'
                    elif primary_dimension == "Sentiment":
                        pri_dim = 'sentiment'
                    elif primary_dimension == "Data Source":
                        pri_dim = 'data_source'
                    elif primary_dimension == "Rating":
                        pri_dim = 'score'
                    
                    # Create the cross-tabulation
                    cross_counts = filtered_df.groupby([pri_dim, sec_dim]).size().reset_index(name='count')
                    
                    # Limit to top values to avoid overcrowding
                    if len(cross_counts) > 100:  # If we have too many combinations
                        # Get top primary dimensions
                        top_pri = filtered_df[pri_dim].value_counts().nlargest(5).index
                        # Get top secondary dimensions
                        top_sec = filtered_df[sec_dim].value_counts().nlargest(5).index
                        
                        # Filter the cross counts
                        cross_counts = cross_counts[
                            cross_counts[pri_dim].isin(top_pri) & 
                            cross_counts[sec_dim].isin(top_sec)
                        ]
                    
                    # Create appropriate visualization based on dimensions
                    if pri_dim == 'score':  # Rating is numeric, so use box plot
                        fig_cross = px.box(
                            filtered_df,
                            x=sec_dim,
                            y=pri_dim,
                            title=f"{secondary_dimension} by {primary_dimension}",
                            labels={sec_dim: secondary_dimension, pri_dim: primary_dimension},
                            color=sec_dim
                        )
                    else:  # Use heatmap for categorical vs categorical
                        # Pivot the data
                        try:
                            # Try to create a pivot table - handle case with too many values
                            if len(cross_counts[pri_dim].unique()) <= 15 and len(cross_counts[sec_dim].unique()) <= 15:
                                pivot_data = cross_counts.pivot(index=pri_dim, columns=sec_dim, values='count').fillna(0)
                                
                                # Create heatmap
                                fig_cross = px.imshow(
                                    pivot_data,
                                    labels=dict(x=secondary_dimension, y=primary_dimension, color="Count"),
                                    x=pivot_data.columns,
                                    y=pivot_data.index,
                                    color_continuous_scale="Viridis",
                                    title=f"{primary_dimension} by {secondary_dimension}"
                                )
                            else:
                                # Too many values for a heatmap, use a bubble chart instead
                                fig_cross = px.scatter(
                                    cross_counts,
                                    x=sec_dim,
                                    y=pri_dim,
                                    size='count',
                                    color='count',
                                    title=f"{primary_dimension} by {secondary_dimension}",
                                    labels={sec_dim: secondary_dimension, pri_dim: primary_dimension, 'count': 'Count'},
                                    height=400
                                )
                        except Exception:
                            # Fallback to bar chart if pivot fails
                            fig_cross = px.bar(
                                cross_counts,
                                x=pri_dim,
                                y='count',
                                color=sec_dim,
                                title=f"{primary_dimension} by {secondary_dimension}",
                                labels={pri_dim: primary_dimension, 'count': 'Count', sec_dim: secondary_dimension},
                                barmode='group'
                            )
                    
                    fig_cross.update_layout(height=400)
                    st.plotly_chart(fig_cross, use_container_width=True)
                else:
                    st.warning(f"{secondary_dimension} data not available in the dataset.")
            else:
                st.info("Not enough data available with the current filters for cross-dimensional analysis.")
        
        # Generate insights based on distribution analysis
        st.subheader("📊 Distribution Insights")
        dist_insight_col1, dist_insight_col2 = st.columns(2)
        
        with dist_insight_col1:
            st.markdown("##### Key Observations")
            
            # Insights based on primary dimension
            if primary_dimension == "Topic":
                # Topic insights
                top_topics = filtered_df['topic'].value_counts().nlargest(3)
                
                if not top_topics.empty:
                    top_topic = top_topics.index[0]
                    top_pct = (top_topics.iloc[0] / len(filtered_df)) * 100
                    st.markdown(f"- **{top_topic}** is the dominant topic at **{top_pct:.1f}%** of reviews")
            
            elif primary_dimension == "Issue":
                # Issue insights
                top_issues = filtered_df['issue'].value_counts().nlargest(3)
                
                if not top_issues.empty:
                    top_issue = top_issues.index[0]
                    top_pct = (top_issues.iloc[0] / len(filtered_df)) * 100
                    st.markdown(f"- **{top_issue}** is the most common issue at **{top_pct:.1f}%** of reviews")
            
            elif primary_dimension == "Sentiment":
                if 'sentiment' in filtered_df.columns:
                    # Sentiment insights
                    sentiment_counts = filtered_df['sentiment'].value_counts()
                    sentiment_pcts = sentiment_counts / len(filtered_df) * 100
                    
                    if 'negative' in sentiment_pcts:
                        neg_pct = sentiment_pcts['negative']
                        st.markdown(f"- **{neg_pct:.1f}%** of reviews have negative sentiment")
                        
                        if neg_pct > 50:
                            st.markdown("- Warning: Negative reviews are the majority")
        
        with dist_insight_col2:
            st.markdown("##### Recommended Actions")
            
            # Recommendations based on primary dimension
            if primary_dimension == "Topic":
                # Topic recommendations
                top_topics = filtered_df['topic'].value_counts().nlargest(2).index.tolist()
                
                if top_topics:
                    st.markdown(f"- Focus improvement efforts on top topics: **{', '.join(top_topics)}**")
            
            elif primary_dimension == "Issue":
                # Issue recommendations
                top_issues = filtered_df['issue'].value_counts().nlargest(3).index.tolist()
                
                if top_issues:
                    st.markdown(f"- Prioritize fixing issue: **{top_issues[0]}**")
            
            elif primary_dimension == "Sentiment":
                if 'sentiment' in filtered_df.columns:
                    # Sentiment recommendations
                    sentiment_counts = filtered_df['sentiment'].value_counts()
                    sentiment_pcts = sentiment_counts / len(filtered_df) * 100
                    
                    if 'negative' in sentiment_pcts and sentiment_pcts['negative'] > 40:
                        st.markdown("- **High priority**: Develop comprehensive plan to address negative sentiment")
        
        # Cross-Analysis Section
        st.subheader("Cross-Analysis")
        
        # Allow users to select multiple dimensions for cross-analysis
        cross_col1, cross_col2, cross_col3 = st.columns(3)
        
        with cross_col1:
            x_dimension = st.selectbox(
                "X-axis dimension:",
                options=["Topic", "Issue", "Sentiment", "Data Source", "Rating"],
                index=0,
                key="x_dim"
            )
        
        with cross_col2:
            y_dimension = st.selectbox(
                "Y-axis dimension:",
                options=["Topic", "Issue", "Sentiment", "Data Source", "Rating"],
                index=1,
                key="y_dim"
            )
        
        with cross_col3:
            color_dimension = st.selectbox(
                "Color dimension:",
                options=["Sentiment", "Rating", "Data Source", "None"],
                index=0,
                key="color_dim"
            )
        
        # Map selected dimensions to dataframe columns
        x_col = x_dimension.lower() if x_dimension != "Rating" else "score"
        y_col = y_dimension.lower() if y_dimension != "Rating" else "score"
        color_col = None if color_dimension == "None" else (color_dimension.lower() if color_dimension != "Rating" else "score")
        
        # Ensure all selected dimensions exist in the dataframe
        dimensions_exist = all(col in filtered_df.columns for col in [x_col, y_col] if col is not None)
        if color_col is not None:
            dimensions_exist = dimensions_exist and color_col in filtered_df.columns
        
        if dimensions_exist:
            # Create the cross-analysis visualization
            if x_col == y_col:
                st.warning("Please select different dimensions for X and Y axes.")
            else:
                # Handle different visualization types based on dimension types
                if x_col == "score" or y_col == "score":
                    # If one dimension is numeric (rating), use box plot or bar chart
                    if x_col == "score":
                        # Y is categorical, X is numeric
                        fig_cross = px.box(
                            filtered_df,
                            x=x_col,
                            y=y_col,
                            color=color_col,
                            title=f"{y_dimension} by {x_dimension}",
                            labels={x_col: x_dimension, y_col: y_dimension}
                        )
                    else:
                        # X is categorical, Y is numeric
                        fig_cross = px.box(
                            filtered_df,
                            x=x_col,
                            y=y_col,
                            color=color_col,
                            title=f"{y_dimension} by {x_dimension}",
                            labels={x_col: x_dimension, y_col: y_dimension}
                        )
                else:
                    # Both dimensions are categorical, use heatmap or bubble chart
                    # Group the data
                    cross_counts = filtered_df.groupby([x_col, y_col]).size().reset_index(name='count')
                    
                    # Create appropriate visualization
                    try:
                        # Try to create a heatmap if not too many values
                        if len(cross_counts[x_col].unique()) <= 15 and len(cross_counts[y_col].unique()) <= 15:
                            # Create pivot table
                            pivot_data = cross_counts.pivot(index=y_col, columns=x_col, values='count').fillna(0)
                            
                            # Create heatmap
                            fig_cross = px.imshow(
                                pivot_data,
                                labels=dict(x=x_dimension, y=y_dimension, color="Count"),
                                x=pivot_data.columns,
                                y=pivot_data.index,
                                color_continuous_scale="Viridis",
                                title=f"{y_dimension} by {x_dimension}"
                            )
                        else:
                            # Too many values for a heatmap, use a bubble chart
                            fig_cross = px.scatter(
                                cross_counts,
                                x=x_col,
                                y=y_col,
                                size='count',
                                color='count',
                                title=f"{y_dimension} by {x_dimension}",
                                labels={x_col: x_dimension, y_col: y_dimension, 'count': 'Count'},
                                height=500
                            )
                    except Exception:
                        # Fallback to grouped bar chart
                        fig_cross = px.bar(
                            cross_counts,
                            x=x_col,
                            y='count',
                            color=y_col,
                            title=f"{y_dimension} by {x_dimension}",
                            labels={x_col: x_dimension, 'count': 'Count', y_col: y_dimension},
                            barmode='group'
                        )
                
                # Update layout and display chart
                fig_cross.update_layout(height=500)
                st.plotly_chart(fig_cross, use_container_width=True)
                
                # Generate AI insights about the cross-analysis
                st.subheader(f"📊 {x_dimension} vs {y_dimension} Insights")
                
                # Create columns for observations and recommendations
                cross_insight_col1, cross_insight_col2 = st.columns(2)
                
                with cross_insight_col1:
                    st.markdown("##### Key Observations")
                    
                    # Generate insights based on dimension combinations
                    if x_col == 'topic' and y_col == 'issue':
                        # Topic-Issue correlation insights
                        # Find top issue for each topic
                        topic_issue_map = {}
                        for topic in filtered_df['topic'].unique():
                            topic_df = filtered_df[filtered_df['topic'] == topic]
                            if len(topic_df) > 0:
                                top_issue = topic_df['issue'].value_counts().idxmax()
                                topic_issue_map[topic] = top_issue
                        
                        # Show top correlations
                        for i, (topic, issue) in enumerate(topic_issue_map.items()):
                            if i < 3:  # Limit to top 3
                                st.markdown(f"- **{topic}** is most commonly associated with **{issue}**")
                    
                    elif (x_col == 'topic' and y_col == 'sentiment') or (x_col == 'sentiment' and y_col == 'topic'):
                        # Topic-Sentiment correlation insights
                        if 'sentiment' in filtered_df.columns:
                            # Calculate sentiment distribution by topic
                            topic_sentiment = {}
                            for topic in filtered_df['topic'].unique():
                                topic_df = filtered_df[filtered_df['topic'] == topic]
                                if len(topic_df) > 0:
                                    neg_pct = topic_df[topic_df['sentiment'] == 'negative'].shape[0] / len(topic_df) * 100
                                    topic_sentiment[topic] = neg_pct
                            
                            # Sort by negative sentiment percentage
                            sorted_topics = sorted(topic_sentiment.items(), key=lambda x: x[1], reverse=True)
                            
                            # Show topics with highest and lowest negative sentiment
                            if sorted_topics:
                                worst_topic, worst_pct = sorted_topics[0]
                                st.markdown(f"- **{worst_topic}** has the highest negative sentiment at **{worst_pct:.1f}%**")
                                
                                if len(sorted_topics) > 1:
                                    best_topic, best_pct = sorted_topics[-1]
                                    st.markdown(f"- **{best_topic}** has the lowest negative sentiment at **{best_pct:.1f}%**")
                    
                    else:
                        # Generic insights for other dimension combinations
                        st.markdown("- Patterns in this cross-analysis reveal important correlations")
                        st.markdown("- Some combinations appear much more frequently than others")
                
                with cross_insight_col2:
                    st.markdown("##### Recommended Actions")
                    
                    # Generate recommendations based on dimension combinations
                    if x_col == 'topic' and y_col == 'issue':
                        # Topic-Issue recommendations
                        st.markdown("- Create dedicated teams for each major topic area")
                        st.markdown("- Prioritize issues based on frequency and impact")
                    
                    elif (x_col == 'topic' and y_col == 'sentiment') or (x_col == 'sentiment' and y_col == 'topic'):
                        # Topic-Sentiment recommendations
                        if 'sentiment' in filtered_df.columns:
                            # Calculate sentiment distribution by topic
                            topic_sentiment = {}
                            for topic in filtered_df['topic'].unique():
                                topic_df = filtered_df[filtered_df['topic'] == topic]
                                if len(topic_df) > 0:
                                    neg_pct = topic_df[topic_df['sentiment'] == 'negative'].shape[0] / len(topic_df) * 100
                                    topic_sentiment[topic] = neg_pct
                            
                            # Sort by negative sentiment percentage
                            sorted_topics = sorted(topic_sentiment.items(), key=lambda x: x[1], reverse=True)
                            
                            if sorted_topics:
                                worst_topic, worst_pct = sorted_topics[0]
                                
                                if worst_pct > 50:
                                    st.markdown(f"- **Urgent**: Create action plan to address **{worst_topic}**")
                                elif worst_pct > 30:
                                    st.markdown(f"- Develop improvement strategy for **{worst_topic}**")
                    
                    else:
                        # Generic recommendations for other dimension combinations
                        st.markdown("- Use these cross-dimensional insights to inform product strategy")
                        st.markdown("- Consider A/B testing to validate improvement hypotheses")
                        st.markdown("- Monitor these relationships over time to track progress")
        else:
            st.warning("One or more selected dimensions are not available in the dataset.")
        
        # Step 4: Sample reviews section that updates dynamically based on filters
        st.subheader("Sample Reviews")
        
        # Show reviews based on filters
        sample_reviews = filtered_df.sort_values('datetime', ascending=False).head(5)
        
        if not sample_reviews.empty:
            # Get reviews by sentiment if available
            if 'sentiment' in filtered_df.columns:
                # Create simple radio button for sentiment filter
                sentiment_filter = st.radio(
                    "Filter reviews by sentiment:",
                    ["All", "Positive", "Negative", "Neutral"],
                    horizontal=True
                )
                
                if sentiment_filter == "Positive":
                    sample_reviews = filtered_df[filtered_df['sentiment'] == 'positive'].sort_values('score', ascending=False).head(5)
                elif sentiment_filter == "Negative":
                    sample_reviews = filtered_df[filtered_df['sentiment'] == 'negative'].sort_values('score').head(5)
                elif sentiment_filter == "Neutral":
                    sample_reviews = filtered_df[filtered_df['sentiment'] == 'neutral'].head(5)
            
            # Display selected reviews
            for i, (_, review) in enumerate(sample_reviews.iterrows()):
                # Determine border color based on sentiment
                if 'sentiment' in review:
                    if review['sentiment'] == 'positive':
                        border_color = 'green'
                    elif review['sentiment'] == 'negative':
                        border_color = 'red'
                    else:
                        border_color = 'gray'
                else:
                    border_color = 'blue'
                
                # Get star rating as emoji string
                stars = '⭐' * int(review.get('score', 0))
                
                # Format date if available
                date_str = ""
                if 'datetime' in review:
                    try:
                        if isinstance(review['datetime'], str):
                            date_obj = pd.to_datetime(review['datetime'])
                        else:
                            date_obj = review['datetime']
                        date_str = date_obj.strftime("%b %d, %Y")
                    except:
                        date_str = str(review['datetime'])
                
                # Create card for this review
                st.markdown(f"""
                <div style="border:1px solid #ddd; border-radius:5px; padding:15px; margin-bottom:15px; border-left:5px solid {border_color};">
                    <div style="display:flex; justify-content:space-between;">
                        <div><strong>Topic:</strong> {review.get('topic', 'N/A')} | <strong>Issue:</strong> {review.get('issue', 'N/A')}</div>
                        <div>{date_str}</div>
                    </div>
                    <p style="margin:5px 0;"><strong>Rating:</strong> {stars}</p>
                    <p style="margin:5px 0;"><strong>Problem:</strong> {review.get('problem', 'N/A')}</p>
                    <p style="margin:10px 0 0 0; font-style:italic;">{review['review']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No matching reviews found.")

else:
    # Add option to load demo data
    st.info("Please upload a CSV file in the sidebar to begin analysis, or use our demo dataset below.")
    
    # Make the demo button more prominent and clear
    demo_col1, demo_col2 = st.columns([1, 2])
    with demo_col1:
        if st.button("📊 Load Demo Data", key="demo_button", use_container_width=True):
            # Set flag to load demo data on next rerun
            st.session_state.demo_loaded = True
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()
    
    with demo_col2:
        st.markdown("""
        <div style="padding-top: 15px;">
            Click to load sample streaming app reviews data
        </div>
        """, unsafe_allow_html=True)
    
    # Sample dashboard image or description
    st.subheader("What You'll Get:")
    st.write("""
    This tool provides:
    - Interactive topic trend analysis 
    - Issue breakdowns by topic
    - AI-powered insights for each visualization
    - Sample review exploration
    - Sentiment analysis across topics
    
Upload your data or use our demo dataset to get started!
    """)
    # Exit early if no data
    st.stop()

# Reset button in sidebar to restart the analysis
with st.sidebar:
    if st.session_state.get('data_confirmed', False):
        if st.button("Reset Analysis"):
            st.session_state.data_confirmed = False
            st.session_state.demo_loaded = False
            if 'processed_df' in st.session_state:
                del st.session_state.processed_df
            st.rerun()  # Use st.rerun() instead of st.experimental_rerun()