# 🍷 Wine Sentiment Analysis Project 📊

Welcome to the Wine Sentiment Analysis Project! I'm on a quest to unravel the juicy secrets hidden within wine reviews, blending the refined critiques of experts with the unfiltered opinions of enthusiasts. Let's dive into the juicy swirl of sentiments. 🌟

## 🚀 Project Journey 🍇

1. **Data Grapevine:**
   - The winemag csv is 'expert' data and winereviews is 'amateur' data. First obviously comes from wine magazine (https://www.kaggle.com/datasets/zynicide/wine-reviews), and the second comes from https://download.data.world/file_download/datafiniti/wine-beer-and-liquor-reviews/wine%20reviews.csv?dwr=US
   - I completed all EDA and data management in the EDA.R file

2. **Data Cleanup Dance:**
   - A VERY important note about the data -- the wine types are not a 1 to 1 match. In fact, I chose to do a fuzzy join based on Levenshtein distance to save time, but the data is imperfect. For example, I attempted to sort out all non-wine reviews in the amateur dataset, but reviews for wine bottle accessories (like aerators) kept joining to Petite Sirah. I manually reviewed the data and was satisfied with how it looked, but take it with a grain of salt.
   - In addition, you may have noticed there are sometimes many amateur reviews, but only ever one expert review. This was the result of the fuzzy join, which I personally think isn't that big of a deal but maybe a more in-depth analysis in the future could find a work around to this.

3. **Sentiment Safari:**
   - Armed with VADER, TextBlob, and Afinn, dissect sentiments like scientists in a wine laboratory.
   - This was all done in the base.py file

4. **Flask Fiesta:**
   - Create nifty Flask web app to compare sentiments and uncover hidden gems.
   - 

5. **User Interaction Galore:**
   - Users can swirl, sniff, and sip through sentiments, exploring trends and uncovering surprises at 
