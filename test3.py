import pickle
count = 0
with open('runCount.pkl', 'wb') as file:
    pickle.dump(count, file)