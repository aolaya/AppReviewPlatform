import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import numpy as np

# Set page configuration
st.set_page_config(
    page_title="App Review Analysis Tool",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #0D47A1;
        margin-top: 2rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E3F2FD;
    }
    .section-header {
        font-size: 1.5rem;
        color: #1565C0;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }
    .insight-box {
        background-color: #E3F2FD;
        border-left: 5px solid #1E88E5;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .action-box {
        background-color: #FFEBEE;
        border-left: 5px solid #F44336;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .success-box {
        background-color: #E8F5E9;
        border-left: 5px solid #4CAF50;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #E0F7FA;
        border-left: 5px solid #00BCD4;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .review-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
    }
    .emoji-bullet {
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar for file upload and data configuration
with st.sidebar:
    st.markdown("## 🧰 Tool Controls")
    st.markdown("### 📤 Upload Data")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Display information about required columns
    with st.expander("ℹ️ Required Column Information"):
        st.markdown("""
        For the best analysis, your CSV should include these columns:
        
        - **reviewId**: Unique identifier for each review
        - **review**: The full text of the review
        - **score**: Numerical rating (1-5 stars)
        - **datetime**: When the review was submitted
        - **topic**: Main category (e.g., performance, usability)
        - **problem**: Specific problem description
        - **sentiment**: Positive, negative, or neutral
        - **issue**: Specific issue type
        - **company**: App or company name
        - **data_source**: Where the review came from
        
        Missing some columns? The tool will still work, but with limited analysis.
        """)
    
    st.markdown("---")
    st.markdown("### 📊 Made with Streamlit")
    st.markdown("A tool for streaming app stakeholders to discover insights in customer feedback.")

# Main content area
st.markdown("<h1 class='main-header'>🔍 App Review Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div class='info-box'>
    <p>This tool helps you uncover patterns in app reviews, identify emerging issues, and understand what users are saying about your streaming app. Upload your data or try the demo to get started!</p>
</div>
""", unsafe_allow_html=True)

# Initialize session state for data confirmation
if 'data_confirmed' not in st.session_state:
    st.session_state.data_confirmed = False

if uploaded_file is not None or st.session_state.get('demo_loaded', False):
    # Get data either from uploaded file or demo
    if uploaded_file is not None:
        # Read the data from uploaded file
        try:
            df = pd.read_csv(uploaded_file)
            data_source = "uploaded file"
            st.success(f"✅ Successfully loaded {len(df)} reviews from your file!")
        except Exception as e:
            st.error(f"❌ Error loading file: {e}")
            st.stop()
    else:
        # Create demo data
        demo_data = {
            'reviewId': ['001', '002', '003', '004', '005', '006', '007', '008', '009', '010', '011', '012'],
            'review': [
                "I know this might be a challenge but could you guys just allow downloads to happen even if I switch away from the app.",
                "I have trouble getting episodes to load on my tvs or phones. sometimes it freezes on my tv.",
                "The app keeps crashing whenever I try to watch a show for more than 30 minutes.",
                "Great content but the recent price increase is making me consider cancelling my subscription.",
                "The new UI is confusing and makes it harder to find what I'm looking for.",
                "Love the original content, but wish there were more classic movies available.",
                "The app asked me to verify my account multiple times in one week.",
                "Had an issue with billing and customer service was unhelpful.",
                "The streaming quality is awesome, best I've seen on any platform!",
                "App works perfectly on my phone but crashes on my tablet.",
                "The recommendations are spot on! I've discovered so many new shows.",
                "Cannot skip intros easily like on other platforms."
            ],
            'score': [2, 1, 1, 3, 2, 4, 2, 1, 5, 2, 5, 3],
            'datetime': [
                '2025-01-15', '2025-01-20', '2025-01-25', 
                '2025-02-05', '2025-02-10', '2025-02-15', 
                '2025-02-20', '2025-02-25', '2025-03-01',
                '2025-03-05', '2025-03-10', '2025-03-15'
            ],
            'topic': [
                'functionality', 'performance', 'performance',
                'value', 'usability', 'content',
                'security', 'customer service', 'performance',
                'performance', 'content', 'usability'
            ],
            'problem': [
                'downloads stop when switching apps', 'loading issues', 'app crashes',
                'price increase', 'confusing UI', 'limited content library',
                'excessive verification', 'poor customer service', 'streaming quality',
                'app stability on specific devices', 'content discovery', 'user interface'
            ],
            'sentiment': [
                'negative', 'negative', 'negative',
                'negative', 'negative', 'mixed',
                'negative', 'negative', 'positive',
                'negative', 'positive', 'neutral'
            ],
            'issue': [
                'background downloads', 'loading issues', 'app stability',
                'pricing concerns', 'navigation difficulty', 'content variety',
                'account security', 'support quality', 'streaming quality',
                'device compatibility', 'content discovery', 'feature request'
            ],
            'company': ['StreamFlix' for _ in range(12)],
            'data_source': ['App Store', 'App Store', 'Google Play', 
                           'App Store', 'Google Play', 'App Store',
                           'Google Play', 'App Store', 'Google Play',
                           'App Store', 'Google Play', 'App Store']
        }
        
        # Create DataFrame
        df = pd.DataFrame(demo_data)
        data_source = "demo dataset"
        st.success("✅ Demo data loaded successfully!")
    
    # Preview the data (if not confirmed yet)
    if not st.session_state.data_confirmed:
        st.markdown(f"<h2 class='sub-header'>📋 Data Preview ({data_source})</h2>", unsafe_allow_html=True)
        
        # Show data preview first
        with st.expander("👁️ View data sample", expanded=True):
            st.dataframe(df.head(), use_container_width=True)
        
        # Add a summary section with key metrics in a 2x2 grid
        st.markdown("<h3 class='section-header'>📊 Data Summary</h3>", unsafe_allow_html=True)
        
        # Create a row of metrics
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            # Number of unique reviews
            num_reviews = len(df['reviewId'].unique()) if 'reviewId' in df.columns else len(df)
            st.metric(label="📝 Total Reviews", value=f"{num_reviews:,}")
        
        with metric_cols[1]:    
            # Average rating
            if 'score' in df.columns:
                avg_rating = df['score'].mean()
                rating_emoji = "⭐" if avg_rating < 2 else "⭐⭐" if avg_rating < 3 else "⭐⭐⭐" if avg_rating < 4 else "⭐⭐⭐⭐" if avg_rating < 4.5 else "⭐⭐⭐⭐⭐"
                st.metric(label=f"{rating_emoji} Average Rating", value=f"{avg_rating:.2f}/5")
        
        with metric_cols[2]:
            # Timeframe
            if 'datetime' in df.columns:
                try:
                    df['datetime'] = pd.to_datetime(df['datetime'])
                    min_date = df['datetime'].min()
                    max_date = df['datetime'].max()
                    date_range = f"{min_date.strftime('%b %Y')} - {max_date.strftime('%b %Y')}"
                    st.metric(label="📅 Time Period", value=date_range)
                except Exception as e:
                    st.error(f"Error processing datetime: {e}")
        
        with metric_cols[3]:
            # Number of unique apps/companies
            if 'company' in df.columns:
                num_companies = df['company'].nunique()
                st.metric(label="🏢 Apps Analyzed", value=num_companies)
        
        # Add a second row of metrics if sentiment is available
        if 'sentiment' in df.columns:
            sentiment_cols = st.columns(3)
            
            with sentiment_cols[0]:
                pos_count = df[df['sentiment'] == 'positive'].shape[0]
                pos_pct = (pos_count / len(df)) * 100
                st.metric(label="😃 Positive Reviews", value=f"{pos_pct:.1f}%", delta=f"{pos_count} reviews")
            
            with sentiment_cols[1]:
                neg_count = df[df['sentiment'] == 'negative'].shape[0]
                neg_pct = (neg_count / len(df)) * 100
                st.metric(label="😞 Negative Reviews", value=f"{neg_pct:.1f}%", delta=f"{neg_count} reviews")
            
            with sentiment_cols[2]:
                neu_count = df[df['sentiment'] == 'neutral'].shape[0]
                neu_pct = (neu_count / len(df)) * 100
                st.metric(label="😐 Neutral Reviews", value=f"{neu_pct:.1f}%", delta=f"{neu_count} reviews")
        
        # Data quality check
        st.markdown("<h3 class='section-header'>🔍 Data Quality Check</h3>", unsafe_allow_html=True)
        
        # Check if data contains required columns
        required_columns = ['topic', 'issue', 'datetime', 'company']
        available_columns = set(df.columns)
        missing_columns = [col for col in required_columns if col not in available_columns]
        
        quality_cols = st.columns(2)
        
        with quality_cols[0]:
            st.markdown("#### Required Columns")
            
            if missing_columns:
                st.markdown(f"""
                <div class='action-box'>
                    <p>⚠️ <strong>Missing columns:</strong> {', '.join(missing_columns)}</p>
                    <p>Some analyses may be limited.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='success-box'>
                    <p>✅ All required columns are present!</p>
                </div>
                """, unsafe_allow_html=True)
        
        with quality_cols[1]:
            st.markdown("#### Data Preparation")
            
            # Convert datetime to datetime format if it's not already
            datetime_ok = False
            if 'datetime' in df.columns:
                try:
                    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
                        df['datetime'] = pd.to_datetime(df['datetime'])
                    datetime_ok = True
                    # Extract month and year for trend analysis
                    df['month_year'] = df['datetime'].dt.strftime('%Y-%m')
                except Exception as e:
                    st.markdown(f"""
                    <div class='action-box'>
                        <p>⚠️ <strong>Error converting datetime:</strong> {e}</p>
                        <p>Time-based analysis may be limited.</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            if datetime_ok:
                st.markdown("""
                <div class='success-box'>
                    <p>✅ Date column processed successfully!</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Data insights preview
        st.markdown("<h3 class='section-header'>🔮 Quick Insights Preview</h3>", unsafe_allow_html=True)
        
        preview_cols = st.columns(2)
        
        with preview_cols[0]:
            # Get top topics
            topic_counts = df['topic'].value_counts()
            top_topic = topic_counts.index[0]
            top_topic_pct = (topic_counts.iloc[0] / len(df)) * 100
            
            st.markdown(f"""
            <div class='insight-box'>
                <p>🏆 <strong>Top topic:</strong> "{top_topic}" appears in {top_topic_pct:.1f}% of reviews</p>
                <p>Common issues in this topic:</p>
                <ul>
            """, unsafe_allow_html=True)
            
            # Get top issues for the top topic
            top_topic_issues = df[df['topic'] == top_topic]['issue'].value_counts().head(3)
            for issue, count in top_topic_issues.items():
                issue_pct = (count / topic_counts.iloc[0]) * 100
                st.markdown(f"<li>{issue} ({issue_pct:.1f}%)</li>", unsafe_allow_html=True)
            
            st.markdown("</ul></div>", unsafe_allow_html=True)
        
        with preview_cols[1]:
            if 'sentiment' in df.columns and 'score' in df.columns:
                # Get average ratings by sentiment
                sentiment_ratings = df.groupby('sentiment')['score'].mean()
                
                st.markdown(f"""
                <div class='insight-box'>
                    <p>🌟 <strong>Rating insights:</strong></p>
                    <ul>
                """, unsafe_allow_html=True)
                
                for sentiment, avg_rating in sentiment_ratings.items():
                    stars = "⭐" * round(avg_rating)
                    st.markdown(f"<li>{sentiment.capitalize()} reviews average {avg_rating:.1f}/5 {stars}</li>", unsafe_allow_html=True)
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='info-box'>
                    <p>ℹ️ More insights will be available after data confirmation.</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Store the processed dataframe in session state
        st.session_state.processed_df = df
        
        # Simple confirm button
        st.markdown("<h3 class='section-header'>✅ Confirm Data</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-box'>
            <p>Click 'Confirm' to proceed with the analysis. This will unlock interactive visualizations, AI insights, and detailed review analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("✅ Confirm and Analyze Data", use_container_width=True):
            st.session_state.data_confirmed = True
            st.balloons()  # Add a fun touch when confirming
            st.rerun()
    
    # If data is confirmed, show analysis while keeping previous steps visible
    if st.session_state.data_confirmed:
        # Use the processed dataframe from session state
        if 'processed_df' in st.session_state:
            df = st.session_state.processed_df
            # Keep the previous steps visible in a continuous flow
            st.markdown("<h2 class='sub-header'>🔄 Analysis Workflow</h2>", unsafe_allow_html=True)
        
        # Data source indicator
        if uploaded_file is not None:
            st.markdown(f"""
            <div class='success-box'>
                <p>📤 <strong>Data Source:</strong> Using your uploaded file with {len(df)} reviews</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class='success-box'>
                <p>🧪 <strong>Data Source:</strong> Using demo data with {len(df)} sample reviews</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create comprehensive filter section to let stakeholders slice the data
        st.markdown("<h2 class='sub-header'>🔍 Interactive Data Explorer</h2>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class='info-box'>
            <p>💡 <strong>Pro Tip:</strong> Use these filters to slice and dice your data. The visualizations below will update automatically to show insights on your selected subset.</p>
        </div>
        """, unsafe_allow_html=True)
        
        filter_container = st.container()
        with filter_container:
            filter_cols = st.columns([2, 2, 1])
            
            # First column of filters
            with filter_cols[0]:
                st.markdown("#### 📅 Time & Categories")
                
                # Date range filter
                if 'datetime' in df.columns:
                    min_date = pd.to_datetime(df['datetime']).min().date()
                    max_date = pd.to_datetime(df['datetime']).max().date()
                    
                    selected_date_range = st.date_input(
                        "📆 Date Range:",
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
                selected_topics = st.multiselect("🏷️ Topics:", topics, default=[])
                
                # Issue multiselect - dynamically updates based on selected topics
                if 'issue' in df.columns:
                    if selected_topics:
                        # Fix for sorting mixed types
                        available_issues = [str(x) for x in df[df['topic'].isin(selected_topics)]['issue'].unique() if not pd.isna(x)]
                        available_issues = sorted(available_issues)
                    else:
                        # Fix for sorting mixed types
                        available_issues = [str(x) for x in df['issue'].unique() if not pd.isna(x)]
                        available_issues = sorted(available_issues)
                        
                    selected_issues = st.multiselect("🔧 Issues:", available_issues, default=[])
            
            # Second column of filters
            with filter_cols[1]:
                st.markdown("#### 🌟 Ratings & Sources")
                
                # Rating range slider
                if 'score' in df.columns:
                    min_rating, max_rating = int(df['score'].min()), int(df['score'].max())
                    selected_rating = st.slider("⭐ Rating Range:", min_rating, max_rating, (min_rating, max_rating))
                
                # Sentiment multiselect
                if 'sentiment' in df.columns:
                    sentiment_map = {
                        'positive': '😃 Positive',
                        'negative': '😞 Negative',
                        'neutral': '😐 Neutral',
                        'mixed': '😕 Mixed'
                    }
                    
                    sentiments = sorted(df['sentiment'].unique())
                    sentiment_options = [sentiment_map.get(s, s) for s in sentiments]
                    selected_sentiment_options = st.multiselect("🎭 Sentiment:", sentiment_options, default=[])
                    
                    # Convert back to actual values
                    reverse_map = {v: k for k, v in sentiment_map.items()}
                    selected_sentiments = [reverse_map.get(s, s) for s in selected_sentiment_options]
                
                # Data source multiselect
                if 'data_source' in df.columns:
                    data_sources = sorted(df['data_source'].unique())
                    selected_data_sources = st.multiselect("📱 Data Source:", data_sources, default=[])
            
            # Third column with search
            with filter_cols[2]:
                st.markdown("#### 🔎 Search")
                
                # Problem search - allows free text search in the problem field
                if 'problem' in df.columns:
                    problem_search = st.text_input("🔍 Search Problems:", "")
                
                # Review text search
                if 'review' in df.columns:
                    review_search = st.text_input("🔍 Search Reviews:", "")
                
                # Reset filters button
                if st.button("🔄 Reset Filters", use_container_width=True):
                    st.experimental_rerun()
        
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
        if 'issue' in df.columns and selected_issues:
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
        
        # Apply review search
        if 'review' in df.columns and review_search:
            filtered_df = filtered_df[filtered_df['review'].str.contains(review_search, case=False, na=False)]
        
        # Show filter summary
        if len(filtered_df) == len(df):
            st.markdown(f"""
            <div class='info-box'>
                <p>🔍 Showing all <strong>{len(filtered_df):,}</strong> reviews</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            filter_pct = (len(filtered_df) / len(df)) * 100
            st.markdown(f"""
            <div class='info-box'>
                <p>🔍 Showing <strong>{len(filtered_df):,}</strong> of {len(df):,} reviews ({filter_pct:.1f}%)</p>
            </div>
            """, unsafe_allow_html=True)
        
        # If no data matches filters, show warning and stop
        if len(filtered_df) == 0:
            st.warning("⚠️ No data matches your selected filters. Please adjust your criteria.")
            st.stop()
        
        # Show key metrics for filtered data
        st.markdown("<h2 class='sub-header'>📊 Key Metrics Dashboard</h2>", unsafe_allow_html=True)
        st.markdown("""
        <div class='info-box'>
            <p>These metrics reflect your current filter selection. Changes in values compared to the overall dataset are shown with ▲ and ▼ indicators.</p>
        </div>
        """, unsafe_allow_html=True)
        
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            # Average rating
            if 'score' in filtered_df.columns:
                avg_score = filtered_df['score'].mean()
                overall_avg = df['score'].mean()
                delta = avg_score - overall_avg
                delta_str = f"{delta:+.1f} vs overall"
                
                rating_emoji = "⭐" if avg_score < 2 else "⭐⭐" if avg_score < 3 else "⭐⭐⭐" if avg_score < 4 else "⭐⭐⭐⭐" if avg_score < 4.5 else "⭐⭐⭐⭐⭐"
                
                st.metric(
                    label=f"{rating_emoji} Average Rating", 
                    value=f"{avg_score:.1f}/5",
                    delta=delta_str,
                    delta_color="normal"
                )
        
        with metric_cols[1]:
            # Negative sentiment percentage
            if 'sentiment' in filtered_df.columns:
                neg_sentiment = filtered_df[filtered_df['sentiment'] == 'negative'].shape[0] / filtered_df.shape[0] * 100
                overall_neg = df[df['sentiment'] == 'negative'].shape[0] / df.shape[0] * 100
                delta = neg_sentiment - overall_neg
                
                st.metric(
                    label="😞 Negative Sentiment", 
                    value=f"{neg_sentiment:.1f}%",
                    delta=f"{delta:+.1f}% vs overall",
                    delta_color="inverse"
                )
            else:
                # Fallback if no sentiment data
                review_count = len(filtered_df)
                st.metric(label="📝 Review Count", value=f"{review_count:,}")
        
        with metric_cols[2]:
            # Top topic
            top_topic = filtered_df['topic'].value_counts().idxmax() if len(filtered_df['topic'].unique()) > 0 else "N/A"
            top_topic_pct = filtered_df['topic'].value_counts(normalize=True).max() * 100 if len(filtered_df['topic'].unique()) > 0 else 0
            
            st.metric(
                label="🔝 Top Topic", 
                value=f"{top_topic}",
                delta=f"{top_topic_pct:.1f}% of selected"
            )
        
        with metric_cols[3]:
            # Top issue
            if 'issue' in filtered_df.columns:
                top_issue = filtered_df['issue'].value_counts().idxmax() if len(filtered_df['issue'].unique()) > 0 else "N/A"
                top_issue_pct = filtered_df['issue'].value_counts(normalize=True).max() * 100 if len(filtered_df['issue'].unique()) > 0 else 0
                
                st.metric(
                    label="⚠️ Top Issue", 
                    value=f"{top_issue}",
                    delta=f"{top_issue_pct:.1f}% of selected"
                )
            else:
                # Fallback if no issue data
                if 'data_source' in filtered_df.columns:
                    top_source = filtered_df['data_source'].value_counts().idxmax()
                    top_source_pct = filtered_df['data_source'].value_counts(normalize=True).max() * 100
                    
                    st.metric(
                        label="📱 Primary Source", 
                        value=f"{top_source}",
                        delta=f"{top_source_pct:.1f}% of selected"
                    )

        # TREND ANALYSIS SECTION - Unified workflow without tabs
        st.markdown("<h2