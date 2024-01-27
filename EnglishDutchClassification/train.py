import sys
import pickle

from common import *

def run_on_test_set(dt):
    test_data = open('data/test_set.dat','r', encoding='utf-8').read().split('\n')
    # test_data = open('data/large_train.dat','r', encoding='utf-8').read().split('\n')
    # test_data = open('data/small_train.dat','r', encoding='utf-8').read().split('\n')
    correct = 0
    for w in test_data:
        w = w.split('|')
        r = dt.classify(Datum(w[0], w[1]))
        if r == w[0]:
            correct += 1
    print(f'Correct: {correct/len(test_data)*100}%')

def main():
    if len(sys.argv) < 3:
        print('train <examples> <hypothesisOut> <learning-type>')
        sys.exit()

    data = [Datum(x.split('|')[0], x.split('|')[1]) for x in open(sys.argv[1], 'r', encoding='utf-8').read().split('\n')]
    hypothesisOut = sys.argv[2]
    learningTypes = sys.argv[3]

    model = None
    if learningTypes == 'dt':
        model = DecisionTreeModel()
    elif learningTypes == 'ada':
        model = AdaBoostModel()
    
    model.train_model(data)
    # run_on_test_set(model)
    pickle.dump(model, open(hypothesisOut, 'wb'))


if __name__ == '__main__':
    main()