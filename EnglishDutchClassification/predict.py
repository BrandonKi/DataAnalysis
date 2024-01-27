from common import *
from train import *

def main():
    model = pickle.load(open(sys.argv[1], 'rb'))

    # print(model.classify(Datum('', 'root node. There are many specific decision-tree algorithms. Notable ones include: While the Yale shooting')))

    for w in open(sys.argv[2],'r').read().split('\n'):
        if len(w) == 0:
            continue
        r = model.classify(Datum('', w))
        # print(r, w)
        print(r)

if __name__ == '__main__':
    main()