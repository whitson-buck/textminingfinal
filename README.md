# Wine Sentiment Analysis Project 🍷

Welcome to the Wine Sentiment Analysis Project! I'm on a quest to unravel the juicy secrets hidden within wine reviews, blending the refined critiques of experts with the unfiltered opinions of enthusiasts. Let's dive into the juicy swirl of sentiments. 🌟

## Project Journey 🍇

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
   - index.html and other landing pages are in the templates folder.

5. **User Interaction Galore:**
   - Users can swirl, sniff, and sip through sentiments, exploring trends and uncovering surprises at whittybuck.pythonanywhere.com
   - future note: I am cheap and don't want to pay for hosting, so if the website is down message me here to let me know and I can refresh the site.
  
### p.s. and final addendum 🌃

the summary statistics page reveals this, but experts do not often show much emotion or first-person preference in their reviews. Amateurs, not confined to the verbal prison of pretentious prose, express themselves much more openly and emotionally. Thus, according to this data, amateurs are often categorized as 'liking' a certain wine more. This may not be a fair categorization, because the expert is not writing THEIR personal preference, just observing about the wine itself. Future research will need to find or create data that is a 1-1 comparison with the persons like or dislike included to make a truly fair comparison. This dataset, to my limited understanding, does not currently exist in the public. 

*The main goal of this project was to learn Flask, refine my Python, and do a little problem solving. I hope this accomplished that.*
