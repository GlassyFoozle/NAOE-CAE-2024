import random
import pandas as pd
import numpy as np


# 데이터 불러오기
data = pd.read_csv('data2_minimized_r6.csv', encoding='cp949')
y = data['Accident_Type']
acc_types= y.drop_duplicates()
acc_types = acc_types.values.tolist()
print(acc_types)
num_choices = 3
acc_types = y.value_counts()
total_count = acc_types.sum()
probabilities = acc_types / total_count
index_list = probabilities.index.tolist()
probability_list = probabilities.tolist()
chosen_values = random.choices(index_list, weights=probability_list, k=num_choices)
tot_num=y.shape[0]
randoms=[]
for _ in range(tot_num):
    selected_numbers = random.choices(index_list, weights=probability_list, k=num_choices)
    randoms.append(selected_numbers)

success = [1 if y[i] in randoms[i] else 0 for i in range(len(y))]
accuracy = np.mean(success)
print(accuracy)