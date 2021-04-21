'''
Discovery of Frequent Itemsets and Association Rules
Author: Bazil Muzaffar Kotriwala
Timestamp: 10 Nov 2020 - 16 Nov 2020
Data used: Sales transaction dataset
'''

# Importing libraries
from itertools import combinations
from timeit import default_timer as timer


def generate_all_single_candidates():
    '''
    This function reads the sales dataset row by row and processes each element in the row. In this function, we
    generate all the length-1 candidates and compute their frequency of occurrence. The length-1
    candidates and their frequency are stored in a dictionary as a (key, value) pair where key = candidate and
    value = frequency. Also, each row is stored as a basket (set) in basket_list which stores all baskets from the
    dataset
    :return: c_1: length-1 candidate set with each candidates total frequency
             all_baskets: A list which has stored all the rows of the dataset as baskets
    '''

    c_1 = {}
    all_baskets = []
    with open("T10I4D100K.dat") as f:
        for row in f:
            row_list = row.split()
            for item in row_list:
                if item in c_1:
                    c_1[item] += 1
                else:
                    c_1[item] = 1
            all_baskets.append(set(row_list))
    return c_1, all_baskets


def filter_candidates(c_k, support):
    '''
    This is a generic function to filter out candidates from the candidate set (c_k) based on the support threshold
    inputted by the user. It filters out the non-frequent candidates and returns the frequent itemset of
    length-k (l_k) which contains the candidate and it's total frequency as (key, value) pair.
    :param c_k: Candidate set (c_k) non-filtered
    :param support: support threshold inputted by the user
    :return: A dictionary containing frequent itemsets with their total frequency > support threshold
    '''

    l_k = {}
    for item, total_count in c_k.items():
        if total_count > support:
            l_k[item] = total_count
    return l_k


def generate_next_candidates(all_baskets, l_1, k):
    '''
    This function iterates over all the baskets in the dataset and finds the frequent common items between l_1
    and each basket. Based on these frequent common items it creates the combinations of length-k. Then it iterates
    over each combination and checks whether it is a subset of basket, if it is it increments the count. At the end
    of the iterations, the whole dataset has been scanned to create and count all frequent item combinations.
    :param all_baskets: A list which has stored all the rows of the dataset as baskets
    :param l_1: Frequent itemset of length-1
    :param k: length of candidates
    :return: c_k: length-k candidate set with each candidates total frequency
    '''

    c_k = {}
    l_1_set = set(l_1.keys())
    for basket in all_baskets:
        frequent_items = list(l_1_set & basket)
        frequent_items.sort()
        current_candidates = list(combinations(frequent_items, k))
        for tup in current_candidates:
            current_candidates_set = set(tup)
            if current_candidates_set.issubset(basket):
                if tup in c_k:
                    c_k[tup] += 1
                else:
                    c_k[tup] = 1
    return c_k


def apriori(all_baskets, support, c_1):
    '''
    This function implements the apriori algorithm. It gets the frequent itemsets for length-1 (L1) and then it
    genrates the candidate sets (C_k) for the remaining k sizes (from 2 onwards) until there are no sets available of
    size k in the dataset. These candidate sets are then filtered based on the support threshold
    using the generic filter_candidates function defined above. The frequent itemsets of length-k (L_k) is merged
    to a dictionary containing all frequent itemsets l_k named all_frequent_itemsets.
    :param all_baskets: A list which has stored all the rows of the dataset as baskets
    :param support: support threshold inputted by the user
    :param c_1: length-1 candidate set with each candidates total frequency
    :return: all_frequent_itemsets - a dictionary containing all the frequent itemsets of length-k (for all k values)
                                     with their counts
             all_frequent_itemsets_greater_than_1 - a dictionary containing all the frequent itemsets of length-k
             except length-1 with their counts, used later for the bonus task of association rule mining
    '''

    l_1 = filter_candidates(c_1, support)
    print("\nFrequent # of length-1 itemsets (L1):", len(l_1))
    all_frequent_itemsets = l_1
    l_k = l_1
    k = 2
    all_itemsets_greater_than_1 = {}
    while len(l_k) != 0:
        c_k = generate_next_candidates(all_baskets, l_1, k)
        l_k = filter_candidates(c_k, support)
        print("Frequent # of length-" + str(k), "itemsets (L" + str(k) + "):", len(l_k))
        all_frequent_itemsets = {**all_frequent_itemsets, **l_k}
        all_itemsets_greater_than_1 = {**all_itemsets_greater_than_1, **l_k}
        k += 1
    return all_frequent_itemsets, all_itemsets_greater_than_1


def generate_association_rules(all_frequent_itemsets, all_itemsets_greater_than_1, conf_threshold):
    '''
    This function computes the association rules based on the support and confidence threshold inputted by the user.
    It iterates over all the frequent itemsets generated previously except those of length-1 and
    computes the combinations possible for each frequent itemset which is then used to compute the confidence and
    if the confidence value >= confidence threshold, then it is appended into a list which tracks the association
    rules.
    :param all_frequent_itemsets: a dictionary containing all the frequent itemsets of length-k (for all k values)
                                     with their counts
    :param all_itemsets_greater_than_1: a dictionary containing all the frequent itemsets of length-k
             except length-1 with their counts, used later for the bonus task of association rule mining
    :param conf_threshold: confidence threshold inputted by the user
    :return: association_rules - A list containing all the association rules along with their support and confidence
                                 values. (all these association rules >= both the support and confidence
                                 threshold values
    '''

    association_rules = []
    for freq_itemset, support in all_itemsets_greater_than_1.items():
        for i in range(1, len(freq_itemset)):
            combination = list(combinations(freq_itemset, i))
            for item in combination:
                curr_item = set(item)
                remaining_items = set(freq_itemset) - curr_item

                if len(item) > 1:
                    conf = support / all_frequent_itemsets[item]
                else:
                    conf = support / all_frequent_itemsets[item[0]]

                if conf > conf_threshold:
                    association_rules.append((curr_item, "->", remaining_items, support, conf))

    return association_rules


if __name__ == '__main__':
    print("Let's find frequent itemsets!\n")
    while True:
        # Ask user for input for the support and confidence value
        support = int(input("\nEnter a support threshold value (any integer) or enter -1 to quit: "))
        if support == -1:
            print('\n The Program has been terminated')
            break
        conf_threshold = float(input("\nEnter a confidence threshold value (0.01 - 0.99) or enter -1 to quit: "))
        if conf_threshold == float(-1):
            print('\n The Program has been terminated')
            break

        print("\nComputing all frequent itemsets with support >= " + str(support) + "...")

        # Generate all candidates of length-1
        start_time = timer()
        c_1, all_baskets = generate_all_single_candidates()

        # Apply the apriori algorithm to calculate all the frequent itemsets
        all_frequent_itemsets, all_itemsets_greater_than_1 = apriori(all_baskets, support, c_1)
        print("Total # of all_frequent_itemsets:", len(all_frequent_itemsets))
        print("All frequent itemsets:", all_frequent_itemsets)

        # Bonus task: Compute all the association rules which are >= support and confidence thresholds
        # Using the frequent itemsets calculated previously
        print("\nComputing all association rules (support >= " + str(support), "and confidence >= " + str(conf_threshold) + ")...")

        association_rules = generate_association_rules(all_frequent_itemsets, all_itemsets_greater_than_1, conf_threshold)
        print("Total # of association rules:", len(association_rules))
        print("Association rules:", association_rules)

        print("\nTotal Running Time: ", round(timer() - start_time, 2), 'seconds')

