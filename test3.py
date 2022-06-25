import pickle
with open('runCount.pkl', 'rb') as file:
    count = pickle.load(file)
count += 1
print("{} runs completed".format(str(count)))