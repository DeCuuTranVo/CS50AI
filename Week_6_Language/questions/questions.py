import nltk
import sys

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    import os
    # print(directory)
    # print(os.listdir(directory))
    
    file_names = os.listdir(directory)
    file_paths = [os.path.join(directory, filename) for filename in file_names]
        
    # read file content from directory
    content_dict = {}
    
    for idx in range(len(file_names)):
        # print(idx)
        # print(file_names[idx])
        # print(file_paths[idx])
        
        file_content = open(file_paths[idx], "r").read()
        content_dict[file_names[idx]] = file_content
    
    # print(content_dict.keys())
    # for item in content_dict.items():
    #     print(item)
    #     break
        
    return content_dict


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    from nltk.tokenize import word_tokenize
    import string
    # split documents to words
    token_list = word_tokenize(document) 
    
    # converting all characters to lowercase
    lowercase_list = [x.lower() for x in token_list]

    # filter out words that contain puctuation or stopwords
    filtered_document = [] 
    stop_words = nltk.corpus.stopwords.words("english")
    
    for item in lowercase_list:
        if (all(punc not in item for punc in string.punctuation)) and (item not in stop_words):
            filtered_document.append(item)
    
    # print(len(lowercase_list))
    # print(len(filtered_document))
    # print(type(filtered_document))
    # print(filtered_document)
    return filtered_document


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    import math
    # print(documents.keys())
    
    # Initialize words_to_idfs dictionary
    words_to_idfs_dict = {}
    for filename, document in documents.items():
        for word in document:
            if word not in words_to_idfs_dict:
                words_to_idfs_dict[word] = 0.0

    # print(len(words_to_idfs_dict))
    
    # Compute idfs for each word and update dictionary
    for word in words_to_idfs_dict.keys():
        # number of documents
        num_documents = len(documents)
        
        # the number of documents in which the word appears
        num_documents_containing_word = 0.0    
        for filename, document in documents.items():
            if word in document:
                num_documents_containing_word += 1
                
        # inverse idf with natural logarithm
        word_idf = math.log(num_documents/ num_documents_containing_word)
        
        # update dictionary
        words_to_idfs_dict[word] = word_idf
        
    # print(words_to_idfs_dict)    
    # print(words_to_idfs_dict["see"])
    # print(words_to_idfs_dict["impacts"])
    # print(words_to_idfs_dict["ai"])
    return words_to_idfs_dict


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # print(query)
    
    # compute tf_idf for all word in query and all files
    file_to_tf_idf_dict = {}
    
    # for each file in files dictionary
    for filename, file_content in files.items():
        # sum of tf idf for this file and this word
        file_word_tf_idf = 0.0
        
        # for each word in query
        for word in query:
            # compute tf_idf of that word
            # compute term frequency (how manytime this word appear in this document)?
            word_count = 0.0
            for file_word in file_content:
                if file_word == word:
                    word_count += 1
                    
            word_tf = word_count

            # get inverse document frequency
            word_idf = idfs[word]
            
            # compute tf_idf
            word_tf_idf = word_tf * word_idf
            
            # update file_word_idf
            file_word_tf_idf += word_tf_idf
            
        # update file_to_tf_idf_dict
        file_to_tf_idf_dict[filename] = file_word_tf_idf
        
    # sort the file_to_tf_idf_dict dictionary by tf_idf
    sorted_dict = {filename: tf_idf for filename, tf_idf in sorted(file_to_tf_idf_dict.items(), key=lambda item: item[1],  reverse=True)}
    # print(sorted_dict)
    # print(list(sorted_dict.keys()))
    
    # print(sorted_dict)
    
    # list of n top files
    n_top_files = list(sorted_dict.keys())[:n]
    # print(n_top_files)
    
    return n_top_files


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # compute idf and query term density for all word in query and all sentences
    sentences_to_metrics_list = [] # each item in this list should be a tuple
    # print(sentences)    
    
    # for each sentence in sentences dictionary
    for sentence, sentence_word_list in sentences.items():
        # sum of tf idf for this file and this word
 
        sum_idf_current_sentence = 0.0
        # for each word in query
        for word in query:
            # compute tf_idf of that word
            # compute matching word measure: sum of idf values for any word in the query that also appear in the sentence
            if word in sentence_word_list:
                word_idf = idfs[word]
                sum_idf_current_sentence += word_idf
                
        matching_word_measure = sum_idf_current_sentence
                    
        # compute query term density: proportion of words in the sentence that are also words in the query.    
        query_term_freq = 0.0
        for word in sentence_word_list:
            if word in query:
                query_term_freq += 1
                
        query_term_density = query_term_freq/ len(sentence_word_list)
                
        # update sentences_to_metrics_list
        sentence_tuple = (sentence, matching_word_measure, query_term_density)
        sentences_to_metrics_list.append(sentence_tuple)
        
    # sort sentences_to_metrics_list with respect to 2 attribute:
    sorted_list = [item for item in sorted(sentences_to_metrics_list, key = lambda x: (x[1], x[2]), reverse=True)]
    
    # print(sorted_list[:n])
    # only get top n sentence
    return_list = [item[0] for item in sorted_list][:n]
    # print(return_list)
    return return_list


if __name__ == "__main__":
    main()
