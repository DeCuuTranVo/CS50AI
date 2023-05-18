# **Project 5: Traffic - CS50’s Introduction to Artificial Intelligence with Python**

## **I. Background and Project Goal**
Autonomous vehicles are cars that can operate themselves. Those cars collect and analyze information about their surrounding environments through cameras and other sensors for later decision-making processes. One problem of self-driving systems is traffic sign recognition and categorization. For example, mandatory and cautionary signs need to be detected to avoid traffic tickets and accidents.

In this project, the task is to use the TensorFlow framework to build a (convolutional) neural network to distinguish different types of road signs utilizing digital images from cameras.

## **II. Code Flow & Project Structure**
In this project, the dataset is stored in a folder named <code> gtsrb </code>. This folder consists of multiple directories with numerical names corresponding to different classes. In each of those directories, multiple image files with the respective label are stored.

The file <code> traffic.py </code> has three functions: <code>main</code>, <code>load_data</code>, and <code>get_model</code>. The <code>main</code> function calls <code>load_data</code> to read image files, attach to each image its label, and return two sequences of images and labels with the correct order (of samples). Then, the <code>main</code> function transforms the integer label list into a binary class matrix. After that, the <code>main</code> function splits the dataset between the training set and the testing set. Afterward, this function calls the <code>get_model</code> function to get the model with its structure, learning rate, loss function, and metrics. Subsequently, the <code>main</code> function calls the <code>model.fit</code> method on training images and training labels in order to train the model. Finally, the <code>main</code> function calls the <code>model.evaluate</code> method on testing images and testing label to compute the model's performance before saving the model.

## **III. Experiments**
Besides parameters that can be learned through gradient descent algorithms, there are hyperparameters that control the model's structure and learning processes, including the number of convolutional layers, the number of filters in convolutional layers, the number of hidden layers, the number of units in hidden layers, dropout, and so on. Those hyperparameters need to be chosen before the training process takes place. Thus, multiple experiments are necessary to discover a nearly optimal hyperparameter configuration for this classification problem.

In my experiments, the method of choice is described below:

    Choose a random hyperparameter configuration
    For each hyperparameter:
        List some possible values for that hyperparameter
        For each value in the list:
            Train the model with that hyperparameter's chosen value
            Evaluate and record the performance
        Choose the hyperparameter value with the best model's performance for the current hyperparameter.

        If the accuracy on the test set >= 99%:
            Return this configuration

    Return this configuration

The chosen search domains for each hyperparameter are:

    {
        Number of convolutional layers: [0,1,2,3]
        Number of filters in each convolutional layer: [8, 16, 32, 64, 128]
        Number of hidden layers: [0, 1, 2, 3]
        Number of units in each hidden layer: [8, 16, 32, 64, 128]
        Dropout rate: [0.1, 0.3, 0.5, 0.7, 0.9]
    }

The initial random configuration is:

    {
        Number of convolutional layers: 1
        Number of filters in each convolutional layer: 32
        Number of hidden layers: 1
        Number of units in each hidden layer: 32
        Dropout rate: 0.5
    }

Note that to get a sufficiently good result for each specified configuration, I train the respective model for 20 EPOCHS. Training time and the number of parameters are also recorded for each configuration.

In the following tables, "hidden layer" means "hidden dense layer."

### **III.1. Experiment 1**: Choose the number of convolutional layers in [0, 1, 2, 3]
| Number of convolutional layer | # Convolutional Filters per layer | # Hidden layers | # Units per hidden layer | Dropout rate | Train Accuracy | Test Accuracy | #Params| Training Time (seconds) |
| ----------------------------- | --------------------------------- | --------------- | ------------------------ | ------------ | -------------- | ------------- | ------ | -------------           |
| 0                             | 32                                | 1               |  32                      | 0.5          | 0.0921         |  0.1403       | 87,851 | 22.33                   |
| 1                             | 32                                | 1               |  32                      | 0.5          | 0.3462         |  0.7088       | 203,051| 33.39                   |
| 2                             | 32                                | 1               |  32                      | 0.5          | 0.6593         |  0.9261       | 48,459 | 49.48                   |
| 3                             | 32                                | 1               |  32                      | 0.5          | 0.8188         |  0.9447       | 24,939 | 51.25                   |

**Comment 1**: With 3 convolutional layers, the model gives the best test accuracy at 94.47%. Therefore, I fix this hyperparameter assignment and then experiment with other hyperparameters.

### **III.2. Experiment 2**: Choose the number of filters for each convolutional layer in [8, 16, 32, 64, 128]
| Number of convolutional layer | # Convolutional Filters per layer | # Hidden layers | # Units per hidden layer | Dropout rate | Train Accuracy | Test Accuracy | #Params| Training Time (seconds) |
| ----------------------------- | --------------------------------- | --------------- | ------------------------ | ------------ | -------------- | ------------- | ------ | -------------           |
| 3                             | 8                                 | 1               |  32                      | 0.5          | 0.6172         | 0.7810        | 3,867  | 35.85                   |
| 3                             | 16                                | 1               |  32                      | 0.5          | 0.7836         | 0.9280        | 8,587  | 37.56                   |
| 3                             | 32                                | 1               |  32                      | 0.5          | 0.8370         | 0.9626        | 24,939 | 52.3                    |
| 3                             | 64                                | 1               |  32                      | 0.5          | 0.7691         | 0.9604        | 85,291 | 95.83                   |
| 3                             | 128                               | 1               |  32                      | 0.5          | 0.8689         | 0.9875        | 316,587| 197.47                  |

