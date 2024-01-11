import pandas as pd
import math

def entropy(data):
    value_counts = data.value_counts()
    probabilities = value_counts / len(data)
    entropy_value = -sum(p * math.log2(p) for p in probabilities)
    return entropy_value

def information_gain(data, feature, target):
    return entropy(data[target]) - sum(
        len(subset) / len(data) * entropy(subset[target]) for _, subset in data.groupby(feature)
    )

def construct_tree(data, target, features):
    if len(set(data[target])) == 1:
        return data[target].iloc[0]
    if not features:
        return data[target].mode().iloc[0]
    best_feature = max(features, key=lambda f: information_gain(data, f, target))
    tree = {best_feature: {}}
    for value, subset in data.groupby(best_feature):
        subset = subset.drop(columns=[best_feature])
        tree[best_feature][value] = construct_tree(subset, target, features - {best_feature})
    return tree

def print_tree(tree, indent=""):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print(indent + key)
            print_tree(value, indent + " ")
    else:
        print(indent + f"=> {tree}")

def predict(tree, instance):
    if not isinstance(tree, dict):
        return tree
    feature = next(iter(tree))
    value = instance[feature]
    if value not in tree[feature]:
        return None
    subtree = tree[feature][value]
    return predict(subtree, instance)

def calculate_accuracy(tree, data, target):
    predictions = data.apply(lambda instance: predict(tree, instance), axis=1)
    correct_predictions = predictions == data[target]
    accuracy = correct_predictions.mean()
    return accuracy

def main():
    # Load dataset from playtennis.csv
    df = pd.read_csv("C:\playtennis.csv")
    # Extract target and features
    target_column = "Play Tennis"
    features = set(df.columns) - {target_column}
    # Construct the decision tree
    tree = construct_tree(df, target=target_column, features=features)
    # Print the decision tree
    print_tree(tree)
    # Calculate prediction accuracy
    accuracy = calculate_accuracy(tree, df, target_column)
    print(f"Prediction Accuracy: {accuracy}")

if __name__ == "__main__":
    main()
