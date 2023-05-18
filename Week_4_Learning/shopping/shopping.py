import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence = []
    labels = []
    # Read data in from file
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader) # discount the header row
        
        for row in reader:            
            processed_row = row[:-1]
            
            # Administrative, an integer
            processed_row[0] = int(processed_row[0])
            
            # Administrative_Duration, a floating point number
            processed_row[1] = float(processed_row[1])
            
            # Informational, an integer
            processed_row[2] = int(processed_row[2])
            
            # Informational_Duration, a floating point number
            processed_row[3] = float(processed_row[3])
            
            # ProductRelated, an integer
            processed_row[4] = int(processed_row[4])
            
            # ProductRelated_Duration, a floating point number
            processed_row[5] = float(processed_row[5])
            
            # BounceRates, a floating point number
            processed_row[6] = float(processed_row[6])
        
            # ExitRates, a floating point number
            processed_row[7] = float(processed_row[7])
        
            # PageValues, a floating point number
            processed_row[8] = float(processed_row[8])
        
            # SpecialDay, a floating point number
            processed_row[9] = float(processed_row[9])
            
            # Month, an index from 0 (January) to 11 (December)
            month_name = processed_row[10]
            if month_name == "Jan":
                processed_row[10] = int(0)
            elif month_name == "Feb":
                processed_row[10] = int(1)
            elif month_name == "Mar":
                processed_row[10] = int(2)
            elif month_name == "Apr":
                processed_row[10] = int(3)
            elif month_name == "May":
                processed_row[10] = int(4)
            elif month_name == "June":
                processed_row[10] = int(5)
            elif month_name == "Jul":
                processed_row[10] = int(6)
            elif month_name == "Aug":
                processed_row[10] = int(7)
            elif month_name == "Sep":
                processed_row[10] = int(8)
            elif month_name == "Oct":
                processed_row[10] = int(9)
            elif month_name == "Nov":
                processed_row[10] = int(10)
            elif month_name == "Dec":
                processed_row[10] = int(11)
            else:
                processed_row[10] = None
             
            # OperatingSystems, an integer
            processed_row[11] = int(processed_row[11])
            
            # Browser, an integer
            processed_row[12] = int(processed_row[12])
        
            # Region, an integer
            processed_row[13] = int(processed_row[13])
        
            # TrafficType, an integer
            processed_row[14] = int(processed_row[14])
            
            # VisitorType, an integer 0 (not returning) or 1 (returning)
            if processed_row[15] == "Returning_Visitor": 
                processed_row[15] = int(1)
            else:
                processed_row[15] = int(0)
            
            # Weekend, an integer 0 (if false) or 1 (if true)
            if processed_row[16] == True:
                processed_row[16] = int(1)
            else:
                processed_row[16] = int(0)
                
            evidence.append(processed_row)
            
            # labels should be the corresponding list of labels, where each label
            # is 1 if Revenue is true, and 0 otherwise.
            label_row = row[-1]
            if label_row == "TRUE":
                label_row = int(1)
            else:
                label_row = int(0)
            labels.append(label_row)
            
    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # define model
    model = KNeighborsClassifier(n_neighbors=1)
    
    # Fit model
    model.fit(evidence, labels)
    
    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Compute true_negative, true_positive, false_negative, false_positive
    false_negative = 0.0
    false_positive = 0.0
    true_negative = 0.0
    true_positive = 0.0
    
    for prediction, label in zip(predictions, labels):
        if prediction == 0 and label == 0:
            true_negative += 1.0
        if prediction == 0 and label == 1:
            false_negative += 1.0
        if prediction == 1 and label == 0:
            false_positive += 1.0
        if prediction == 1 and label == 1:
            true_positive += 1.0
    
    # compute sensitivity and specitivity
    sensitivity = true_positive/ (true_positive + false_negative)
    specificity = true_negative/ (false_positive + true_negative)
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
