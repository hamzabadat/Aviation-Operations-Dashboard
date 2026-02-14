# ============================================================================
# AVIATION OPERATIONS DASHBOARD - INTERACTIVE STREAMLIT APP
# ============================================================================
# A professional flight delay analysis dashboard with swim lane timeline view
# Perfect portfolio project for operations, logistics, and analyst roles
# ============================================================================

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Aviation Operations Dashboard",
    page_icon="✈️",
    layout="wide",  # Use full width of browser
    initial_sidebar_state="expanded"
)

# ============================================================================
# AIRLINE BRAND COLORS (Authentic airline branding)
# ============================================================================
AIRLINE_COLORS = {
    'UA': '#0078D2',    # United - Blue
    'DL': '#C8102E',    # Delta - Red
    'AA': '#A2AAAD',    # American - Silver/Grey
    'WN': '#304CB2',    # Southwest - Blue
    'NK': '#FFE900',    # Spirit - Yellow
    'F9': '#00A859',    # Frontier - Green
    'B6': '#0047BB',    # JetBlue - Dark Blue
    'AS': '#01426A',    # Alaska - Teal Blue
    'US': '#8B0000',    # US Airways - Dark Red
    'OO': '#FF6B35',    # Skywest - Orange
    'EV': '#1E90FF',    # Atlantic Southeast - Light Blue
    'HA': '#7B1FA2',    # Hawaiian - Purple
    'MQ': '#4A4A4A',    # American Eagle - Dark Grey
    'VX': '#FF3366',    # Virgin America - Pink/Red
}

# Default color for airlines not in our list
DEFAULT_COLOR = '#808080'  # Grey

# Airline full names
AIRLINE_NAMES = {
    'UA': 'United Airlines',
    'AA': 'American Airlines',
    'DL': 'Delta Air Lines',
    'WN': 'Southwest Airlines',
    'B6': 'JetBlue Airways',
    'AS': 'Alaska Airlines',
    'NK': 'Spirit Airlines',
    'F9': 'Frontier Airlines',
    'US': 'US Airways',
    'OO': 'SkyWest Airlines',
    'EV': 'Atlantic Southeast',
    'HA': 'Hawaiian Airlines',
    'MQ': 'American Eagle',
    'VX': 'Virgin America'
}

