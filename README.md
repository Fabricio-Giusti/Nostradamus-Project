<<<<<<< HEAD
# Nostradamus-Project
=======
# Nostradamus — Hurricane Probability Predictor

> **Predict the likelihood of a hurricane striking any location on Earth, for any month of the year.**

A Python-based tool that analyzes the complete [IBTrACS](https://www.ncei.noaa.gov/products/international-best-track-archive) historical cyclone dataset to calculate hurricane probabilities and generate interactive heatmaps.

Developed as an individual Dream Project for **ENGR 13300 — Transforming Ideas to Innovation** at Purdue University (Fall 2024).

---

## Features

- **Location Search** — Enter any city name and get accurate geocoding via [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)
- **Monthly Probability** — Calculates the historical probability of a hurricane occurring within ±5° of your location for a chosen month
- **Interactive Heatmap** — Generates a global [Folium](https://python-visualization.github.io/folium/) heatmap showing cyclone intensity for the selected month, with your location pinned on the map
- **Risk Classification** — Categorizes the risk level (Low / Moderate / High / Extreme) and displays it as a tooltip on the map
- **Full Historical Data** — Uses the IBTrACS v04r01 dataset covering **all ocean basins** from 1842 to present (~300k+ records)

---

## Repository Structure

```
├── Nostradamus (early access).py   # Original version of the program
├── Nostradamus_improved.py         # Refactored & optimized version
├── location.py                     # Geocoding helper module
├── PROJECT_EXPLANATION.md          # Detailed project documentation
└── README.md
```

| File | Description |
|------|-------------|
| `Nostradamus (early access).py` | First working version — procedural style with manual loops |
| `Nostradamus_improved.py` | Improved version — vectorized Pandas operations, cleaner structure, better error handling |
| `location.py` | Utility function that converts a city name to latitude/longitude using OpenStreetMap |
| `PROJECT_EXPLANATION.md` | In-depth documentation of the project architecture and algorithms |

---

## Getting Started

### Prerequisites

- **Python 3.8+**
- Required packages:

```bash
pip install pandas folium branca requests
```

### Running the Program

1. **Clone this repository:**

```bash
git clone https://github.com/Fabricio-Giusti/Nostradamus-Project.git
cd Nostradamus-Project
```

2. **Download the dataset:**
   - Go to the [IBTrACS NOAA page](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/)
   - Download `ibtracs.ALL.list.v04r01.csv`
   - Rename it to `ALL.csv` and place it in the project root directory

3. **Run the improved version:**

```bash
python Nostradamus_improved.py
```

4. **Follow the prompts:**
   - Enter a city name (e.g., `Miami`, `Tokyo, Japan`)
   - Confirm the location found
   - Select a month (1–12)

5. **View the results:**
   - The terminal will display the hurricane probability percentage
   - An interactive heatmap will automatically open in your default browser

---

## How It Works

```
User Input (City + Month)
        │
        ▼
┌──────────────────────┐
│   Geocoding API      │  ──►  Lat/Lon of user's city
│  (OpenStreetMap)     │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│   IBTrACS Dataset    │  ──►  Filter by month & ±5° radius
│     (ALL.csv)        │
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Probability Calc    │  ──►  unique hurricanes / total years × 100
└──────────────────────┘
        │
        ▼
┌──────────────────────┐
│  Heatmap Generation  │  ──►  Interactive HTML map with Folium
└──────────────────────┘
```

1. The user provides a city name, which is geocoded to latitude and longitude
2. The program reads `ALL.csv` and filters hurricane records that fall within a **±5 degree** radius of the user's location for the chosen month
3. The number of **unique hurricanes** (by Storm ID) is divided by the **total number of years** in the dataset to compute a probability
4. An interactive heatmap is generated showing all cyclone track points for that month worldwide, with the user's location marked

---

## Example Output

**Terminal:**
```
The probability of a hurricane in Miami during September is 42.86%.
```

**Heatmap:** An interactive HTML map opens in your browser showing global hurricane activity for the selected month, with your location pinned and a risk-level tooltip.

---

## Dataset

This project requires the **IBTrACS v04r01** (International Best Track Archive for Climate Stewardship) dataset, which is too large (~310 MB) to include in the repository.

**Download:** [ibtracs.ALL.list.v04r01.csv](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/) from NOAA NCEI. Rename the file to `ALL.csv` and place it in the project root.

- **Coverage:** All ocean basins worldwide
- **Time span:** 1842 – present
- **Columns used:** `SID` (Storm ID), `ISO_TIME` (timestamp), `LAT` (latitude), `LON` (longitude)

---

## Technologies

| Tool | Purpose |
|------|---------|
| [Python](https://python.org) | Core programming language |
| [Pandas](https://pandas.pydata.org/) | Data processing and filtering |
| [Folium](https://python-visualization.github.io/folium/) | Interactive map generation |
| [Branca](https://github.com/python-visualization/branca) | Colormap legend on the heatmap |
| [Requests](https://docs.python-requests.org/) | HTTP calls to the geocoding API |
| [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) | Free geocoding service |

---

## Author

**Fabricio Giusti Oliveira Monteiro**  
Purdue University — ENGR 13300 (Fall 2024)  
fgiustio@purdue.edu

---

## License

This project was developed for academic purposes at Purdue University. The IBTrACS dataset is provided by NOAA and is publicly available.
>>>>>>> 3a37171 (Initial commit)
