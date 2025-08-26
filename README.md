
# Bird Migration Analysis

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)  
![Libraries](https://img.shields.io/badge/Libraries-Pandas%20%7C%20Matplotlib%20%7C%20Cartopy-green.svg)  
![License](https://img.shields.io/badge/License-MIT-orange.svg)  

---

## Project Overview
This project focuses on analyzing the migration patterns of birds using GPS tracking data. It includes trajectory visualization, speed analysis, time-based movement trends, and geographic mapping of bird paths using Python.

---

## Dataset
- **File:** `bird_tracking.csv`
- **Columns:**
  - `bird_name` – Name of the bird (Eric, Nico, Sanne)
  - `longitude`, `latitude` – GPS coordinates
  - `date_time` – Timestamp of observation
  - `speed_2d` – Bird's speed in 2D (m/s)

---

## Technologies Used
- **Python Libraries**
  - pandas – Data manipulation
  - matplotlib – Data visualization
  - numpy – Numerical operations
  - cartopy – Map projections and geospatial plotting
  - datetime – Time processing

---

## Analysis & Visualizations
### 1. Bird Trajectories  
Plots the movement paths of all tracked birds based on latitude and longitude.  

---

### 2. Speed Distribution  
Histogram of Eric's 2D speed distribution.  

---

### 3. Elapsed Time  
Elapsed time progression for Eric's migration.  

---

### 4. Daily Mean Speed  
Plots the mean daily speed of Eric to observe behavioral patterns.  

---

### 5. Migration Map  
Bird trajectories displayed on a geographical map using Cartopy.  

---

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bird-migration-analysis.git
   cd bird-migration-analysis
   ```
2. Install the required dependencies:
   ```bash
   pip install pandas matplotlib numpy cartopy
   ```
3. Execute the script:
   ```bash
   python BIRD\ migration\ analysis.py
   ```

---

## Features
- Visualize migration paths of multiple birds.
- Analyze speed distribution and daily trends.
- Track elapsed time for individual birds.
- Map migration routes using geographic projections.

---

## Future Enhancements
- Add interactive visualizations using Plotly or Folium.
- Develop machine learning models for migration prediction.
- Create animated migration timelines.

---

## Output

<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/8e625e74-897f-4ac3-bfe7-09753e9e06b1" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/b13b713f-e3ce-4ee7-bb5d-cb59e6bc0f70" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/af68d852-a71b-4b76-a22b-8f6562419da7" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/cedf27ec-9a10-4e10-b65b-260cdac2984f" />
<img width="1366" height="768" alt="Image" src="https://github.com/user-attachments/assets/52815725-53c4-42ec-a529-7496b869d126" />

## License
This project is released under the MIT License.