**Comment 2**: With 128 filters per convolutional layer, the best test accuracy is achieved at 98.75%. Therefore, I fix this hyperparameter assignment and then experiment with other hyperparameters.

### **III.3. Experiment 3**: Choose the number of hidden layers in [0, 1, 2, 3]
| Number of convolutional layer | # Convolutional Filters per layer | # Hidden layers | # Units per hidden layer | Dropout rate | Train Accuracy | Test Accuracy | #Params| Training Time (seconds) |
| ----------------------------- | --------------------------------- | --------------- | ------------------------ | ------------ | -------------- | ------------- | ------ | -------------           |
| 3                             | 128                               | 0               |  32                      | 0.5          | 0.9847         | 0.9947        | 320,811| 198.98                  |
| 3                             | 128                               | 1               |  32                      | 0.5          | 0.7694         | 0.9601        | 316,587| 196.69                  |
| 3                             | 128                               | 2               |  32                      | 0.5          | 0.5570         | 0.7253        | 317,643| 197.04                  |
| 3                             | 128                               | 3               |  32                      | 0.5          | 0.4339         | 0.5042        | 318,699| 196.86                  |

**Comment 3**: With 0 hidden dense layers, the model produces the best test accuracy with 99.47%. Therefore, I fix this hyperparameter assignment. *Because the result is already satisfied, there is no further need to tune dropout and number of units per hidden layer.*


## **IV. Results**
### **IV.1. Optimized hyperparameter configuration**
    {
        Number of convolutional layers: 3
        Number of filters in each convolutional layer: 128
        Number of hidden layers: 0
        Number of units in each hidden layer: 32
        Dropout rate: 0.5
    }

### **IV.2. Model Architecture**
    Model: "model"
    _________________________________________________________________
    Layer (type)                Output Shape              Param #   
    =================================================================
    input_1 (InputLayer)        [(None, 30, 30, 3)]       0         
                                                                    
    conv2d (Conv2D)             (None, 28, 28, 128)       3584      
                                                                    
    max_pooling2d (MaxPooling2D  (None, 14, 14, 128)      0         
    )                                                               
                                                                    
    conv2d_1 (Conv2D)           (None, 12, 12, 128)       147584    
                                                                    
    max_pooling2d_1 (MaxPooling  (None, 6, 6, 128)        0         
    2D)                                                             
                                                                    
    conv2d_2 (Conv2D)           (None, 4, 4, 128)         147584    
                                                                    
    max_pooling2d_2 (MaxPooling  (None, 2, 2, 128)        0         
    2D)                                                             
                                                                    
    flatten (Flatten)           (None, 512)               0         
                                                                    
    dropout (Dropout)           (None, 512)               0         
                                                                    
    dense (Dense)               (None, 43)                22059     
                                                                    
    =================================================================
    Total params: 320,811
    Trainable params: 320,811
    Non-trainable params: 0

### **IV.3. Performance**
    Epoch 1/20
    500/500 [==============================] - 10s 19ms/step - loss: 2.4674 - accuracy: 0.3208
    Epoch 2/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.7836 - accuracy: 0.7613
    Epoch 3/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.3862 - accuracy: 0.8798
    Epoch 4/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.2588 - accuracy: 0.9215
    Epoch 5/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.1978 - accuracy: 0.9403
    Epoch 6/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.1525 - accuracy: 0.9538
    Epoch 7/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.1318 - accuracy: 0.9610
    Epoch 8/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.1056 - accuracy: 0.9695
    Epoch 9/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0992 - accuracy: 0.9702
    Epoch 10/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0884 - accuracy: 0.9724
    Epoch 11/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0806 - accuracy: 0.9750
    Epoch 12/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0775 - accuracy: 0.9759
    Epoch 13/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.0696 - accuracy: 0.9782
    Epoch 14/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0616 - accuracy: 0.9809
    Epoch 15/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.0579 - accuracy: 0.9824
    Epoch 16/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0599 - accuracy: 0.9802
    Epoch 17/20
    500/500 [==============================] - 10s 19ms/step - loss: 0.0477 - accuracy: 0.9853
    Epoch 18/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.0478 - accuracy: 0.9848
    Epoch 19/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.0472 - accuracy: 0.9852
    Epoch 20/20
    500/500 [==============================] - 10s 20ms/step - loss: 0.0467 - accuracy: 0.9858
    333/333 - 2s - loss: 0.0227 - accuracy: 0.9950 - 2s/epoch - 5ms/step

## **V.Conclusion & Discussion**
From the experiment process, I derive a well-performed hyperparameter configuration with 3 convolutional layers, 128 filters in each convolutional layer, 0 hidden dense layers, 32 units per hidden dense layer, and a dropout rate of 0.5. The model trained with this configuration reaches 98.47% on the training set and 99.47% on the testing set. 
    
Through each experiment, I notice that: 
- The bigger the model is, the longer the training process takes place. (Experiment 1)
- For this problem, adding convolutional and pooling layers increases training and testing accuracy. (Experiment 2)
- For this problem, the model can have good results without hidden dense layers. (Experiment 3)