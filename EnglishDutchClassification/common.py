import sys
import re
import math
import string

'''
A single data point in a dataset.
Can either be weighted or unweighted and labelled or unlabelled.
'''
class Datum:
    def __init__(self, language, content) -> None:
        self.language = language
        self.content = content
        self.split_content = [w.translate(str.maketrans('', '', string.punctuation)) for w in re.split(r"\b\W\b", self.content)]
        self.features = self.extract_features()
        self.weight = 1

    def extract_features(self):
        return [
            # self.sentence_length() > 100,
            self.average_word_length() > 6,
            self.average_word_length() > 8,
            self.average_word_length() > 10,
            self.average_word_length() > 12,
            # self.longest_word() > 12,
            # self.frequency('e') > 0.13,
            self.contains(['the']),
            self.contains(['be']),
            self.contains(['to']),
            self.contains(['of']),
            self.contains(['and']),
            self.contains(['a']),
            self.contains(['is']),
            self.en_function_word(),
            self.contains(['de']),
            self.contains(['het']),
            self.contains(['ik']),
            self.contains(['je']),
            self.contains(['en']),
            self.contains(['van']),
            self.contains(['det']),
            self.nl_function_word(),
            self.contains(['the', 'be', 'to']),
            self.contains(['of', 'and', 'a', 'is']),
            self.contains(['de', 'het', 'ik']),
            self.contains(['je', 'en', 'van', 'dat']),
            self.vowel_pairs() > 1,
            self.vowel_pairs() > 2,
            self.vowel_pairs() > 3,
            self.vowel_pairs() > 4,
            self.vowel_pairs() > 5,
            self.vowel_pairs() > 6,
            self.first_letter('t') > 1,
            self.first_letter('t') > 2,
            self.first_letter('t') > 3,
            self.first_letter('t') > 4,
            self.first_letter('t') > 5,
            self.first_letter('t') > 6,
            self.first_letter('d') > 1,
            self.first_letter('d') > 2,
            self.first_letter('d') > 3,
            self.first_letter('d') > 4,
            self.first_letter('d') > 5,
            self.first_letter('d') > 6,
            self.last_letter('n') > 1,
            self.last_letter('n') > 2,
            self.last_letter('n') > 3,
            self.last_letter('n') > 4,
            self.last_letter('n') > 5,
            self.last_letter('n') > 6,
            self.last_letter('e') > 1,
            self.last_letter('e') > 2,
            self.last_letter('e') > 3,
            self.last_letter('e') > 4,
            self.last_letter('e') > 5,
            self.last_letter('e') > 6,
            self.percentage_of(['a', 'e', 'i', 'o', 'u']) > 0.05,
            self.percentage_of(['a', 'e', 'i', 'o', 'u']) > 0.1,
            self.percentage_of(['a', 'e', 'i', 'o', 'u']) > 0.15,
            self.percentage_of(['a', 'e', 'i', 'o', 'u']) > 0.2,
            self.percentage_of(['a', 'e', 'i', 'o', 'u']) > 0.25,
            self.count('z') > 1,
            self.count('z') > 2,
            self.count('z') > 3,
            self.count('x') > 1,
            self.count('x') > 2,
            self.count('x') > 3,
            self.count('q') > 1,
            self.count('q') > 2,
            self.count('q') > 3,
        ]
    
    def sentence_length(self):
        return len(self.content)
    
    def percentage_of(self, words):
        total = 0
        for w in words:
            total += self.frequency(w)
        return total


    def longest_word(self):
        longest = len(self.split_content[0])
        for w in self.split_content:
            if len(w) > longest:
                longest = len(w)
        return longest
    
    def contains(self, words):
        for w in self.split_content:
            if w.strip().lower() in words:
                return True
        return False
    
    def nl_function_word(self):
        return self.contains(['de', 'het', 'ik', 'je', 'en', 'van', 'dat'])

    def en_function_word(self):
        return self.contains(['the', 'be', 'to', 'of', 'and', 'a', 'is'])

    def average_word_length(self):
        avg = 0
        for w in self.split_content:
            avg += len(w)
        return avg / len(self.split_content)
    
    def frequency(self, letter):
        sanitized = self.content.replace(' ', '').strip().lower()
        sanitized = sanitized.translate(str.maketrans('', '', string.punctuation))

        count = 0
        for c in sanitized:
            if c == letter:
                count += 1
        return count / len(sanitized)
    
    def count(self, letter):
        sanitized = self.content.replace(' ', '').strip().lower()
        sanitized = sanitized.translate(str.maketrans('', '', string.punctuation))

        count = 0
        for c in sanitized:
            if c == letter:
                count += 1
        return count

    def vowel_pairs(self):
        pair_count = 0

        for w in self.split_content:
            if 'aa' in w:
                pair_count += 1
            if 'ee' in w:
                pair_count += 1
            if 'ii' in w:
                pair_count += 1
            if 'oo' in w:
                pair_count += 1
            if 'uu' in w:
                pair_count += 1

        return pair_count
    
    def first_letter(self, letter):
        letter_count = 0

        for w in self.split_content:
            if w.lower().startswith(letter):
                letter_count += 1

        return letter_count
    
    def last_letter(self, letter):
        letter_count = 0

        for w in self.split_content:
            if w.lower().endswith(letter):
                letter_count += 1

        return letter_count
    
