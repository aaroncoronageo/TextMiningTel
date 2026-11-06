library(dplyr)
library(stopwords)
library(tidytext)
library(stringi)
library(stringr)
library(ggplot2)
library(scales)
library(tidyr)
library(widyr)
library(ggraph)
library(igraph)
library(quanteda)
library(topicmodels)
library(cvTools)
library(wordcloud)
library(RColorBrewer)
library(Rcpp)

# Text mining TT

# CCM -----------------------------------------------------------
df <- read.csv('C:/CasaCeviche/V2/dataV2/opinionesV2.csv', header = T, encoding = 'latin1')
sw <- read.csv('C:/DemoProjects/TextMining/sw_spanish.csv', header = T, encoding = 'latin1')
table(df$Lugar)
df <- df %>%
  filter(Rango == 'Más de 800') %>%
  select(1) %>%
  mutate(id = c(1:nrow(.)))

# Analisis exploratorio
review_words <- df %>%
  distinct(Opinion, .keep_all = T) %>% # eliminar filas duplicadas
  unnest_tokens(w, Opinion, drop = F) %>%
  distinct(id, w, .keep_all = T) %>%
  anti_join(sw, by = 'w') %>%
  filter(str_detect(w, '[^\\d]')) %>% # selececciona words con algun comentario
  group_by(w) %>%
  dplyr::mutate(word_total = n()) %>%
  ungroup() # agrega nuevas variables y conserva las existentes

# Wordcloud
df_grouped_V <- review_words %>%
  group_by(w) %>%
  count(w) %>%
  group_by(w) %>%
  mutate(frecuencia = n / dim(review_words)[1])

# Generamos el wordcloud
mas_freq <- sort(df_grouped_V$n, decreasing = T)[3]
df_grouped_V <- df_grouped_V %>%
 filter(n < mas_freq)
wordcloud(words = df_grouped_V$w, freq = df_grouped_V$frecuencia,
          max.words = 100, random.order = F, rot.per = 0.35,
          colors = brewer.pal(8, 'Dark2'))


# Further analysis --------------------------------------------------------
# Bigramas
review_bigrams <- review_words %>%
  unnest_tokens(bigram, Opinion, token = 'ngrams', n = 2) # separamos token
bigrams_separated <- review_bigrams %>%
  separate(bigram, c('w1', 'w2'), sep = ' ') # separamos word por bigrama
bigram_counts <- bigrams_separated %>% 
  dplyr::count(w1, w2, sort = T) # contamos la cantidad de words por bigrama
bigrams_united <- bigram_counts %>%
  unite(bigram, w1, w2, sep = ' ') # count bigrams cleaning
bigrams_united %>%
  dplyr::count(bigram, sort = T)

# Visualizacion
review_subject <- review_words %>% 
  unnest_tokens(w, Opinion)
title_word_pairs <- review_subject %>% 
  pairwise_count(w, id, sort = T, upper = F)

listadoBigramas <- title_word_pairs[which(title_word_pairs$n>10),]
set.seed(1234)
title_word_pairs %>%
  filter(n >= 500) %>%
  graph_from_data_frame() %>%
  ggraph(layout = "fr") +
  geom_edge_link(aes(edge_alpha = n, edge_width = n), edge_colour = "cyan4") +
  geom_node_point(size = 5) +
  geom_node_text(aes(label = name), repel = T, 
                 point.padding = unit(0.2, 'lines')) +
  ggtitle('Bigramas 2021-07')

# Trigramas
review_trigrams <- df %>%
  unnest_tokens(trigram, Title, token = 'ngrams', n = 3) # separamos token
trigrams_separated <- review_trigrams %>%
  separate(trigram, c('w1', 'w2', 'w3'), sep = ' ') # separamos word por trigrama
trigrams_counts <- trigrams_separated %>% 
  dplyr::count(w1, w2, w3, sort = T) # contamos la cantidad de words por trigrama
trigrams_united <- trigrams_counts %>%
  unite(trigrams, w1, w2, w3, sep = ' ') # count trigrams cleaning
trigrams_united %>%
  dplyr::count(trigrams, sort = T)
trigrams_united[2:11, ]

# Bigger topics
df <- read.csv('D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/text_mining_DIC21.csv', header = T)

df_topics <- df %>%
  filter(Topic_Number == 'Mala Red de Datos') %>%
  group_by(ciudad) %>%
  summarise(n_mun = n()) %>%
  filter(n_mun == max(n_mun))

write.csv(df_topics, 'D:/Documents/Tracking_Telefonico/TextMining_TT/NoRecomendacion/DIC21/text_mining_DIC21_group.csv', row.names = F)
