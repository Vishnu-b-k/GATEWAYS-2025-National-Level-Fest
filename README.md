# GATEWAYS 2025 - Streamlit Analytics Dashboard

## Project Overview

This project is a data-driven web application built using Streamlit for the GATEWAYS 2025 National Level Tech Fest organized at Christ University. The application analyzes participation data from 250 students across multiple states, colleges, and events in India. It provides visual insights to the core organizing team through interactive charts, maps, and feedback analysis.

The dataset used is a CSV file named "C5-FestDataset - fest_dataset.csv" which contains information such as student name, college, state, event name, event type, amount paid, feedback text, and rating.

---

## Features

### Page 1 - Participation Trends
- Choropleth map of India showing the number of participants from each state
- Bar charts showing event-wise and college-wise participation
- Donut chart comparing individual vs group event participation
- Revenue breakdown by event
- Treemap showing college and event distribution

### Page 2 - Feedback and Ratings Analysis
- Word cloud generated from participant feedback text
- Rating distribution chart (1 to 5 stars)
- Average rating per event
- Sentiment tag frequency chart based on common feedback phrases
- Heatmap showing average rating by state and event
- Searchable table of all feedback records with filters

### Page 3 - Executive Dashboard
- Summary KPI cards showing total participants, revenue, average rating, top event, top state, and top college
- Bubble chart mapping states to events with participant count and average rating
- Top colleges by revenue
- Sunburst chart showing the hierarchy of State, College, and Event
- Box plot for rating distribution per event
- Grouped bar chart showing individual vs group participation by state
- Key insights panel with auto-generated summary
- Scatter plot showing relationship between registration fee and rating

---

## Project Structure

```
ETE/
|-- app.py                          (Home page)
|-- pages/
|   |-- 1_Participation_Trends.py   (Participation analysis)
|   |-- 2_Feedback_Analysis.py      (Feedback and ratings)
|   |-- 3_Dashboard.py              (Executive dashboard)
|-- C5-FestDataset - fest_dataset.csv
|-- requirements.txt
|-- README.md
```

---

## Requirements

Python 3.9 or above is recommended.

Install all dependencies using:

```
pip install -r requirements.txt
```

The requirements.txt file contains:
- streamlit
- pandas
- plotly
- wordcloud
- matplotlib
- pillow
- numpy

---

## How to Run

Step 1 - Make sure Python is installed on your system.

Step 2 - Open a terminal or command prompt and navigate to the project folder.

```
cd path/to/ETE
```

Step 3 - Install the required libraries.

```
pip install -r requirements.txt
```

Step 4 - Run the Streamlit application.

```
streamlit run app.py
```

Step 5 - The app will open in your browser automatically at http://localhost:8501
Use the sidebar to navigate between pages.

---

## Implementation Steps

1. Collected and examined the dataset (250 rows, 10 columns).
2. Loaded the data using pandas and cleaned column names.
3. Built the home page with KPI summary cards showing key statistics.
4. Used Plotly Express choropleth with India GeoJSON to render the state-wise map.
5. Created bar charts, pie charts, treemaps, and box plots using Plotly Express.
6. Integrated the WordCloud library to visualize participant feedback text.
7. Built a heatmap using Plotly imshow to show rating distribution across states and events.
8. Designed an executive dashboard with a bubble chart, sunburst chart, and auto-generated key insights.
9. Added sidebar filters (event, state, rating range) to each page.
10. Applied custom CSS for consistent styling, fonts, and layout.

---

## Design and UI References

The visual theme of the application uses a pastel and pale color palette with soft lavender, pink, mint, and cream tones. The design is inspired by modern data dashboard aesthetics.

Font Reference:
- Google Fonts - Inter (https://fonts.google.com/specimen/Inter)
- Used for all headings, labels, and body text across the app

Color Palette Reference:
- Pastel palette inspired by Coolors (https://coolors.co)
- Colors used: #c9b8ff (lavender), #ffb3c6 (blush pink), #b3e5fc (sky blue), #b9f6ca (mint green), #ffe082 (pale yellow)

GeoJSON Reference for India Map:
- India States GeoJSON by jbrobst on GitHub Gist
- URL: https://gist.github.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112

Plotting Library:
- Plotly Documentation (https://plotly.com/python/)
- Streamlit Documentation (https://docs.streamlit.io)

WordCloud Library:
- WordCloud for Python (https://amueller.github.io/word_cloud/)

---

## Dataset Columns

| Column Name       | Description                              |
|-------------------|------------------------------------------|
| Student Name      | Name of the participant                  |
| College           | College of the participant               |
| Phone Number      | Contact number                           |
| Place             | City of residence                        |
| State             | State of residence                       |
| Event Name        | Name of the event participated in        |
| Event Type        | Individual or Group                      |
| Amount Paid       | Registration fee paid                    |
| Feedback on Fest  | Text feedback provided by the student    |
| Rating            | Rating given by student (1 to 5)         |

---

## Notes

- No login or session management is used. All filters are applied directly through sidebar widgets.
- The India map requires an internet connection to load the GeoJSON file from GitHub.
- The app is built for academic demonstration purposes as part of the Advanced Python Programming course at Christ University.
