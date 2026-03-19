# Nostradamus — Hurricane Probability Predictor

> **Predict the likelihood of a hurricane striking any location on Earth, for any month of the year.**

A Python-based tool that analyzes the complete [IBTrACS](https://www.ncei.noaa.gov/products/international-best-track-archive) historical cyclone dataset to calculate hurricane probabilities and generate interactive global heatmaps.

---

## Features

- **Location Search** — Enter any city name and get accurate geocoding via the [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) API
- **Monthly Probability** — Calculates the historical probability of a hurricane occurring within ±5° of your location for a chosen month
- **Interactive Heatmap** — Generates a global [Folium](https://python-visualization.github.io/folium/) heatmap showing cyclone intensity for the selected month, with your location pinned on the map
- **Risk Classification** — Categorizes the risk level (Very Low / Low / Moderate / High / Extreme) and displays it as a tooltip on the map
- **Full Historical Data** — Uses the IBTrACS v04r01 dataset covering all ocean basins from 1842 to present (~3 million track records)

---

## Repository Structure

```
├── Nostradamus (early access).py   # Original version — procedural style
├── Nostradamus_improved.py         # Refactored version — vectorized Pandas operations
├── location.py                     # Geocoding helper module
├── PROJECT_EXPLANATION.md          # Detailed documentation of architecture and algorithms
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.8+

```bash
pip install pandas folium branca requests
```

### Dataset

This project requires the **IBTrACS v04r01** dataset (~310 MB), which is too large to include in the repository.

1. Go to the [NOAA NCEI IBTrACS page](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/)
2. Download `ibtracs.ALL.list.v04r01.csv`
3. Rename it to `ALL.csv` and place it in the project root directory

### Running the Program

```bash
git clone https://github.com/Fabricio-Giusti/Nostradamus-Project.git
cd Nostradamus-Project
python Nostradamus_improved.py
```

Follow the prompts:
1. Enter a city name (e.g., `Miami`, `Tokyo, Japan`)
2. Confirm the location found
3. Select a month (1–12)

The terminal will display the hurricane probability and risk level. An interactive heatmap will automatically open in your browser.

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

1. The user's city is geocoded to latitude and longitude via the OpenStreetMap API
2. The IBTrACS dataset is filtered to records within a ±5° bounding box around the location for the selected month
3. Unique Storm IDs are counted and divided by the total years in the dataset to compute the probability
4. An interactive heatmap is generated with all global cyclone track points for that month and the user's location marked

### Risk Classification

| Probability | Risk Level |
|-------------|------------|
| 0% | Very Low — no historical hurricanes recorded |
| < 10% | Low Risk |
| 10% – 29% | Moderate Risk |
| 30% – 49% | High Risk |
| ≥ 50% | Extreme Risk |

---

## Example Output

**Terminal:**
```
The probability of a hurricane in Miami during September is 42.86%.
```

**Heatmap:** An interactive HTML map opens in your browser showing global hurricane activity for the selected month, with your location pinned and a risk-level tooltip.

---

## Technologies

| Tool | Purpose |
|------|---------|
| [Python](https://python.org) | Core language |
| [Pandas](https://pandas.pydata.org/) | Data processing and vectorized filtering |
| [Folium](https://python-visualization.github.io/folium/) | Interactive map generation |
| [Branca](https://github.com/python-visualization/branca) | Colormap legend on the heatmap |
| [Requests](https://docs.python-requests.org/) | HTTP calls to the geocoding API |
| [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/) | Free geocoding service |

---

## Author

**Fabricio Giusti Oliveira Monteiro**
[linkedin.com/in/fabricio-giusti](https://linkedin.com/in/fabricio-giusti)

---

## License

The IBTrACS dataset is provided by NOAA and is publicly available for non-commercial use.
