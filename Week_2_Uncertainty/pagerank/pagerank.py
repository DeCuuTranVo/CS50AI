import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


# real main function
def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # initialize data structure
    probability_dict = {}
    for from_page in corpus.keys():
        probability_dict[from_page] = 0.0
        
    # if a page has no links, we can pretend it has links to all pages in the corpus, including itself.
    is_no_links = len(corpus[page]) == 0
    if is_no_links == False:  
        # initialize data structure
        linkout_dict = {}
        allpage_dict = {}
        for from_page in corpus.keys():
            linkout_dict[from_page] = 0.0
            allpage_dict[from_page] = 0.0
        # randomly choose one of the links from page with equal probability With probability (damping_factor)
        linkout_pages = corpus[page]
        for linkout_page in linkout_pages:
            linkout_dict[linkout_page] += damping_factor * (1.0/len(linkout_pages))
        
        # randomly choose one of all pages in the corpus with equal probability with probability (1 - damping_factor)
        for a_page in allpage_dict:
            allpage_dict[a_page] = (1 - damping_factor) * (1.0/len(allpage_dict))
        
        # add those two probability for each pages
        for key in corpus.keys():
            probability_dict[key] = linkout_dict[key] + allpage_dict[key]
    else:        
        # equal probability with no damping factor
        for key in corpus.keys():
            probability_dict[key] = (1.0/len(corpus.keys()))
         
    return probability_dict
    

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    # Initiate the pagerank_dictionary and transition_dictionary
    pagerank_dictionary = dict()     # print(pagerank_dictionary)
    transition_dictionary = dict()
    
    # Loop through each page
    for from_page in corpus.keys():
        # Initiate pagerank dictionary for each page
        pagerank_dictionary[from_page] = 0.0 
        
        # Pre-compute transition_model's probability distribution for each page
        from_page_transition_model = transition_model(corpus, from_page, damping_factor)
        transition_dictionary[from_page] = from_page_transition_model
    
    # choose a random page
    current_page = random.choice(list(corpus.keys())) ## print(current_page)
    pagerank_dictionary[current_page] += 1
    
    # for each sample from 1 to n - 1
    for idx in range(1, n):
        # call transition model and get probability distribution
        current_transition_model = transition_dictionary[current_page]
        
        # use transition model to choose next page
        next_page = random.choices(list(current_transition_model.keys()), weights=list(current_transition_model.values()), k=1)[0]
        
        # update the current page variable and the return dictionary
        pagerank_dictionary[next_page] += 1
        current_page = next_page
        
    # normalize pagerank_dictionary
    sum_page_rank = 0 # check sum if total page count == total number of sample
    for from_page in corpus.keys():
        pagerank_dictionary[from_page] /= n #n is the number of samples
        sum_page_rank += pagerank_dictionary[from_page]
        
    # normalize pagerank_dictionary again
    for from_page in corpus.keys():
        pagerank_dictionary[from_page] /= sum_page_rank #n is the number of samples
        
    # print(sum_page)
    
    # # Debug by calculating total sum
    # total_sum = 0
    # for a_page in pagerank_dictionary:
    #     total_sum += pagerank_dictionary[a_page]
    # print("Debug sample page rank, total sum: ", total_sum)
    
    # return pagerank_dictionary
    return pagerank_dictionary


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # begin by assigning each page a rank of 1 / N, where N is the total number of pages in the corpus.
    # Initiate the pagerank_dictionary
    pagerank_dictionary = dict()     # print(pagerank_dictionary)
    
    # print(corpus)
    # Loop through each page
    for from_page in corpus.keys():
        # Initiate pagerank dictionary for each page
        pagerank_dictionary[from_page] = (1.0/len(corpus.keys()))
        
        # A page that has no links at all should be interpreted as having one link for every page in the corpus (including itself).
        if len(corpus[from_page]) == 0:
            for each_page in corpus.keys():
                corpus[from_page].add(each_page)
        
    # build inverse_corpus: key: to_page, value: a set of form_page
    inverse_corpus = dict() 
    for page in corpus.keys(): # initialize
        inverse_corpus[page] = set()
            
    for from_page in corpus.keys(): # operate
        to_pages = corpus[from_page]
        for to_page in to_pages:   
            inverse_corpus[to_page].add(from_page)
    
    # print(pagerank_dictionary)
    # print(corpus)
    # print(inverse_corpus)
    

    # compute parameters
    d = damping_factor # damping factor
    N = len(corpus) #  corpus length
    limit_threshold = 0.001 
    
    # For each iterations
    while True:
        # # Loop through scopus, for each pages, calculate PR(p)
        num_consecutive_page_rank_change_under_limit = 0
        
        for current_page in inverse_corpus.keys():
            first_term = 0.0
            second_term = 0.0
            
            # calculate first term(1-d)/N
            first_term = (1-d)/N
            
            # calculate second term d*SUM{i}{(PR(i)/NumLinks(i))}
            last_pages = inverse_corpus[current_page]
            for last_page in last_pages:
                pagerank_last_page = pagerank_dictionary[last_page]
                numlink_last_page = len(corpus[last_page])
                second_term += pagerank_last_page/numlink_last_page
                
            second_term = d*second_term      
                
            # Update pagerank for that page
            last_pagerank_current_page = pagerank_dictionary[current_page]  
            current_pagerank_current_page = first_term + second_term
            pagerank_dictionary[current_page] = current_pagerank_current_page
            
            # check if the small threshold not change by a small value 
            if abs(current_pagerank_current_page - last_pagerank_current_page) <= limit_threshold:
                num_consecutive_page_rank_change_under_limit += 1
            else:
                num_consecutive_page_rank_change_under_limit = 0
                
        # if all page have their page rank change < limit_threshold
        if num_consecutive_page_rank_change_under_limit >= len(corpus):
            break

    # normalize pagerank_dictionary
    # compute total page rank probability
    sum_page_rank = 0 
    for from_page in corpus.keys():
        sum_page_rank += pagerank_dictionary[from_page]
                
    # divide current probability to total page rank probability
    for from_page in corpus.keys():
        pagerank_dictionary[from_page] /= sum_page_rank #n is the number of samples
        
    # # Debug iterative pagerank by calculating total sum
    # total_sum = 0
    # for a_page in pagerank_dictionary:
    #     total_sum += pagerank_dictionary[a_page]
    # print("Debug iterative pagerank, total sum: ", total_sum)
    # 
    return pagerank_dictionary


if __name__ == "__main__":
    main()
