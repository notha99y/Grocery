# Grocery Repo
This repo contains scripts to do web scraping of e-commerce grocery web pages. <br>
This is done merely as a school project and we adhere to the robots.txt and ethics of being a [good webscrapper](https://towardsdatascience.com/ethics-in-web-scraping-b96b18136f01). <br>

# Requirements
In order to run the code, you would need to have [Anaconda3](https://www.anaconda.com/download/) installed. 

# Setup
1. Clone the repo
```
git clone https://github.com/notha99y/Grocery.git
```
2. Set up conda environment
```
cd Grocery
conda env create -f=environment.yml
```

With this, you are set to do webscraping and some simple data analysis

# RedMart
Somethings you do can with the Redmart Scripts

- Scrap Redmart 
    - This would create a project directory called data/raw, scraps the redmart webpage and saves it into a .json file
    - This would take roughly 10 mins (depending on your internet speed and redmart servers) The .json file would be rougly 200 MB in size
```
python src/redmart.py
```
- Extract data into MongoDB
    - This would extract the relevant information from the raw json data and add it into MongoDB. 
    - The extracted data will be saved into a db called Grocery and in a collection called redmart
```
python src/make_mongodb_redmart.py
```

# FairPrice
TODO