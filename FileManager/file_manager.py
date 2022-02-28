from nltk.corpus import stopwords
import re
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer


class FileManager:
    def __init__(self, file_name):
        self.file_name = file_name
        self.articles = []
        self.titles = []

    def read_articles(self):
        index = -1
        is_title = True
        for line in open(self.file_name, 'r', encoding="mbcs"):
            if is_title:
                self.titles.append(line)
                self.articles.append('')
                index += 1
                is_title = False
            elif line == '\n':
                is_title = True
            else:
                self.articles[index] += line
        return self.articles, self.titles

    def process_articles(self):
        processed_articles = []
        stemmer = PorterStemmer()
        tokenizer = RegexpTokenizer(r'\w+')
        stop_words = stopwords.words('english')
        for article in self.articles:
            text = re.sub("[^a-zA-Z#]", " ", article.lower())
            tokens = tokenizer.tokenize(str(text))
            short_tokens = [word for word in tokens if len(word) > 2]
            stopped_tokens = [word for word in short_tokens if word not in stop_words]
            stemmed_tokens = [stemmer.stem(word) for word in stopped_tokens]
            processed_articles.append(' '.join(stemmed_tokens))
        return processed_articles

    def define_terms(self, articles):
        terms_freq = {}
        terms_dict = {}
        tokenizer = RegexpTokenizer(r'\w+')
        index = 0
        for doc in articles:
            tokens = tokenizer.tokenize(str(doc))
            for word in tokens:
                if word not in terms_dict:
                    terms_freq[word] = 1
                    terms_dict[word] = index
                    index += 1
                else:
                    terms_freq[word] += 1
        return terms_dict, terms_freq
