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
# To-do's
## Data Pre-Processing
### Sales 
- Date and Time need to be properly pre-processed with 'pd.to_datetime' according to assignment  
- Product Type needs to be normalized (swaps notation midway through check comment in 'data_preprocessing.py') **NOT THE MOST IMPORTANT**
### Crashes
- Check if columns need merging and handle them like we did for Sales
- Format Date with 'pd.to_datetime'
- Filter package name
### Ratings Country
- Same steps as Crashes
### Reviews and Ratings Overview
- Optional so we'll decide if we do these once everything else is working properly
## Bokeh (Webbased Dashboard)
Nothing has been done on this end since it relies on the Data Pre-processing, but the mentioned requirements are:
- At least 4 widgets visualizing data in a different way each
- Sales Volume: sales over time (in terms of at least two measures)
- Attribute Segmentation and Filtering: Present Sales volume segmented per attribute (at least SKU ID)
- Ratings vs Stability: Come up with key performance indicators to help understand app stability vs user satisfaction
- Geographical Development: Map of Sales Volume and rating per country
