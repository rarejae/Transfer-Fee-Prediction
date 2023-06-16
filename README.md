![Python version](https://img.shields.io/badge/Python%20version-3.11%2B-lightgrey)
![GitHub last commit](https://img.shields.io/github/last-commit/rarejae/Transfer-Fee-Prediction)
![GitHub repo size](https://img.shields.io/github/repo-size/rarejae/Transfer-Fee-Prediction)
![Type of ML](https://img.shields.io/badge/Type%20of%20ML-Regression%20-red)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://rarejae-transfer-fee-prediction-transfer-fee-app-9y2v7q.streamlit.app/)


# Transfer-Fee-Prediction
Transfer fee prediction model and app
- [Streamlit App](https://rarejae-transfer-fee-prediction-transfer-fee-app-9y2v7q.streamlit.app/)

## Authors
- [@rarejae](https://github.com/rarejae)


## Repository Structure
```

├── datasets
│   ├── transfer_data1.csv                        <- 250 most expensive transfers each season 2017-2018
│   ├── transfer_data2.csv                        <- 250 most expensive transfers each season 2019-2020
│   ├── transfer_data3.csv                        <- 250 most expensive transfers each season 2021-2022
│
│
├── model
│   ├── featureScaler.joblib                      <- Scaler object used for standardizing dataset features
│   ├── finalModel.joblib                         <- Trained machine learning model for making predictions
│   ├── targetScaler.joblib                       <- Scaler object used for standardizing target variable
│
│
├── .gitignore                                    <- Ignore unecessary files
│
│
├── README.md                                     <- This file
│
│
├── requirements.txt                              <- All dependencies used (for Streamlit)
│
│
├── scraper.py                                    <- Scraper used to collect data
│
│
├── transfer_fee_app.py                           <- Streamlit app
│
│
├── transfer_fee_prediction.ipynb                 <- Main notebook for model development
```

## Utilizing the Scraper
The web-scraper scrapes the transfermarkt website and works between two season intervals.


The years should be inputted in chronological order and should only span 1 year for example (2019, 2020) or (2017, 2019). 
A span of greater than 1 year will result in requests being denied. The function obtains player information inclusive of both years. 

```
# get_pages obtains the html files of all the pages containing player information
pages = get_pages(2021, 2022)

# get_info extracts all of the relevant player information via BeautifulSoup4
data = get_info(pages)
```

