import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    # Assumption: Each person have either both father and mother or have neither father nor mother.
    # print(people)
    
    known_parents = set() # people who we know both parents
    unknown_parents = set() # people who we don't know about all of their parents
    
    # separent people who we know both parents and people who not.
    for person_name in people.keys():
        if (people[person_name]["father"] is None) and (people[person_name]["father"] is None):
            unknown_parents.add(person_name)
        else:
            known_parents.add(person_name)

    # convert one_gene, two_genes, have_trait to question dict
    question_dict = {}
    for person_name in people.keys():
        question_dict[person_name] = {}
        question_dict[person_name]["name"] = person_name
        
        if person_name in one_gene:
            question_dict[person_name]["gene"] = 1
        elif person_name in two_genes:
            question_dict[person_name]["gene"] = 2
        else:
            question_dict[person_name]["gene"] = 0
        
        if person_name in have_trait:
            question_dict[person_name]["trait"] = True
        else:
            question_dict[person_name]["trait"] = False
            
        question_dict[person_name]["combination_prob"] = None
            
    # print(question_dict) # {'Harry': {'gene': 1, 'trait': False}, 'James': {'gene': 2, 'trait': True}, 'Lily': {'gene': 0, 'trait': False}}


    # for each person who have no parents information
    for person_name in unknown_parents:
        # probability that this person has the number of gene in question (draw from population)
        prob_number_genes = PROBS["gene"][question_dict[person_name]["gene"]] 
        
        # probability that this person has/ has not the trait given that they has the number of gene in question
        prob_have_trait = PROBS["trait"][question_dict[person_name]["gene"]][question_dict[person_name]["trait"]] 
        
        # probability that his person both have the questioned number of gene and the questioned trait
        question_dict[person_name]["combination_prob"] = prob_number_genes * prob_have_trait
        
    # print(question_dict) # {'Harry': {'gene': 1, 'trait': False, 'combination_prob': None}, 'James': {'gene': 2, 'trait': True, 'combination_prob': 0.006500000000000001}, 'Lily': {'gene': 0, 'trait': False, 'combination_prob': 0.9503999999999999}}

    # dictionary mapping gene and allele to the probability that a diseased allele is transfer to the child given that the parent have a certain number of genes.
    # Before mutation
    PROB_PARENT_2_GENE_GIVE_DISEASE_ALLELE = 1.0
    PROB_PARENT_1_GENE_GIVE_DISEASE_ALLELE = 0.5
    PROB_PARENT_1_GENE_GIVE_NORMAL_ALLELE = 0.5
    PROB_PARENT_0_GENE_GIVE_NORMAL_ALLELE = 1.0
    
    # After mutation
    GENE_ALLELE_MAP = {      
        # parent_gene = 0     
        0: {
            # transferred_allele = True (disease)
            True: PROB_PARENT_0_GENE_GIVE_NORMAL_ALLELE * PROBS["mutation"],
            # transferred_allele = False (normal)
            False: PROB_PARENT_0_GENE_GIVE_NORMAL_ALLELE * (1 - PROBS["mutation"]),  
        },
        # parent_gene = 1
        1: {
            # transferred_allele = True (disease)
            True: PROB_PARENT_1_GENE_GIVE_NORMAL_ALLELE * PROBS["mutation"] + PROB_PARENT_1_GENE_GIVE_DISEASE_ALLELE * (1 - PROBS["mutation"]),
            # transferred_allele = False (normal)
            False: PROB_PARENT_1_GENE_GIVE_NORMAL_ALLELE * (1 - PROBS["mutation"]) + PROB_PARENT_1_GENE_GIVE_DISEASE_ALLELE *  PROBS["mutation"],
        },
        # parent_gene = 2     
        2: {
            # transferred_allele = True (disease)
            True: PROB_PARENT_2_GENE_GIVE_DISEASE_ALLELE * (1 - PROBS["mutation"]), 
            # transferred_allele = False (normal)
            False: PROB_PARENT_2_GENE_GIVE_DISEASE_ALLELE * PROBS["mutation"],
        },
    }

    # for each person who have both parents information
    for person_name in known_parents:
        # get person's mom name
        mom_name = people[person_name]["mother"]
        
        # get person's dad name
        dad_name = people[person_name]["father"]
        
        # print(person_name, mom_name, dad_name)
        dad_gene = question_dict[dad_name]["gene"]
        mom_gene = question_dict[mom_name]["gene"]
        prob_child_gene = None
        prob_child_trait = None
        
        if question_dict[person_name]["gene"] == 0: # # if desired child_gene = 0:      
            prob_normal_allele_from_dad = GENE_ALLELE_MAP[dad_gene][False]
            prob_normal_allele_from_mom = GENE_ALLELE_MAP[mom_gene][False]
            
            prob_child_gene = prob_normal_allele_from_dad * prob_normal_allele_from_mom
            prob_child_trait = PROBS["trait"][question_dict[person_name]["gene"]][question_dict[person_name]["trait"]] 
                
        elif question_dict[person_name]["gene"] == 1: # if desired child_gene = 1:       
            prob_normal_allele_from_dad = GENE_ALLELE_MAP[dad_gene][False]
            prob_disease_allele_from_mom = GENE_ALLELE_MAP[mom_gene][True]
            
            prob_disease_allele_from_dad = GENE_ALLELE_MAP[dad_gene][True]
            prob_normal_allele_from_mom = GENE_ALLELE_MAP[mom_gene][False]
            
            prob_child_gene = prob_normal_allele_from_dad * prob_disease_allele_from_mom + prob_disease_allele_from_dad * prob_normal_allele_from_mom 
            prob_child_trait = PROBS["trait"][question_dict[person_name]["gene"]][question_dict[person_name]["trait"]] 
            
        else: # question_dict[person_name]["gene"] == 2: # # if desired child_gene = 2:     
            prob_disease_allele_from_dad = GENE_ALLELE_MAP[dad_gene][True]
            prob_disease_allele_from_mom = GENE_ALLELE_MAP[mom_gene][True]
            
            prob_child_gene = prob_disease_allele_from_dad * prob_disease_allele_from_mom
            prob_child_trait = PROBS["trait"][question_dict[person_name]["gene"]][question_dict[person_name]["trait"]] 
            
        question_dict[person_name]["combination_prob"] = prob_child_gene * prob_child_trait
          
        # print(people[person_name]) # {'name': 'Harry', 'mother': 'Lily', 'father': 'James', 'trait': None}
        # print(question_dict[person_name]) # {'name': 'Harry', 'gene': 1, 'trait': False, 'combination_prob': None}
    
    # multiply the each individual's combination probability.
    joint_probability_family = 1.0
    for person_name in question_dict.keys():
        prob_person_gen_trait_combination = question_dict[person_name]['combination_prob']
        joint_probability_family *= prob_person_gen_trait_combination
        
    return joint_probability_family


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # print("p=", p) # p= 0.0026643247488
    # print(probabilities)
    """  
    {'Harry': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
     'James': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}, 
     'Lily': {'gene': {2: 0, 1: 0, 0: 0}, 'trait': {True: 0, False: 0}}}
    """
    
    # the function should not return any value, it only need to update probabilities dictionary
    for person_name in probabilities.keys():        
        if person_name in one_gene:
            probabilities[person_name]["gene"][1] += p 
        elif person_name in two_genes:
            probabilities[person_name]["gene"][2] += p 
        else: # person_name in no_gene
            probabilities[person_name]["gene"][0] += p 
        
        if person_name in have_trait:
            probabilities[person_name]["trait"][True] += p 
        else: # person_name not in have_trait:
            probabilities[person_name]["trait"][False] += p 


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # the function should not return any value, it only need to update probabilities dictionary
    # print(probabilities)
    
    for person_name in probabilities.keys():   
        # print(person_name)
        sum_prob_num_gene = 0.0
        for num_gene, prob_num_gene in probabilities[person_name]["gene"].items():
            sum_prob_num_gene += prob_num_gene
            
        for num_gene, prob_num_gene in probabilities[person_name]["gene"].items():
            probabilities[person_name]["gene"][num_gene] /= sum_prob_num_gene
            # print(num_gene, probabilities[person_name]["gene"][num_gene])
            
        sum_prob_trait_presence = 0.0
        for trait_presence, prob_presence in probabilities[person_name]["trait"].items():
            sum_prob_trait_presence += prob_presence
            
        for trait_presence, prob_presence in probabilities[person_name]["trait"].items():
            probabilities[person_name]["trait"][trait_presence] /= sum_prob_trait_presence
            # print(trait_presence, probabilities[person_name]["trait"][trait_presence])


if __name__ == "__main__":
    main()
