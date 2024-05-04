library(tidyverse)
library(stringdist)
library(tidytext)
library(vader)
library(textTinyR)

#Datareading

#Amateur data--

amateur_data <- read_csv("winereviews.csv")

#Keep review, title, and points columns

#categories string contains Wine

amateur_data <- amateur_data %>% filter(grepl("Wine", name)|grepl("wine", categories))

#only name, reviews.date, reviews,txt, reviews.title

amateur_data <- amateur_data %>% select(reviews.date, name, reviews.text, reviews.title, reviews.username)

amateur_data$name <- gsub("[-,].*", "", amateur_data$name)

#Prune end of dataset, not actually one type of wine it's a box set

amateur_data <- amateur_data[-(211:255),]

#remove rows in name that contain Yeast

amateur_data <- amateur_data %>% filter(!grepl("Yeast", name))

#remove rows in name that contain Potassium Sorbate

amateur_data <- amateur_data %>% filter(!grepl("Potassium Sorbate", name))

#remove rows in name that contain Vinegar

amateur_data <- amateur_data %>% filter(!grepl("Vinegar", name))

#remove names containing Vintage Wine

amateur_data <- amateur_data %>% filter(!grepl("Vintage Wine", name))

#remove names that contain Smoking Loon

amateur_data <- amateur_data %>% filter(!grepl("Smoking Loon", name))

#remove names that contain Barefoot Cellars 

amateur_data <- amateur_data %>% filter(!grepl("Barefoot Cellars", name))

#remove names that contain Kalamera 12

amateur_data <- amateur_data %>% filter(!grepl("Kalamera 12", name))

#remove names that contain Gerrit Verburg Wine Gums

amateur_data <- amateur_data %>% filter(!grepl("Gerrit Verburg Wine Gums", name))

#remove names that contain Naked Winery

amateur_data <- amateur_data %>% filter(!grepl("Naked Winery", name))

#expert--

expert_data <- read_csv("winemag-data-130k-v2.csv")

#only complete cases for expert data
#129971 rows contain one or more NA values.

expert_data <- expert_data[complete.cases(expert_data),]

#New data 22,387 obs long

#take random sample of 2857 rows of the expert data

set.seed(123)
expert_data <- expert_data[sample(nrow(expert_data), 5000),]

calculate_lv_distance <- function(name, variety) {
  dist <- stringdist::stringdist(name, variety, method = "lv")
  return(dist)
}

# Find lowest cosine distance for each name in amateur dataset
# amateur_data <- amateur_data %>%
#   mutate(lowest_cosine_distance = map_dbl(name, ~ min(map_dbl(expert_data$variety, ~ calculate_cosine_distance(.x, .)))))

merged_data <- amateur_data %>%
  rowwise() %>%
  mutate(expert_index = which.min(map_dbl(expert_data$variety, ~ calculate_lv_distance(name, .))),
         expert_variety = expert_data$variety[expert_index],
         expert_description = expert_data$description[expert_index],
         expert_designation = expert_data$designation[expert_index],
         expert_points = expert_data$points[expert_index],
         expert_price = expert_data$price[expert_index],
         expert_province = expert_data$province[expert_index],
         expert_region_1 = expert_data$region_1[expert_index],
         expert_region_2 = expert_data$region_2[expert_index],
         expert_taster_name = expert_data$taster_name[expert_index],
         expert_taster_twitter_handle = expert_data$taster_twitter_handle[expert_index],
         expert_winery = expert_data$winery[expert_index])

merged_data

#Create a corpus of the reviews.text and the expert_description

library(tm)

corpus <- Corpus(VectorSource(merged_data$reviews.text))

corpus <- tm_map(corpus, content_transformer(tolower))

corpus <- tm_map(corpus, removePunctuation)

corpus <- tm_map(corpus, removeNumbers)

corpus <- tm_map(corpus, removeWords, stopwords("en"))

corpus <- tm_map(corpus, stripWhitespace)

corpus_expert <- Corpus(VectorSource(merged_data$expert_description))

corpus_expert <- tm_map(corpus_expert, content_transformer(tolower))

corpus_expert <- tm_map(corpus_expert, removePunctuation)

corpus_expert <- tm_map(corpus_expert, removeNumbers)

corpus_expert <- tm_map(corpus_expert, removeWords, stopwords("en"))

corpus_expert <- tm_map(corpus_expert, stripWhitespace)

#Create a document term matrix for the reviews.text and the expert_description

dtm <- DocumentTermMatrix(corpus)

dtm_expert <- DocumentTermMatrix(corpus_expert)

#Convert the document term matrix to a data frame

dtm_df <- as.data.frame(as.matrix(dtm))

dtm_expert_df <- as.data.frame(as.matrix(dtm_expert))


#########

library(tidyverse)
library(tm)
library(textblob)
library(vader)
library(afinn)

# Preprocess the text
preprocess <- function(text) {
  text <- tolower(text)
  text <- removePunctuation(text)
  text <- removeNumbers(text)
  text <- removeWords(text, stopwords("en"))
  text <- stripWhitespace(text)
  return(text)
}

# Create corpus for merged data
corpus_merged <- Corpus(VectorSource(merged_data$description))
corpus_merged <- tm_map(corpus_merged, preprocess)

# Function to analyze sentiment using TextBlob
analyze_sentiment_textblob <- function(text) {
  sentiment <- textblob(text)$sentiment
  polarity <- sentiment$polarity
  return(polarity)
}

# Function to analyze sentiment using VADER
analyze_sentiment_vader <- function(text) {
  sentiment <- vader(text)
  compound <- sentiment$compound
  return(compound)
}

# Function to analyze sentiment using AFINN
analyze_sentiment_afinn <- function(text) {
  sentiment <- afinn::afinn_sentiment(text)
  score <- sentiment$score
  return(score)
}

# Analyze sentiment for merged data
merged_data <- merged_data %>%
  mutate(sentiment_textblob = map_dbl(description, analyze_sentiment_textblob),
         sentiment_vader = map_dbl(description, analyze_sentiment_vader),
         sentiment_afinn = map_dbl(description, analyze_sentiment_afinn))

# Print the results
print(merged_data)