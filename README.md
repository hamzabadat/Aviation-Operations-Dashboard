# ✈️ Aviation Operations Dashboard

A comprehensive flight delay analysis and visualization dashboard built with Python, Pandas, Plotly, and Streamlit. This project demonstrates data analysis, visualization, and dashboard development skills for aviation operations, logistics, and business analyst roles.

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.40-red)
![Plotly](https://img.shields.io/badge/Plotly-5.24-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📊 Project Overview

This interactive dashboard analyzes **5.8 million flight records** from 2015 U.S. domestic flights, providing insights into:
- Flight delay patterns and root causes
- Airline performance comparisons
- Airport operational efficiency
- Temporal delay trends (hourly, daily, weekly)
- Real-time flight operations visualization

**Perfect for:** Operations analysts, logistics coordinators, business analysts, and aviation industry professionals.

---

## 🎯 Key Features

### 1. **Flight Operations Timeline** (Air Gantt Style)
- Interactive timeline view of all departures from any airport
- Filter by airline, date, and departure airport
- Real-time indicator showing current time
- Flight details: flight number, tail number, destination, duration
- Color-coded by airline brand colors
- Customizable bar thickness and spacing

### 2. **Analytics Dashboard**
- Daily flight volume and delay trends
- Airline performance comparison (on-time %, average delays)
- Hourly delay cascade visualization
- Root cause analysis (weather, airline issues, air traffic, late aircraft)
- Interactive filters for date range and airline selection

### 3. **Root Cause Analysis**
- Delay severity distribution
- Problem airport identification (departure & arrival hotspots)
- Day-of-week delay patterns
- Actionable operational insights and recommendations

---

## 🚀 Live Demo

[Add your Streamlit Cloud deployment link here once deployed]

---

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/aviation-dashboard.git
cd aviation-dashboard
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Download the Dataset
1. Download the **2015 Flight Delays and Cancellations** dataset from [Kaggle](https://www.kaggle.com/datasets/usdot/flight-delays)
2. Extract the `flights.csv` file
3. Place it in the project root directory

### Step 4: Run the Dashboard
```bash
streamlit run streamlit_app.py
```

The dashboard will open automatically in your default web browser at `http://localhost:8501`

---

## 📁 Project Structure

```
aviation-dashboard/
├── streamlit_app.py          # Main dashboard application
├── dashboard_explained.py     # Heavily commented learning version
├── flights.csv               # Dataset (not included - download separately)
├── airlines.csv              # Airline code lookup table
├── requirements.txt          # Python dependencies
├── README.md                 # This file

```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| **Python 3.13** | Core programming language |
| **Pandas** | Data manipulation and analysis |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web dashboard framework |
| **NumPy** | Numerical computations |

---

## 📊 Dataset Information

**Source:** U.S. Department of Transportation (DOT) Bureau of Transportation Statistics

**Size:** ~5.8 million flight records

**Time Period:** January - December 2015

**Coverage:** U.S. domestic flights from major airlines

### Key Data Fields:
- Flight identifiers (airline, flight number, tail number)
- Airports (origin, destination)
- Scheduled vs actual times (departure, arrival)
- Delay metrics (departure delay, arrival delay)
- Delay causes (weather, air system, security, airline, late aircraft)
- Flight details (distance, air time, taxi times)
- Cancellation data and reasons

---

## 💡 Use Cases

This dashboard is designed to demonstrate skills relevant to:

### **Aviation Operations**
- Flight schedule optimization
- Delay pattern identification
- Airport capacity planning
- Operational bottleneck analysis

### **Business Analysis**
- Performance metrics tracking
- Root cause analysis
- Trend identification
- Data-driven decision making

### **Logistics & Planning**
- Resource allocation optimization
- Timeline visualization
- Capacity management
- Performance benchmarking

---

## 🔧 Customization

### Adjusting the Timeline View

**Flight Bar Thickness:**
```python
BAR_HEIGHT = 1.5  # Increase for thicker bars
```

**Spacing Between Flights:**
```python
SPACE_BETWEEN = 0.5  # Increase for more space
```

**Information Displayed on Bars:**
```python
text=f"{selected_airline}{flight['FLIGHT_NUMBER']} | {flight['TAIL_NUMBER']} | →{flight['DESTINATION_AIRPORT']} | {flight['AIR_TIME']:.0f}min"
```

### Adding New Visualizations

The modular structure makes it easy to add new pages or charts. See `dashboard_explained.py` for detailed comments on how each component works.

---

## 📈 Future Enhancements

Potential features to add:
- [ ] Multi-day view with day navigation
- [ ] Export functionality (PDF, CSV)
- [ ] Predictive delay modeling with ML
- [ ] Airport weather integration
- [ ] Real-time flight tracking API integration
- [ ] Custom alert thresholds
- [ ] Email report automation
- [ ] Mobile-responsive design improvements

---

## 🤝 Contributing

Contributions are welcome! If you'd like to improve this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Hamza Badat**

---

## 🙏 Acknowledgments

- **Data Source:** U.S. Department of Transportation (DOT)
- **Dataset:** Kaggle - Flight Delays and Cancellations (2015)
- **Inspiration:** Real-world aviation operations tools and Air Gantt charts
- **Built with:** Python, Streamlit, Plotly, and Pandas communities

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ and Python

</div>