def B(b):
    return -(b * math.log2(b) + (1-b) * math.log2(1-b))

def entropy(node):
    if len(node) == 0:
        return 0

    ProbEN = ProbNL = 0
    for n in node:
        if n.language == 'en':
            ProbEN += 1 * n.weight
        elif n.language == 'nl':
            ProbNL += 1 * n.weight
    ProbEN /= len(node)
    ProbNL /= len(node)

    if ProbEN == 0 or ProbEN == 1:
        return 0
    
    return B(ProbEN)
    
def plurality_value(v):
    probEN = 0
    probNL = 0
    for i in v:
        if i.language == 'en':
            probEN += 1 * i.weight
        elif i.language == 'nl':
            probNL += 1 * i.weight
    # print(f'en:{probEN}, nl:{probNL}')
    if probEN > probNL:
        return 'en'
    return 'nl'

class DecisionTreeNode:
    def __init__(self, value = None, weight = None, left = None, right = None) -> None:
        self.value = value
        self.weight = weight
        self.left = left
        self.right = right

'''
A decision tree model with a default depth of 10.
'''
class DecisionTreeModel:
    def __init__(self, depth = 10) -> None:
        self.root = DecisionTreeNode()
        self.depth = depth

    def train_decision_tree_helper(self, parent, current, depth, tag=''):
        plurality_value(current)
        node = DecisionTreeNode()

        if len(current) == 0:
            # print(tag, plurality_value(parent))
            node.value = plurality_value(parent)
            return node
        if depth == 0:
            # print(tag, plurality_value(current))
            node.value = plurality_value(current)
            return node
        
        en = False
        nl = False
        monotypic = en ^ nl
        for c in current:
            if c.language == 'en':
                en = True
            elif c.language == 'nl':
                nl = True
        if monotypic == True:
            node.value = current[0].language
            return node

        original = entropy(current)

        # print(f'[{tag}] entropy: {original}')

        max_info_gain = 0
        index = 0
        new_left = []
        new_right = []
        for b in range(0, len(current[0].features)-1):
            left = []
            right = []
            for d in current:
                if d.features[b] == True:
                    left.append(d)
                elif d.features[b] == False:
                    right.append(d)
            gain = original - (len(left)/len(current) * entropy(left) + len(right)/len(current) * entropy(right))
            if gain > max_info_gain:
                max_info_gain = gain
                index = b
                new_left = left
                new_right = right

        # print(f'[{tag}] {index} : {max_info_gain}')
        # print(f'[{tag}] new entropy: {original-max_info_gain}')

        node.value = index
        node.left = self.train_decision_tree_helper(current, new_left, depth - 1, tag + 'L')
        node.right = self.train_decision_tree_helper(current, new_right, depth - 1, tag + 'R')

        return node
    
    '''
    train a model given a labelled dataset
    '''
    def train_model(self, current):
        self.root = self.train_decision_tree_helper([], current, self.depth)
    
    '''
    classify an unknown piece of data given a Datum
    '''
    def classify(self, unknown):
        root = self.root
        while root != None:
            if root.left == None and root.right == None:
                return root.value
            
            index = root.value
            if unknown.features[index] == True:
                root = root.left
            else:
                root = root.right

        return 'ERROR, could not classify??'


'''
An Adaboost model with 10 as a default number of stumps
'''
class AdaBoostModel:
    def __init__(self, num_stumps=10) -> None:
        self.stumps = []
        self.num_stumps = num_stumps
      
    '''
    train a model given a labelled dataset
    '''
    def train_model(self, data):
        for _ in range(0, self.num_stumps):
            err = 0

            stump = DecisionTreeModel(1)
            stump.train_model(data)
            
            for i in range(0, len(data)):
                data[i].weight = 1/len(data)

            for d in data:
                p = stump.classify(d)

                if p != d.language:
                    err += d.weight

            update = err/(1-err)
            for i in range(0, len(data)):
                d = data[i]
                p = stump.classify(d)

                if p == d.language:
                    data[i].weight *= update

            # min_weight = data[0].weight
            # max_weight = data[0].weight
            weight_sum = 0
            for d in data:
                weight_sum += d.weight
                # max_weight = max(max_weight, d.weight)
                # min_weight = min(min_weight, d.weight)

            for i in range(0, len(data)):
                # data[i].weight = (data[i].weight - min_weight)/(max_weight - min_weight)
                data[i].weight = data[i].weight / weight_sum

            Hw = .5 * math.log((1-err)/err)
            stump.root.weight = Hw
            self.stumps.append(stump)

    '''
    classify an unknown piece of data given a Datum
    '''
    def classify(self, unknown):
        en = 0
        nl = 0

        for s in self.stumps:
            p = s.classify(unknown)

            if p == 'en':
                en += 1 * s.root.weight
            elif p == 'nl':
                nl += 1 * s.root.weight

        if en > nl:
            return 'en'
        elif nl >= en:
            return 'nl'
