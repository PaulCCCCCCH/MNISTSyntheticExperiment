import pickle
from models import LeNet, load_model
import torch
from args import *
import numpy as np
from data_utils import get_standard_mnist_dataset

train, dev, test = get_standard_mnist_dataset(os.path.join(args.data_dir, 'mnist.pkl'), args.batch_size)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

lenet = LeNet()
lenet.to(device)

state_dict = load_model(args)
lenet.load_state_dict(state_dict)

# Testing
correct = 0
total = 0
with torch.no_grad():
    for inputs_batch, labels_batch in test:
        inputs = inputs_batch.to(device)
        labels = labels_batch.to(device)

        outputs = lenet(inputs)
        _, predicted = torch.max(outputs.data, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

print('Correct predictions: {} of {}'.format(correct, total))
print('Accuracy of the network on 10000 standard test images: {}'.format(correct / total))
