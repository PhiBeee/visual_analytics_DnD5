# visual_analytics_DnD5
First assignment for Data Science course at Leiden University 2025  
The goal of this assignment is to create a Dashboard with information on:
- The status and trends with respect to the monetization of the app
- The ratings and feedback given by users 
- The stability (crashes) of the app  

This information is provided based on the data from "Emerald-IT"'s Developer Console logs, which contains:  
- All purchases
- Ratings
- Feedback
- Crashes reported by the customers
# Usage
If running from terminal make sure to be in `src` folder
```
python main.py
```
# Credits 
Geographic shapefile by [geoBoundaries](https://www.geoboundaries.org/)  
Puerto Rico shapefile by [Stanford University](https://purl.stanford.edu/wm713fm9130) made by Hijmans, Robert J.
# To-do's
## Data Pre-Processing
Data pre-processing is mostly done, further pre-processing will be added depending on if we need it for the dashboard or not.
## Bokeh (Webbased Dashboard)
### What we have at the moment
- Slightly nice looking base
- Two charts for Sales Volume:
    - Sales Amount per currency
    - Sales per month per purchase type (SKU ID)

Assignment requirements are:
- ❌ At least 4 widgets visualizing data in a different way each
- ✔️ Sales Volume: sales over time (in terms of at least two measures)
- ✔️ Attribute Segmentation and Filtering: Present Sales volume segmented per attribute (at least SKU ID)
- ❌ Ratings vs Stability: Come up with key performance indicators to help understand app stability vs user satisfaction
- ✔️ (Kinda) Geographical Development: Map of Sales Volume and rating per country
- ❓ Make it look nice (Started, hard to tell without a final product)
## Written Document
TBD
