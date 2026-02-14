# 🚀 Quick Start Guide

## Getting Your Dashboard Running in 5 Minutes

### Step 1: Install Python
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### Step 2: Download the Project
```bash
# Clone or download this repository
cd aviation-dashboard
```

### Step 3: Install Libraries
```bash
pip install pandas plotly streamlit openpyxl
```

### Step 4: Get the Data
1. Go to [Kaggle Flight Delays Dataset](https://www.kaggle.com/datasets/usdot/flight-delays)
2. Download `flights.csv` (warning: it's ~500MB)
3. Put it in the same folder as `streamlit_app.py`

### Step 5: Run!
```bash
streamlit run streamlit_app.py
```

That's it! The dashboard will open in your browser.

---

## 📱 Using the Dashboard

### Page 1: Flight Operations Timeline
1. Select an **airline** (e.g., United, Delta, American)
2. Pick a **date** from 2015
3. Choose a **departure airport**
4. See all flights for that day!

**Pro tip:** Hover over any flight bar to see detailed info.

### Page 2: Analytics Dashboard
- View daily trends and patterns
- Compare airline performance
- See when delays happen throughout the day
- Understand root causes

### Page 3: Root Cause Analysis
- Find the worst airports for delays
- See which days of the week have most delays
- Get actionable insights

---

## 🎨 Customizing Your View

### Want to see different information on flight bars?

Edit line ~310 in `streamlit_app.py`:

**Current:**
```python
text=f"UA{flight['FLIGHT_NUMBER']} | {flight['TAIL_NUMBER']} | →{flight['DESTINATION_AIRPORT']} | {flight['AIR_TIME']:.0f}min"
```

**Simple version:**
```python
text=f"{flight['FLIGHT_NUMBER']} → {flight['DESTINATION_AIRPORT']}"
```

**With delay info:**
```python
text=f"{flight['FLIGHT_NUMBER']} | {flight['DESTINATION_AIRPORT']} | Delay: {flight['DEPARTURE_DELAY']:.0f}m"
```

### Want thicker/thinner flight bars?

Find these lines (~182):
```python
BAR_HEIGHT = 1.5  # Make this bigger for thicker bars
SPACE_BETWEEN = 0.5  # Make this bigger for more space
```

---

## ❓ Troubleshooting

**"Module not found" error:**
```bash
pip install --break-system-packages pandas plotly streamlit openpyxl
```

**"File not found" error:**
Make sure `flights.csv` is in the same folder as `streamlit_app.py`

**Dashboard is slow:**
This is normal - it's loading millions of flights! First load takes 30-60 seconds.

**No flights showing:**
Try a different date or airport. Not all combinations have data.

---

## 💡 Tips for Recruiters/Interviewers

This project demonstrates:

✅ **Data Analysis:** Processing 5.8M records with Pandas  
✅ **Visualization:** Professional charts with Plotly  
✅ **Web Development:** Interactive dashboard with Streamlit  
✅ **Domain Knowledge:** Aviation operations concepts  
✅ **Problem Solving:** Root cause analysis and insights  
✅ **Code Quality:** Clean, documented, maintainable code  

**Key talking points:**
- "I built an Air Gantt style timeline to visualize flight operations"
- "I analyzed 5.8 million flight records to identify delay patterns"
- "The dashboard helps operations teams identify bottlenecks and optimize schedules"
- "I implemented smart filtering to show relevant data for any airline/airport/date combination"

---

**Questions? Issues? Open an issue on GitHub or reach out!**
