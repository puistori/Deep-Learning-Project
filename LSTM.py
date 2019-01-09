# -*- coding: utf-8 -*-
"""
Created on Tue Dec  4 09:15:35 2018

@author: samst
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import gensim.downloader as api
import os


########## Data Processing Starts ##########

info = api.info()
model = api.load("glove-twitter-25")

dataset = list()

for filename in os.listdir(r'C:\Users\samst\Desktop\LIGN Project\Movies2vec\test'):

    if filename.endswith('.txt'):
        with open(filename) as movie_in:
            file = movie_in.read().split()

            movie_word_vectors = list()


            for word in file:
                try:
                    movie_word_vectors.append(model[word])
                except:
                    pass

        dataset.append(movie_word_vectors)

        continue
    else:
        continue

movie_dataset = dict()

for index in range(len(dataset)):
    movie_dataset[index] = torch.tensor(dataset[index])

target_dataset = {0:[8], 1:[6], 2:[7], 3:[7]}


########## Data Processing Ends ##########



########## LSTM Model Definition Start ##########

INPUT_DIM = 25
HIDDEN_DIM = 50
OUTPUT_DIM = 10
num_layers = 1


class LSTM(nn.Module):
    
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super(LSTM, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # Holds word_vectors for a certain movie
        # self.word_vectors = word_vectors

        # LSTM creator with input_size, hidden_size 
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim)

        # Linear layer mapping hidden state to out space
        self.hidden2out = nn.Linear(hidden_dim, output_dim)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        # Dimensions are (num_layers, minibatch_size, hidden_dim)
        return (torch.zeros(self.num_layers, 1, self.hidden_dim),
                torch.zeros(self.num_layers, 1, self.hidden_dim))
    
    def forward(self, W2V):
        inputs = W2V
        lstm_out, self.hidden = self.lstm(
                inputs.view(len(inputs), 1, -1), self.hidden)
        output_space = self.hidden2out(lstm_out.view(len(inputs), -1))

        return output_space
    
    def __str__(self):
        return "LSTM created"

########## LSTM Definition End ##########



########## Training Start ##########

lstm = LSTM(INPUT_DIM, HIDDEN_DIM, OUTPUT_DIM, num_layers)
loss_function = nn.CrossEntropyLoss()
optimizer = optim.SGD(lstm.parameters(), lr=.02)

with torch.no_grad():
    inputs = movie_dataset[0]
    test = lstm(inputs)
    print("This is our starting output")
    print(test)

for epoch in range(10):
    for index in range(len(movie_dataset)):
        # Zeros the gradient before each instance
        lstm.zero_grad()

        # Clears out the hidden states of the LSTM
        lstm.hidden = lstm.init_hidden()
        
        # Define target vectors
        target_data = target_dataset[index]
        target = torch.tensor(target_data, dtype=torch.long)
        
        # Run forward pass
        output_scores = lstm(movie_dataset[index])[-1].view(-1,10)

        # Compute loss, gradients, and update parameters
        loss = loss_function(output_scores, target)
        print("\nFollowing is loss:")
        print(loss)
        loss.backward()
        optimizer.step()
        
with torch.no_grad():
    for index in range(len(movie_dataset)):
        inputs = movie_dataset[index]
        test = lstm(inputs)
        
        print("\nThis is the last item")
        print(test[-1])


########## Training ENDS ##########
        