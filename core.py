import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from os import system

class core:

    import nltk
    
    # nltk.download('omw-1.4')

    lemmatizer = WordNetLemmatizer()

    def __init__(self,docs):
        
        tokenized_docs = self.tokenizing_docs(docs)
        for d in tokenized_docs:
            print(d)
            pass
        
        self.X = self.applying_tf_idf(tokenized_docs)
        
        S = self.svd(self.X)
        
        self.ranking_docks(S)
        
        pass
    
    def preprocess_query(self, query):
        
        # Tokenize, remove stop words, and lemmatize the query
        tokens = word_tokenize(query)
        tokens = [token for token in tokens if token.isalpha()] # Keep only alphabetic tokens
        tokens = [token for token in tokens if token not in stopwords.words('english')] # Remove stop words
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens] # Lemmatize tokens
        
        return tokens
    
    # def query_to_vector(self, query):
        
    #     # Transform the query into a vector using the same vectorizer used for the documents
    #     query_str = ' '.join(query)
    #     query_vector = self.vectorizer.transform([query_str])
        
    #     return query_vector
    

    # def compute_similarity(self, query_vector,X):
    
    #     from sklearn.metrics.pairwise import cosine_similarity
    
        
    #     return similarities
    
    
    def tokenizing_docs(self,docs):
        
        # Tokenize and remove stop words
        processed_documents = []
        
        for document in docs:
            tokens = word_tokenize(document)
            tokens = [token for token in tokens if token.isalpha()] # Keep only alphabetic tokens
            tokens = [token for token in tokens if token not in stopwords.words('english')] # Remove stop words
            tokens = [self.lemmatizer.lemmatize(token) for token in tokens] # Lemmatize tokens
            processed_documents.append(tokens)
        
        return processed_documents

    def applying_tf_idf(self,processed_documents):

        from sklearn.feature_extraction.text import TfidfVectorizer

        # Join processed documents into a single list of strings
        documents_str = [' '.join(doc) for doc in processed_documents]

        # Create the Document-Term matrix
        vectorizer = TfidfVectorizer()

        X = vectorizer.fit_transform(documents_str)

        print(X.shape) # Prints the shape of the matrix
        
        return X
        
    def svd(self,vectoriced_matrix ):
        
        
        #_____________FIX!!!!!!!!!!!
        
        from sklearn.decomposition import TruncatedSVD
        import numpy as np
        
        #print(vectoriced_matrix)
        # Example matrix
        A = np.array(vectoriced_matrix)

        # Compute SVD
        svd = TruncatedSVD(n_components=5)
        svd.fit(svd)

        U = svd.components_
        S = svd.singular_values_
        Vt = svd.transform(A)
        
        print("S:",S)
        
        return S
        
    def ranking_docks(self , S ):
        
         # Rank documents based on the first singular value
        document_ranks = S
        
        # Sort documents by their rank
        sorted_document_ranks = sorted(enumerate(document_ranks),reverse=True)

        # Print the rank of each document
        for  document_index in sorted_document_ranks:
            print(document_index)
            
        pass
    
system('clear')

# Example documents
documents = [
    "Growth produce enter up tree radio art goal live memory six hear  \
    if do enter natural kitchen ok walk social at herself claim student \
    teacher newspaper old employee leg sit pass white become especially",
      
    "Just for natural prevent food sit next whom under identify property indeed \
        who ever social economy agent resource structure however market during try \
            natural surface administration a can painting study early top property kind guy quite instead try.",
    
    "once run hit senior fine teacher line decide others land our contain buy size wife result \
    water challenge door room card mission beautiful keep happen adult enjoy follow people eye onto.\"",
    
    "North quickly yes view place yeah get but carry statement near east score include bill \
        manage point beat store firm color central reflect determine right understand continue \
            up into catch evening chair front challenge yet knowledge simply week election today \
                white morning stage address political test last police free account age growth key \
                    improve million teach game myself.",
    
    "Low born rise watch imagine him political go safe cost simply travel small enough cold military them \
        poor prove adult they despite control couple buy woman month alone forget prepare figure rate very \
            PM he over hard book matter entire example area worry land research up beyond fight grow record \
                trip main stuff question big office others next onto however whatever community more fear manager power forget.",
                
    "Unit within process whether direction capital nearly investment case their life evening risk shoulder factor \
        mean operation financial source develop season out skin knowledge head federal matter available suddenly \
            trip important although couple know truth next lose office phone growth less across you yes want guess \
                beautiful soldier agreement discover main sea."
                    
                
]

core(docs=documents)