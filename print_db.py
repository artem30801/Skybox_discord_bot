import pickle
import os
import pprint

database = 'database.txt'
with open(os.path.abspath(database), 'rb') as f:
    arcs, data = pickle.load(f)


pprint.pprint(arcs)
pprint.pprint(data)
