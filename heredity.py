import csv
import itertools
import sys
import random

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

    jointProb = 1.0
    pplProbs = []  # Contains probability of each person's gene situation

    # Loop will go through each person in people & get the probability that a
    # person has x amount of genes and does/n't have the trait. This 
    # probability is added to a list of people probabilities
    for person in people:
        geneCount = getGeneCount(person, one_gene, two_genes)

        geneProb = getGeneProb(people, person, one_gene, two_genes, geneCount)
        traitProb = getTraitProb(person, geneCount, have_trait)
        pplProbs.append(geneProb * traitProb)

    for indivProb in pplProbs:
        jointProb *= indivProb

    return jointProb


def getGeneCount(person, one_gene, two_genes):
    """
    This method will return the amount of trait-causing genes that a person 
    has given a set of people with one & two of these genes. If a person is in
    neither sets, then they don't possess the gene.
    """
    
    if person in one_gene:
        return 1
    if person in two_genes:
        return 2
    
    return 0


def getGeneProb(people, person, one_gene, two_gene, geneCount):
    """
    This method will get a person's probability that they have x amount of 
    genes.
    """

    # If a person has their parents, their gene probability depends on the
    # amount of genes their parents have. Otherwise, it's just the default
    # probability that they have x amount of genes.
    if people[person]["mother"]:
        momGeneCount = getGeneCount(people[person]["mother"], one_gene, two_gene)
        dadGeneCount = getGeneCount(people[person]["father"], one_gene, two_gene)

        return geneProbWithParents(geneCount, momGeneCount, dadGeneCount)
    else:
        return PROBS["gene"][geneCount]
    

def geneProbWithParents(geneCount, momGeneCount, dadGeneCount):
    """
    This method will return the probability that a person has x amount of 
    trait-posessing genes given their parents' trait-gene counts. 
    """

    # Getting the probability a parent passes down a trait gene
    momPassProb = parentPassDownProb(momGeneCount)
    dadPassProb = parentPassDownProb(dadGeneCount)

    if geneCount == 0:
        # If person has no trait gene, then this returns likelihood that
        # both parents don't pass their genes
        return (1 - momPassProb) * (1 - dadPassProb)
    
    elif geneCount == 1:
        # Since the person only gets 1 trait gene, they can only get it from
        # just the mom or just the dad. So, it returns the probability that 
        # the mom doesn't pass the trait gene and the dad does, plus the 
        # probability the mom passes the gene and the dad doesn't
        return ((momPassProb * (1 - dadPassProb)) + ((1 - momPassProb) * dadPassProb))
    
    else:
        # Since the person gets 2 genes, returns the probability both parents
        # pass it down
        return momPassProb * dadPassProb

def parentPassDownProb(parentGeneCount):
    """
    This method returns the probability that a parent passes down a gene with 
    a certain trait given they have x amount of genes with the trait. The 
    parents pass down 1 gene each, and there's a chance that it can mutate from
    a clean gene to a trait-posessing (mutated) gene, and vice-versa.
    """

    if parentGeneCount == 0:
        # Only chance to pass it down is if it mutates since they don't have 
        # the gene
        return PROBS["mutation"]
     
    elif parentGeneCount == 1:
        return 0.5
    
    else:
        # Returns if parent has 2 trait-posessing genes. Only chance it doesn't
        # pass down is if the gene mutates
        return 1 - PROBS["mutation"]
    
def getTraitProb(person, geneCount, have_trait):
    """
    This method simply returns the likelihood that a person has or doesn't have 
    the trait they have geneCount amount of trait-inducing genes, and a set of
    people exhibiting the trait. The more of  these genes you have, the higher
    the likelihood that you exhibit the trait.
    """

    exhibitTrait = False

    if person in have_trait:
        exhibitTrait = True

    # Using PROBS dictionary to get probability
    return PROBS["trait"][geneCount][exhibitTrait]

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # Updating each person's probability distribution for trait & gene
    for person in probabilities:
        geneCount = getGeneCount(person, one_gene, two_genes)
    
        exhibitTrait = False
        if person in have_trait:
            exhibitTrait = True
        
        probabilities[person]["gene"][geneCount] += p
        probabilities[person]["trait"][exhibitTrait] += p

def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # Getting the sum of the probability distribution for each person's genes & 
    # normalizing the distribution.
    for person in probabilities:
        # Person that is selected to evaluate sum of probability distributions
        probDistSum = (probabilities[person]["gene"][0] 
        + probabilities[person]["gene"][1] + probabilities[person]["gene"][2])

        # If the sume is zero, then there's no data. Thus, all values in gene 
        # will be 1/3, and both values in trait will be 1/2
        if probDistSum == 0:
            probabilities[person]["gene"][0] = (1 / 3)
            probabilities[person]["gene"][1] = (1 / 3)
            probabilities[person]["gene"][2] = (1 / 3)
            probabilities[person]["trait"][False] = (1 / 2)
            probabilities[person]["trait"][True] = (1 / 2)
        else:
            # Normalizing a person's probability distributions
            probabilities[person]["gene"][0] /= probDistSum
            probabilities[person]["gene"][1] /= probDistSum
            probabilities[person]["gene"][2] /= probDistSum

            probabilities[person]["trait"][False] /= probDistSum
            probabilities[person]["trait"][True] /= probDistSum
    
        


 

        
        
        
        

    


if __name__ == "__main__":
    main()
