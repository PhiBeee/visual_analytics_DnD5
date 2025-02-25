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
## Dependencies 
This python project makes use of a couple modules that are necesarry to generate the html:
```
pip install pandas, geopandas, bokeh, country-converter
```
## Generating the HTML file
If running from terminal make sure to be in `src` folder
```
python main.py
```

## Adding extra final styling
We could not figure out how to change the styling in the head of the HTML file the following needs to be manually added in place of the generated style tags:
```
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,100..1000;1,9..40,100..1000&display=swap" rel="stylesheet">
    <style>
      html, body {
        box-sizing: border-box;
        padding: 0;
        background-color: #15191c;
        color: white;
        align-items: center;
      }

      html{
        display: table;
        margin: auto;
      }

      body{
        display: table-cell;
        vertical-align: middle;
      }
      
    </style>
```
# Credits 
Geographic shapefile by [Natural Earth](https://www.naturalearthdata.com/downloads/110m-cultural-vectors/110m-admin-0-countries/)
# To-do's
## Written Document
We just need to write the report now.
