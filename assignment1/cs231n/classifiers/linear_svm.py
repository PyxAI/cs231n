import numpy as np
from random import shuffle
from past.builtins import xrange

def svm_loss_naive(W, X, y, reg):
  """
  Structured SVM loss function, naive implementation (with loops).

  Inputs have dimension D, there are C classes, and we operate on minibatches
  of N examples.

  Inputs:
  - W: A numpy array of shape (D, C) containing weights.
  - X: A numpy array of shape (N, D) containing a minibatch of data.
  - y: A numpy array of shape (N,) containing training labels; y[i] = c means
    that X[i] has label c, where 0 <= c < C.
  - reg: (float) regularization strength

  Returns a tuple of:
  - loss as single float
  - gradient with respect to weights W; an array of same shape as W
  """
  dW = np.zeros(W.shape) # initialize the gradient as zero

  # compute the loss and the gradient
  num_classes = W.shape[1] #10
  num_train = X.shape[0] #(500)
  loss = 0.0
  for i in xrange(num_train):
    scores = X[i].dot(W) #[1 * 3072] * [3072 * 10] = [1 * 10]
    correct_class_score = scores[y[i]] #just the score for the correct class, the y[i] returns the position of the correct score
    for j in xrange(num_classes):
      if j == y[i]:
        continue
      margin = scores[j] - correct_class_score + 1 # note delta = 1
      if margin > 0:
        loss += margin
        dW[:,y[i]]-=X[i,:]
        dW[:,j]+=X[i,:]


  #X.dot(W) # (500 * 3072) * (3072 * 10) = [500 * 10]
  # Right now the loss is a sum over all training examples, but we want it
  # to be an average instead so we divide by num_train.
  loss /= num_train
  dW=dW/num_train
  # Add regularization to the loss.
  loss += reg * np.sum(W * W)
  dW+=W*reg
  #############################################################################
  # TODO:                                                                     #
  # Compute the gradient of the loss function and store it dW.                #
  # Rather that first computing the loss and then computing the derivative,   #
  # it may be simpler to compute the derivative at the same time that the     #
  # loss is being computed. As a result you may need to modify some of the    #
  # code above to compute the gradient.                                       #
  #############################################################################


  return loss, dW

#DEBUGGING METHOD!!

'''

import pdb; pdb.set_trace()

'''
def svm_loss_vectorized(W, X, y, reg):
  """
  Structured SVM loss function, vectorized implementation.

  Inputs and outputs are the same as svm_loss_naive.
  """
  loss = 0.0
  dW = np.zeros(W.shape) # initialize the gradient as zero
  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the structured SVM loss, storing the    #
  # result in loss.                                                           #
  #############################################################################
  dots=X.dot(W)
  cs=dots[range(dots.shape[0]),y]
  margins = np.maximum(0, dots - np.matrix(cs).T + 1)
  margins[np.arange(X.shape[0]),y] = 0
  loss=np.sum(margins)/X.shape[0]
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################
  binary=margins
  binary[margins>0]=1
  row_sum = np.sum(binary, axis=1)
  binary[np.arange(X.shape[0]), y] = -row_sum.T
  dW = np.dot(X.T, binary)
  dW /= X.shape[0]
  dW += reg*W

  #############################################################################
  # TODO:                                                                     #
  # Implement a vectorized version of the gradient for the structured SVM     #
  # loss, storing the result in dW.                                           #
  #                                                                           #
  # Hint: Instead of computing the gradient from scratch, it may be easier    #
  # to reuse some of the intermediate values that you used to compute the     #
  # loss.                                                                     #
  #############################################################################
  pass
  #############################################################################
  #                             END OF YOUR CODE                              #
  #############################################################################

  return loss, dW