# ============================================================================
# DATA LOADING FUNCTION (with caching for speed)
# ============================================================================
@st.cache_data  # This caches the data so it doesn't reload every time
def load_data():
    """
    Load and prepare the flight data
    Always loads the complete dataset for full analysis
    """
    # Load the data
    df = pd.read_csv('flights.csv')
    
    # Create proper date column
    df['DATE'] = pd.to_datetime(df[['YEAR', 'MONTH', 'DAY']])
    
    # Fill missing delay values with 0
    df['DEPARTURE_DELAY'] = df['DEPARTURE_DELAY'].fillna(0)
    df['ARRIVAL_DELAY'] = df['ARRIVAL_DELAY'].fillna(0)
    
    # Create hour column from scheduled departure (e.g., 1435 -> 14)
    df['DEPARTURE_HOUR'] = (df['SCHEDULED_DEPARTURE'] // 100).clip(0, 23)
    df['ARRIVAL_HOUR'] = (df['SCHEDULED_ARRIVAL'] // 100).clip(0, 23)
    
    # Convert times to decimal hours for plotting (e.g., 1430 -> 14.5)
    df['DEPARTURE_HOUR_DECIMAL'] = (df['SCHEDULED_DEPARTURE'] // 100) + ((df['SCHEDULED_DEPARTURE'] % 100) / 60)
    df['ARRIVAL_HOUR_DECIMAL'] = (df['SCHEDULED_ARRIVAL'] // 100) + ((df['SCHEDULED_ARRIVAL'] % 100) / 60)
    
    # Handle midnight crossings (arrival next day)
    df.loc[df['ARRIVAL_HOUR_DECIMAL'] < df['DEPARTURE_HOUR_DECIMAL'], 'ARRIVAL_HOUR_DECIMAL'] += 24
    
    # Fill delay cause columns
    delay_cols = ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY', 
                  'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
    for col in delay_cols:
        df[col] = df[col].fillna(0)
    
    return df

# ============================================================================
# SIDEBAR - DATA LOADING
# ============================================================================
st.sidebar.title("⚙️ Dashboard Settings")
st.sidebar.markdown("---")

# Always load full dataset
st.sidebar.info("📊 Loading complete dataset for full analysis")

# Load data with a spinner
with st.spinner('Loading flight data... This may take a minute.'):
    df = load_data()

st.sidebar.success(f"✅ Loaded {len(df):,} flights")
st.sidebar.markdown(f"📅 Date Range: {df['DATE'].min().strftime('%b %d, %Y')} - {df['DATE'].max().strftime('%b %d, %Y')}")
st.sidebar.markdown("---")

# ============================================================================
# NAVIGATION - SELECT PAGE
# ============================================================================
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Select Page:",
    ["🛫 Flight Operations Timeline", "📈 Analytics Dashboard", "🔍 Root Cause Analysis"]
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Tip:** This dashboard demonstrates data analysis and visualization skills for aviation operations roles.")

# ============================================================================
# PAGE 1: FLIGHT OPERATIONS TIMELINE (SINGLE AIRPORT VIEW)
# ============================================================================
if page == "🛫 Flight Operations Timeline":
    st.title("✈️ Flight Operations Timeline - Single Airport View")
    st.markdown("**Departure Schedule Visualization**")
    st.markdown("---")
    
    # ==================================================================
    # FILTERS: Airline, Date, and Airport Selection
    # ==================================================================
    st.subheader("🔎 Select View Parameters")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # AIRLINE SELECTOR
        available_airlines = sorted(df['AIRLINE'].unique())
        airline_options = [f"{code} - {AIRLINE_NAMES.get(code, 'Unknown')}" for code in available_airlines]
        selected_airline_display = st.selectbox(
            "Select Airline:",
            options=airline_options,
            index=airline_options.index('UA - United Airlines') if 'UA - United Airlines' in airline_options else 0,
            help="Choose which airline to view"
        )
        selected_airline = selected_airline_display.split(' - ')[0]
    
    with col2:
        # DATE SELECTOR
        min_date = df['DATE'].min().date()
        max_date = df['DATE'].max().date()
        
        # Default to Feb 1, 2015 if available, otherwise first date
        default_date = pd.to_datetime('2015-02-01').date()
        if default_date < min_date or default_date > max_date:
            default_date = min_date
        
        selected_date = st.date_input(
            "Select Date:",
            value=default_date,
            min_value=min_date,
            max_value=max_date,
            help="Choose any date from the dataset"
        )
    
    with col3:
        # AIRPORT SELECTOR
        # First filter by airline and date to get relevant airports
        df_filtered = df[
            (df['DATE'] == pd.to_datetime(selected_date)) & 
            (df['AIRLINE'] == selected_airline) &
            (df['CANCELLED'] == 0)
        ]
        
        available_airports = sorted(df_filtered['ORIGIN_AIRPORT'].unique())
        
        if len(available_airports) > 0:
            selected_airport = st.selectbox(
                "Select Departure Airport:",
                options=available_airports,
                index=0,
                help="View all departing flights from this airport"
            )
        else:
            st.warning("⚠️ No airports found for selected airline/date combination")
            selected_airport = None
    
    st.markdown("---")
    
    # ==================================================================
    # MAIN CHART
    # ==================================================================
    if selected_airport:
        # Filter data: Only DEPARTURES from selected airport, airline, and date
        df_departures = df[
            (df['DATE'] == pd.to_datetime(selected_date)) & 
            (df['AIRLINE'] == selected_airline) &
            (df['ORIGIN_AIRPORT'] == selected_airport) &
            (df['CANCELLED'] == 0)
        ].copy()
        
        # Sort by departure time
        df_departures = df_departures.sort_values('DEPARTURE_HOUR_DECIMAL')
        
        if len(df_departures) > 0:
            # Display summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_flights = len(df_departures)
            avg_delay = df_departures['DEPARTURE_DELAY'].mean()
            ontime_pct = (df_departures['DEPARTURE_DELAY'] <= 0).sum() / total_flights * 100
            max_delay = df_departures['DEPARTURE_DELAY'].max()
            
            col1.metric("Departures", f"{total_flights:,}")
            col2.metric("Average Delay", f"{avg_delay:.1f} min")
            col3.metric("On-Time %", f"{ontime_pct:.1f}%")
            col4.metric("Max Delay", f"{max_delay:.0f} min")
            
            st.markdown("---")
            
            # Create the chart
            fig = go.Figure()
            
            # VERTICAL SPACING PARAMETERS (Adjust these to change appearance)
            BAR_HEIGHT = 1.5  # Height of each flight bar
            SPACE_BETWEEN = 0.5  # Space between bars
            TOTAL_ROW_HEIGHT = BAR_HEIGHT + SPACE_BETWEEN  # 2.0 total per flight
            
            # Add vertical grid lines every 2 hours
            for hour in range(0, 25, 2):
                fig.add_shape(
                    type="line",
                    x0=hour, x1=hour,
                    y0=-0.5, y1=len(df_departures) * TOTAL_ROW_HEIGHT,
                    line=dict(color="rgba(180,180,180,0.4)", width=1),
                    layer='below'
                )
            
            # Add lighter grid lines every 1 hour
            for hour in range(1, 24, 2):
                fig.add_shape(
                    type="line",
                    x0=hour, x1=hour,
                    y0=-0.5, y1=len(df_departures) * TOTAL_ROW_HEIGHT,
                    line=dict(color="rgba(200,200,200,0.2)", width=1, dash="dot"),
                    layer='below'
                )
            
            # Get airline color
            airline_color = AIRLINE_COLORS.get(selected_airline, DEFAULT_COLOR)
            
            # Plot each flight
            for idx, (_, flight) in enumerate(df_departures.iterrows()):
                start_time = flight['DEPARTURE_HOUR_DECIMAL']
                end_time = flight['ARRIVAL_HOUR_DECIMAL']
                
                # Clip to 24-hour window
                if end_time > 24:
                    end_time = 24
                    continues_next_day = True
                else:
                    continues_next_day = False
                
                # Calculate Y position with proper spacing
                y_center = idx * TOTAL_ROW_HEIGHT
                
                # Create hover text
                hover_text = (
                    f"<b>{selected_airline}{flight['FLIGHT_NUMBER']}</b><br>"
                    f"{flight['ORIGIN_AIRPORT']} → {flight['DESTINATION_AIRPORT']}<br>"
                    f"Tail: {flight['TAIL_NUMBER']}<br>"
                    f"Scheduled Dep: {int(flight['SCHEDULED_DEPARTURE']):04d}<br>"
                    f"Scheduled Arr: {int(flight['SCHEDULED_ARRIVAL']):04d}<br>"
                    f"Departure Delay: {flight['DEPARTURE_DELAY']:.0f} min<br>"
                    f"Flight Duration: {flight['AIR_TIME']:.0f} min<br>"
                    f"Distance: {flight['DISTANCE']:.0f} miles"
                )
                
                if continues_next_day:
                    hover_text += "<br><i>(Continues next day)</i>"
                
                # Color based on delay - use airline brand color
                if flight['DEPARTURE_DELAY'] > 15:
                    # Slightly darker for significant delays
                    bar_color = airline_color
                    opacity = 0.7
                else:
                    bar_color = airline_color
                    opacity = 0.85
                
                # Add the flight bar
                fig.add_trace(go.Bar(
                    x=[end_time - start_time],
                    y=[y_center],
                    base=start_time,
                    orientation='h',
                    width=BAR_HEIGHT,  # Set explicit bar height
                    marker=dict(
                        color=bar_color,
                        line=dict(color='#004080', width=1),
                        opacity=opacity
                    ),
                    # CUSTOMIZE THIS TEXT - Add whatever info you want!
                    text=f"{selected_airline}{flight['FLIGHT_NUMBER']} | {flight['TAIL_NUMBER']} | →{flight['DESTINATION_AIRPORT']} | {flight['AIR_TIME']:.0f}min",
                    textposition='inside',  # Text inside the bar
                    textfont=dict(size=9, color='white', family='Arial Black'),
                    hovertext=hover_text,
                    hoverinfo='text',
                    showlegend=False
                ))
            
            # Add current time marker
            current_time = datetime.now()
            current_hour_decimal = current_time.hour + current_time.minute / 60
            
            fig.add_shape(
                type="line",
                x0=current_hour_decimal,
                x1=current_hour_decimal,
                y0=-0.5,
                y1=len(df_departures) * TOTAL_ROW_HEIGHT,
                line=dict(color="#E53935", width=3),
                layer='above'
            )
            
            fig.add_annotation(
                x=current_hour_decimal,
                y=len(df_departures) * TOTAL_ROW_HEIGHT,
                text=f"NOW {current_time.strftime('%H:%M')}",
                showarrow=False,
                yshift=20,
                font=dict(size=12, color="#E53935", family="Arial Black"),
                bgcolor="rgba(229, 57, 53, 0.15)",
                bordercolor="#E53935",
                borderwidth=2,
                borderpad=4
            )
            
            # Update layout
            fig.update_layout(
                title=dict(
                    text=f"<b>{AIRLINE_NAMES.get(selected_airline, selected_airline)} Departures from {selected_airport}</b><br><sub>{pd.to_datetime(selected_date).strftime('%B %d, %Y')}</sub>",
                    font=dict(size=20, color='#003366', family='Arial Black'),
                    x=0.5,
                    xanchor='center'
                ),
                xaxis=dict(
                    title=dict(
                        text="<b>Time of Day (24-Hour Format)</b>",
                        font=dict(size=14, color='#003366', family='Arial Black')
                    ),
                    tickmode='array',
                    tickvals=list(range(0, 25, 2)),
                    ticktext=[f"<b>{h:02d}:00</b>" for h in range(0, 25, 2)],
                    tickfont=dict(size=12, color='#003366', family='Arial'),
                    range=[-0.2, 24.2],
                    showgrid=False,
                    zeroline=False,
                    side='top',
                    showline=True,
                    linewidth=2,
                    linecolor='#003366'
                ),
                yaxis=dict(
                    title=dict(
                        text="<b>Flights</b>",
                        font=dict(size=14, color='#003366', family='Arial Black')
                    ),
                    showticklabels=False,  # Hide individual flight labels on y-axis
                    showgrid=False,
                    zeroline=False,
                    showline=True,
                    linewidth=2,
                    linecolor='#003366'
                ),
                height=1200,  # FIXED HEIGHT
                hovermode='closest',
                plot_bgcolor='#F8F9FA',
                paper_bgcolor='white',
                bargap=0,  # No gap - we're controlling spacing manually
                margin=dict(l=100, r=60, t=120, b=60),
                font=dict(family='Arial')
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True)
            
            # Information boxes
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f"""
                <div style='background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid {airline_color};'>
                    <h4 style='color: #003366; margin-top: 0;'>📊 Chart Details</h4>
                    <p style='color: #004080;'><b>Airline:</b> {AIRLINE_NAMES.get(selected_airline, selected_airline)}</p>
                    <p style='color: #004080;'><b>Airport:</b> {selected_airport}</p>
                    <p style='color: #004080;'><b>Date:</b> {pd.to_datetime(selected_date).strftime('%b %d, %Y')}</p>
                    <p style='color: #004080;'><b>Departures:</b> {total_flights}</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style='background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 4px solid #FF9800;'>
                    <h4 style='color: #E65100; margin-top: 0;'>🎨 Visual Guide</h4>
                    <p style='color: #E65100;'><span style='background-color: {airline_color}; padding: 2px 8px; color: white; border-radius: 3px;'>{selected_airline}</span> Airline color</p>
                    <p style='color: #E65100;'><span style='color: #E53935;'>●</span> <b>Red Line</b> - Current time</p>
                    <p style='color: #E65100;'><b>Bar Info:</b> Flight# | Tail | Dest | Time</p>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown("""
                <div style='background-color: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #4CAF50;'>
                    <h4 style='color: #2E7D32; margin-top: 0;'>💡 Tips</h4>
                    <p style='color: #2E7D32;'>✈️ Change airline/date/airport above</p>
                    <p style='color: #2E7D32;'>🖱️ Hover over flights for details</p>
                    <p style='color: #2E7D32;'>📊 Each bar = 1 departure</p>
                </div>
                """, unsafe_allow_html=True)
        
        else:
            st.warning(f"⚠️ No departures found from {selected_airport} for {AIRLINE_NAMES.get(selected_airline, selected_airline)} on {pd.to_datetime(selected_date).strftime('%B %d, %Y')}")
            st.info("💡 Try selecting a different date or airport")
    
    else:
        st.info("👆 Please select an airline, date, and airport above to view the departure schedule")

# ============================================================================
# PAGE 2: ANALYTICS DASHBOARD
# ============================================================================
elif page == "📈 Analytics Dashboard":
    st.title("📊 Aviation Analytics Dashboard")
    st.markdown("**Comprehensive flight performance analysis with interactive filters**")
    st.markdown("---")
    
    # Filters in the sidebar (in addition to main sidebar options)
    st.sidebar.markdown("### 🔎 Data Filters")
    
    # Date range filter
    date_range = st.sidebar.date_input(
        "Date Range:",
        value=(df['DATE'].min().date(), df['DATE'].max().date()),
        min_value=df['DATE'].min().date(),
        max_value=df['DATE'].max().date()
    )
    
    # Airline filter
    airlines = st.sidebar.multiselect(
        "Select Airlines:",
        options=sorted(df['AIRLINE'].unique()),
        default=sorted(df['AIRLINE'].unique())
    )
    
    # Apply filters
    if len(date_range) == 2:
        df_filtered = df[
            (df['DATE'] >= pd.to_datetime(date_range[0])) &
            (df['DATE'] <= pd.to_datetime(date_range[1])) &
            (df['AIRLINE'].isin(airlines))
        ].copy()
    else:
        df_filtered = df[df['AIRLINE'].isin(airlines)].copy()
    
    # Filter active flights only
    df_active = df_filtered[df_filtered['CANCELLED'] == 0].copy()
    
    # =======================================================================
    # KEY METRICS ROW
    # =======================================================================
    st.subheader("📍 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_flights = len(df_filtered)
    cancelled_flights = df_filtered['CANCELLED'].sum()
    avg_dep_delay = df_active['DEPARTURE_DELAY'].mean()
    avg_arr_delay = df_active['ARRIVAL_DELAY'].mean()
    ontime_rate = (df_active['DEPARTURE_DELAY'] <= 0).sum() / len(df_active) * 100 if len(df_active) > 0 else 0
    
    col1.metric("Total Flights", f"{total_flights:,}")
    col2.metric("Cancellations", f"{cancelled_flights:,}", 
                delta=f"{(cancelled_flights/total_flights*100):.1f}%", 
                delta_color="inverse")
    col3.metric("Avg Dep. Delay", f"{avg_dep_delay:.1f} min")
    col4.metric("Avg Arr. Delay", f"{avg_arr_delay:.1f} min")
    col5.metric("On-Time Rate", f"{ontime_rate:.1f}%")
    
    st.markdown("---")
    
    # =======================================================================
    # CHART 1: DAILY OPERATIONS OVERVIEW
    # =======================================================================
    st.subheader("📅 Daily Flight Operations & Delays")
    
    daily_stats = df_filtered.groupby('DATE').agg({
        'FLIGHT_NUMBER': 'count',
        'DEPARTURE_DELAY': 'mean',
        'CANCELLED': 'sum'
    }).reset_index()
    daily_stats.columns = ['DATE', 'Total_Flights', 'Avg_Delay', 'Cancellations']
    
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    
    fig1.add_trace(
        go.Scatter(x=daily_stats['DATE'], y=daily_stats['Total_Flights'],
                  name="Flight Volume", line=dict(color='#0078D2', width=2),
                  fill='tozeroy', fillcolor='rgba(0,120,210,0.1)'),
        secondary_y=False
    )
    
    fig1.add_trace(
        go.Scatter(x=daily_stats['DATE'], y=daily_stats['Avg_Delay'],
                  name="Avg Delay", line=dict(color='#C8102E', width=2)),
        secondary_y=True
    )
    
    fig1.update_layout(
        title="Daily Flight Volume vs Average Delays",
        height=400,
        hovermode='x unified',
        plot_bgcolor='white'
    )
    fig1.update_yaxes(title_text="Number of Flights", secondary_y=False, gridcolor='lightgray')
    fig1.update_yaxes(title_text="Average Delay (minutes)", secondary_y=True)
    
    st.plotly_chart(fig1, use_container_width=True)
    
    # =======================================================================
    # CHARTS 2 & 3: SIDE BY SIDE
    # =======================================================================
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏢 Airline Performance")
        
        airline_perf = df_active.groupby('AIRLINE').agg({
            'FLIGHT_NUMBER': 'count',
            'DEPARTURE_DELAY': 'mean',
            'ARRIVAL_DELAY': 'mean'
        }).reset_index()
        airline_perf.columns = ['Airline', 'Flights', 'Dep_Delay', 'Arr_Delay']
        airline_perf = airline_perf.sort_values('Arr_Delay')
        
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=airline_perf['Airline'],
            y=airline_perf['Dep_Delay'],
            name='Departure',
            marker_color='#FF9800'
        ))
        fig2.add_trace(go.Bar(
            x=airline_perf['Airline'],
            y=airline_perf['Arr_Delay'],
            name='Arrival',
            marker_color='#F44336'
        ))
        
        fig2.update_layout(
            title="Average Delays by Airline",
            xaxis_title="Airline",
            yaxis_title="Minutes",
            barmode='group',
            height=400,
            plot_bgcolor='white'
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        st.subheader("⏰ Hourly Delay Pattern")
        
        hourly = df_active.groupby('DEPARTURE_HOUR')['DEPARTURE_DELAY'].mean().reset_index()
        
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=hourly['DEPARTURE_HOUR'],
            y=hourly['DEPARTURE_DELAY'],
            mode='lines+markers',
            line=dict(color='#9C27B0', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(156,39,176,0.2)'
        ))
        
        fig3.update_layout(
            title="Delay Cascade Throughout the Day",
            xaxis_title="Hour of Day (24hr)",
            yaxis_title="Avg Delay (min)",
            height=400,
            plot_bgcolor='white',
            xaxis=dict(gridcolor='lightgray'),
            yaxis=dict(gridcolor='lightgray')
        )
        
        st.plotly_chart(fig3, use_container_width=True)
    
    st.markdown("---")
    
    # =======================================================================
    # CHART 4: DELAY CAUSES PIE CHART
    # =======================================================================
    st.subheader("🔍 Root Causes of Delays")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        delay_causes = df_active[df_active['ARRIVAL_DELAY'] > 0][
            ['AIR_SYSTEM_DELAY', 'SECURITY_DELAY', 'AIRLINE_DELAY',
             'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY']
        ].sum()
        
        fig4 = go.Figure(data=[go.Pie(
            labels=['Air System', 'Security', 'Airline', 'Late Aircraft', 'Weather'],
            values=delay_causes.values,
            hole=0.4,
            marker=dict(colors=['#2196F3', '#FF9800', '#F44336', '#9C27B0', '#4CAF50'])
        )])
        
        fig4.update_layout(
            title="Delay Minutes by Cause",
            height=400
        )
        
        st.plotly_chart(fig4, use_container_width=True)
    
    with col2:
        st.markdown("### Insights")
        
        # Calculate percentages
        total_delay_mins = delay_causes.sum()
        top_cause = delay_causes.idxmax()
        top_cause_pct = (delay_causes.max() / total_delay_mins * 100)
        
        st.info(f"""
        **Top Delay Cause:**
        
        {top_cause.replace('_', ' ').title()}
        
        **{top_cause_pct:.1f}%** of all delay minutes
        
        **Total Delay Time:**
        {total_delay_mins:,.0f} minutes
        ({total_delay_mins/60:,.0f} hours)
        """)

# ============================================================================
# PAGE 3: ROOT CAUSE ANALYSIS
# ============================================================================
elif page == "🔍 Root Cause Analysis":
    st.title("🔬 Root Cause & Hotspot Analysis")
    st.markdown("**Deep dive into delay patterns, problem airports, and operational insights**")
    st.markdown("---")
    
    # Filter to only delayed flights
    df_delayed = df[(df['ARRIVAL_DELAY'] > 0) & (df['CANCELLED'] == 0)].copy()
    
    # =======================================================================
    # SECTION 1: DELAY SEVERITY BREAKDOWN
    # =======================================================================
    st.subheader("📊 Delay Severity Distribution")
    
    # Categorize delays
    df_delayed['DELAY_CATEGORY'] = pd.cut(
        df_delayed['ARRIVAL_DELAY'],
        bins=[0, 15, 30, 60, 120, float('inf')],
        labels=['Minor (0-15m)', 'Moderate (15-30m)', 'Significant (30-60m)', 
                'Major (1-2h)', 'Severe (>2h)']
    )
    
    delay_dist = df_delayed['DELAY_CATEGORY'].value_counts().sort_index()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            x=delay_dist.index,
            y=delay_dist.values,
            labels={'x': 'Delay Category', 'y': 'Number of Flights'},
            title='How Severe Are the Delays?',
            color=delay_dist.values,
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400, showlegend=False, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Key Findings")
        total_delayed = len(df_delayed)
        severe_pct = (df_delayed['ARRIVAL_DELAY'] > 120).sum() / total_delayed * 100
        
        st.metric("Total Delayed Flights", f"{total_delayed:,}")
        st.metric("Severe Delays (>2h)", f"{severe_pct:.1f}%")
        
        avg_delay_delayed = df_delayed['ARRIVAL_DELAY'].mean()
        st.metric("Avg Delay (delayed flights)", f"{avg_delay_delayed:.1f} min")
    
    st.markdown("---")
    
    # =======================================================================
    # SECTION 2: PROBLEM AIRPORTS
    # =======================================================================
    st.subheader("🛬 Airport Hotspot Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### **Worst Departure Airports**")
        
        dept_airports = df[df['CANCELLED'] == 0].groupby('ORIGIN_AIRPORT').agg({
            'FLIGHT_NUMBER': 'count',
            'DEPARTURE_DELAY': 'mean'
        }).reset_index()
        dept_airports.columns = ['Airport', 'Flights', 'Avg_Delay']
        dept_airports = dept_airports[dept_airports['Flights'] >= 100]  # Min 100 flights
        dept_airports = dept_airports.sort_values('Avg_Delay', ascending=False).head(10)
        
        fig = px.bar(
            dept_airports,
            x='Avg_Delay',
            y='Airport',
            orientation='h',
            title='Top 10 Airports with Highest Departure Delays',
            color='Avg_Delay',
            color_continuous_scale='Reds'
        )
        fig.update_layout(height=400, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("#### **Worst Arrival Airports**")
        
        arr_airports = df[df['CANCELLED'] == 0].groupby('DESTINATION_AIRPORT').agg({
            'FLIGHT_NUMBER': 'count',
            'ARRIVAL_DELAY': 'mean'
        }).reset_index()
        arr_airports.columns = ['Airport', 'Flights', 'Avg_Delay']
        arr_airports = arr_airports[arr_airports['Flights'] >= 100]
        arr_airports = arr_airports.sort_values('Avg_Delay', ascending=False).head(10)
        
        fig = px.bar(
            arr_airports,
            x='Avg_Delay',
            y='Airport',
            orientation='h',
            title='Top 10 Airports with Highest Arrival Delays',
            color='Avg_Delay',
            color_continuous_scale='Oranges'
        )
        fig.update_layout(height=400, plot_bgcolor='white')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # =======================================================================
    # SECTION 3: DAY OF WEEK PATTERNS
    # =======================================================================
    st.subheader("📆 When Do Delays Happen?")
    
    # Day of week analysis
    day_names = {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 
                 5: 'Friday', 6: 'Saturday', 7: 'Sunday'}
    
    df_active = df[df['CANCELLED'] == 0].copy()
    df_active['DAY_NAME'] = df_active['DAY_OF_WEEK'].map(day_names)
    
    dow_stats = df_active.groupby('DAY_NAME').agg({
        'FLIGHT_NUMBER': 'count',
        'DEPARTURE_DELAY': 'mean',
        'ARRIVAL_DELAY': 'mean'
    }).reset_index()
    
    # Reorder to start with Monday
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    dow_stats['DAY_NAME'] = pd.Categorical(dow_stats['DAY_NAME'], categories=day_order, ordered=True)
    dow_stats = dow_stats.sort_values('DAY_NAME')
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=dow_stats['DAY_NAME'],
            y=dow_stats['DEPARTURE_DELAY'],
            mode='lines+markers',
            name='Departure',
            line=dict(color='#FF9800', width=3),
            marker=dict(size=10)
        ))
        fig.add_trace(go.Scatter(
            x=dow_stats['DAY_NAME'],
            y=dow_stats['ARRIVAL_DELAY'],
            mode='lines+markers',
            name='Arrival',
            line=dict(color='#F44336', width=3),
            marker=dict(size=10)
        ))
        
        fig.update_layout(
            title='Average Delays by Day of Week',
            xaxis_title='Day',
            yaxis_title='Average Delay (minutes)',
            height=400,
            plot_bgcolor='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(
            dow_stats,
            x='DAY_NAME',
            y='FLIGHT_NUMBER',
            title='Flight Volume by Day of Week',
            color='FLIGHT_NUMBER',
            color_continuous_scale='Blues'
        )
        fig.update_layout(height=400, plot_bgcolor='white', showlegend=False)
        fig.update_xaxes(title='Day')
        fig.update_yaxes(title='Number of Flights')
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # =======================================================================
    # SECTION 4: ACTIONABLE INSIGHTS
    # =======================================================================
    st.subheader("💡 Operational Insights & Recommendations")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🎯 Peak Problem Times")
        
        # Find worst hour
        hourly = df_active.groupby('DEPARTURE_HOUR')['DEPARTURE_DELAY'].mean()
        worst_hour = hourly.idxmax()
        worst_delay = hourly.max()
        
        st.info(f"""
        **Worst Hour:** {worst_hour}:00
        
        Average delay: **{worst_delay:.1f} minutes**
        
        **Recommendation:** Schedule buffer time for flights departing during this hour.
        """)
    
    with col2:
        st.markdown("### 🏢 Best/Worst Carriers")
        
        carrier_avg = df_active.groupby('AIRLINE')['ARRIVAL_DELAY'].mean().sort_values()
        best_carrier = carrier_avg.index[0]
        worst_carrier = carrier_avg.index[-1]
        
        st.success(f"""
        **Best On-Time:**
        {best_carrier} ({carrier_avg.iloc[0]:.1f} min avg delay)
        """)
        
        st.error(f"""
        **Needs Improvement:**
        {worst_carrier} ({carrier_avg.iloc[-1]:.1f} min avg delay)
        """)
    
    with col3:
        st.markdown("### 🌦️ Weather Impact")
        
        weather_delays = df_delayed['WEATHER_DELAY'].sum()
        total_delay_mins = df_delayed['ARRIVAL_DELAY'].sum()
        weather_pct = (weather_delays / total_delay_mins * 100)
        
        st.warning(f"""
        **Weather Delays:**
        {weather_pct:.1f}% of total delay time
        
        **Total:** {weather_delays:,.0f} minutes
        ({weather_delays/60:,.0f} hours)
        
        **Note:** Weather is often unavoidable but can be mitigated with better planning.
        """)

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray; padding: 20px;'>
    <p><b>Aviation Operations Dashboard</b> | Built with Python, Streamlit & Plotly</p>
    <p>💼 Portfolio Project demonstrating data analysis and visualization skills</p>
    <p>📊 Data Source: U.S. Department of Transportation (2015 Flight Data)</p>
</div>
""", unsafe_allow_html=True)