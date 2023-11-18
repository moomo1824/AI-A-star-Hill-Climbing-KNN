import math
import csv
import pandas as pd
import matplotlib.pyplot as plt

dataset_file = "./dataset.csv"
mark_records = []

min_marks = {
    "Assignment-1": 100,
    "Assignment-2": 100,
    "Assignment-3": 100,
    "Assignment-4": 100,
    "Assignment-5": 100,
    "Final": 100,
    "Mid": 100,
}

max_marks = {
    "Assignment-1": -100,
    "Assignment-2": -100,
    "Assignment-3": -100,
    "Assignment-4": -100,
    "Assignment-5": -100,
    "Final": -100,
    "Mid": -100,
}

def load_min_max(df):
    for k in min_marks:
        min_marks[k] = min(df.loc[:, k])
        max_marks[k] = max(df.loc[:, k])

def get_normalized_entry(row):
    result = []
    result.append((row[0] - min_marks["Assignment-1"]) / (max_marks["Assignment-1"] - min_marks["Assignment-1"]))
    result.append((row[1] - min_marks["Assignment-2"]) / (max_marks["Assignment-2"] - min_marks["Assignment-2"]))
    result.append((row[2] - min_marks["Assignment-3"]) / (max_marks["Assignment-3"] - min_marks["Assignment-3"]))
    result.append((row[3] - min_marks["Assignment-4"]) / (max_marks["Assignment-4"] - min_marks["Assignment-4"]))
    result.append((row[4] - min_marks["Assignment-5"]) / (max_marks["Assignment-5"] - min_marks["Assignment-5"]))
    result.append((row[5] - min_marks["Final"]) / (max_marks["Final"] - min_marks["Final"]))
    result.append((row[6] - min_marks["Mid"]) / (max_marks["Mid"] - min_marks["Mid"]))
    return result

df = pd.read_csv(dataset_file)
load_min_max(df)

for row in range(len(df)):
    current_record = list(df.loc[row, :])
    current_record_updated = [current_record[0]]
    current_record_updated.extend(get_normalized_entry(current_record[1: len(current_record) - 1]))
    current_record_updated.append(current_record[-1])
    mark_records.append(current_record_updated)

def euclidean_distance(row1, row2):
    if len(row1) != len(row2):
        return None
    ret_val = 0
    for idx, item in enumerate(row1):
        ret_val += (row1[idx] - row2[idx]) ** 2
    return math.sqrt(ret_val)

def get_accuracy(true_output, predicted_output):
    correct = 0
    for idx, outcome in enumerate(true_output):
        if predicted_output[idx] == outcome:
            correct += 1
    return correct / len(true_output) * 100

# Split the dataset into training, validation, and testing sets
training_size = int(len(mark_records) * 0.8)
validation_size = int(len(mark_records) * 0.1)

training = mark_records[:training_size]
validation = mark_records[training_size:training_size + validation_size]
testing = mark_records[training_size + validation_size:]

# Define the k values to test
k_values_to_test = [1, 3, 5, 7]

# Initialize lists to store k values and their corresponding accuracies
k_values = []
accuracies = []

# Initialize best_accuracy outside the loop
best_accuracy = 0

# Find the best k value using the validation set
for k in k_values_to_test:
    predicted_output = []

    for entry in validation:
        dist_vector = []

        for compare_entry in training:
            if entry != compare_entry:
                sample1 = entry[1: -1]
                sample2 = compare_entry[1: -1]
                dist_vector.append((euclidean_distance(sample1, sample2), compare_entry[-1]))

        dist_vector.sort(key=lambda x: x[0])
        # For k neighbors, take the majority class
        top_k_classes = [x[1] for x in dist_vector[:k]]
        predicted_output.append(max(set(top_k_classes), key=top_k_classes.count))

    true_output = [entry[-1] for entry in validation]
    accuracy = get_accuracy(true_output, predicted_output)

    print(f"For k={k}, accuracy on validation set: {accuracy}%")

    # Append values to lists for visualization
    k_values.append(k)
    accuracies.append(accuracy)

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_k_value = k

print(f"The best k value is {best_k_value} with accuracy {best_accuracy}% on the validation set.")

# Plotting the results
plt.plot(k_values, accuracies, marker='o')
plt.title('Validation Accuracy vs. K Value')
plt.xlabel('K Value')
plt.ylabel('Accuracy (%)')
plt.show()

# Evaluate accuracy on the testing set with the best k
predicted_output_test = []

for entry_test in testing:
    dist_vector_test = []

    for compare_entry_test in training:
        sample1_test = entry_test[1: -1]
        sample2_test = compare_entry_test[1: -1]
        dist_vector_test.append((euclidean_distance(sample1_test, sample2_test), compare_entry_test[-1]))

    dist_vector_test.sort(key=lambda x: x[0])
    # For k neighbors, take the majority class
    top_k_classes_test = [x[1] for x in dist_vector_test[:best_k_value]]
    predicted_output_test.append(max(set(top_k_classes_test), key=top_k_classes_test.count))

true_output_test = [entry_test[-1] for entry_test in testing]
accuracy_test = get_accuracy(true_output_test, predicted_output_test)

print(f"Accuracy on the testing set with the best k ({best_k_value}): {accuracy_test}%")
