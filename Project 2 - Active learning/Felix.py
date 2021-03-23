
import torch
import torchvision.transforms as transforms
import torchvision.datasets as datasets
import torchvision.models as models
import torch.nn as nn
import torch.optim as optim
import numpy as np
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import sklearn.linear_model as lin
import idx2numpy



#data = datasets.FashionMNIST(root="Project 2 - Active learning", download=True)
#print(data)

os.chdir('/Users/christiandjurhuus/PycharmProjects/Active_ML_and_Agency/Project 2 - Active learning/Project 2 - Active learning/FashionMNIST/raw')
#Getting file paths
file_train = 'train-images-idx3-ubyte'
file_test = 't10k-images-idx3-ubyte'
file_train_label = 'train-labels-idx1-ubyte'
file_test_label = 't10k-labels-idx1-ubyte'

#Creating numpy arrays
arr_train = idx2numpy.convert_from_file(file_train)
arr_train_label = idx2numpy.convert_from_file(file_train_label)
arr_test = idx2numpy.convert_from_file(file_test)
arr_test_label = idx2numpy.convert_from_file(file_test_label)



#cv.imshow("Image", arr[4], )
#plt.imshow(arr_train[4], cmap='gray')
#plt.show()

#Making subsample
#Xtrain = arr_train[:9000]
#ytrain = arr_train_label[:9000]


X = arr_test
y = arr_test_label

#Creating pools for pool based active learning
Xtest = X[5000:].reshape(5000,784)
ytest = y[5000:]
Xpool = X[:5000].reshape(5000,784)
ypool = y[:5000]

#Visualizing a subsample of the data
def show_image(x, title="", clim=None, cmap=plt.cm.gray, colorbar=False):
    ax = plt.gca()
    im = ax.imshow(x.reshape((28, 28)), cmap=cmap, clim=clim)

    if len(title) > 0:
        plt.title(title)

    plt.axis('off')

    if colorbar:
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)
        plt.colorbar(im, cax=cax)

num_images_per_row = 6
num_rows = 3
num_images = num_images_per_row * num_rows

plt.figure(figsize=(20, 8))
for i in range(num_images):
    plt.subplot(num_rows, num_images_per_row, 1 + i)
    show_image(Xtest[i, :])
plt.show()



#Defining model
lr = lin.LogisticRegression(penalty='l2',C=1.)


addn = 2 #samples to add each time
#randomize order of pool to avoid sampling the same subject sequentially
np.random.seed(0)
order = np.random.permutation(range(len(Xpool)))
#samples in the poolx
poolidx=np.arange(len(Xpool),dtype=int)
ninit = 10 #initial samples
#initial training set
trainset=order[:ninit]
print(trainset)
Xtrain=np.take(Xpool,trainset,axis=0)
ytrain=np.take(ypool,trainset,axis=0)
#remove data from pool
poolidx=np.setdiff1d(poolidx,trainset)

model=lr
testacc=[]

for i in range(25):
    #Fit model
    model.fit(Xtrain, ytrain)
    #predict on test set
    ye = model.predict(Xtest)
    #calculate and accuracy and add to list
    testacc.append((ninit+i*addn, sklearn.metrics.accuracy_score(ytest, ye)))
    print('Model: LR, %i random samples'%(ninit+i*addn))
'''












