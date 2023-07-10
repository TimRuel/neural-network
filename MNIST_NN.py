import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data/train.csv")

data = np.array(data)
m, n = data.shape
np.random.shuffle(data)

data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]
X_dev = X_dev / 255.

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.
_, m_train = X_train.shape

def init_params():
  W1 = np.random.rand(10, 784) - 0.5 # 10 rows, 784 columns
  b1 = np.random.rand(10, 1) - 0.5 # 10 rows, 1 column
  W2 = np.random.rand(10, 10) - 0.5 # 10 rows, 10 columns
  b2 = np.random.rand(10, 1) - 0.5 # 10 rows, 1 column
  return W1, b1, W2, b2

def ReLU(Z):
  return np.maximum(Z, 0)

def softmax(Z):
  A = np.exp(Z) / np.sum(np.exp(Z), 0)
  return A

def forward_prop(W1, b1, W2, b2, X):
  Z1 = W1.dot(X) + b1 # 10 rows, m columns
  A1 = ReLU(Z1) # 10 rows, m columns
  Z2 = W2.dot(A1) + b2 # 10 rows, m columns
  A2 = softmax(Z2) # 10 rows, m columns
  return Z1, A1, Z2, A2
  
def one_hot(Y):
  one_hot_Y = np.zeros((Y.size, Y.max() + 1))
  one_hot_Y[np.arange(Y.size), Y] = 1
  one_hot_Y = one_hot_Y.T
  return one_hot_Y
  
def deriv_ReLU(Z):
  return Z > 0

def back_prop(Z1, A1, A2, W2, X, Y): 
  m = Y.size
  one_hot_Y = one_hot(Y) # 10 rows, m columns
  dZ2 = A2 - one_hot_Y # 10 rows, m columns
  dW2 = 1 / m * dZ2.dot(A1.T) # 10 rows, 10 columns
  db2 = 1 / m * np.sum(dZ2, 1, keepdims = True) # 10 rows, 1 column
  dZ1 = W2.T.dot(dZ2) * deriv_ReLU(Z1) # 10 rows, m columns
  dW1 = 1 / m * dZ1.dot(X.T) # 10 rows, 784 columns
  db1 = 1 / m * np.sum(dZ1, 1, keepdims = True) # 10 rows, 1 column
  return dW1, db1, dW2, db2
  
def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
  W1 = W1 - alpha * dW1
  b1 = b1 - alpha * db1
  W2 = W2 - alpha * dW2
  b2 = b2 - alpha * db2
  return W1, b1, W2, b2

def get_predictions(A2):
  return np.argmax(A2, 0)

def get_accuracy(predictions, Y):
  print(predictions, Y)
  return np.sum(predictions == Y) / Y.size

def gradient_descent(X, Y, iterations, alpha):
  W1, b1, W2, b2 = init_params()
  for i in range(iterations):
    Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
    dW1, db1, dW2, db2 = back_prop(Z1, A1, A2, W2, X, Y)
    W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)
    if i % 50 == 0:
      print("Iteration: ", i)
      print("Accuracy: ", get_accuracy(get_predictions(A2), Y))
  return W1, b1, W2, b2

W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 500, 0.1)

def make_predictions(X, W1, b1, W2, b2):
  _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
  predictions = get_predictions(A2)
  return predictions

def test_prediction(index, W1, b1, W2, b2):
  current_image = X_train[:, index, None]
  prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
  label = Y_train[index]
  print("Prediction: ", prediction)
  print("Label: ", label)
  
  current_image = current_image.reshape((28, 28)) * 255
  plt.gray()
  plt.imshow(current_image, interpolation = "nearest")
  plt.show()

test_prediction(1562, W1, b1, W2, b2)

dev_predictions = make_predictions(X_dev, W1, b1, W2, b2)
get_accuracy(dev_predictions, Y_dev)
