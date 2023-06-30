#!/usr/bin/env python
# coding: utf-8

import numpy as np
import torch
from torch import nn

class Encoder2(nn.Module):
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2):
        super().__init__()
        
    ### Linear section
        self.encoder_lin=nn.Sequential(
        nn.Linear(input_size, hidden_size_1),
        nn.ReLU(True),
        nn.Linear(hidden_size_1, hidden_size_2),
        nn.ReLU(True), 
        nn.Linear(hidden_size_2, latent_size),
        )
        
    def forward(self,x):
        x=self.encoder_lin(x)
        return x

class Decoder2(nn.Module):
    
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2):
        super().__init__()
        self.decoder_lin=nn.Sequential(
        nn.Linear(latent_size, hidden_size_2),
        nn.ReLU(True),
        nn.Linear(hidden_size_2, hidden_size_1),
        nn.ReLU(True), 
        nn.Linear(hidden_size_1, input_size),
        #nn.Sigmoid(),
        )
        
    def forward(self,x):
        x=self.decoder_lin(x)
        return x

class Encoder3(nn.Module):
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3):
        super().__init__()
        
    ### Linear section
        self.encoder_lin=nn.Sequential(
        nn.Linear(input_size, hidden_size_1),
        nn.ReLU(True),
        nn.Linear(hidden_size_1, hidden_size_2),
        nn.ReLU(True), 
        nn.Linear(hidden_size_2, hidden_size_3),
        nn.ReLU(True),
        nn.Linear(hidden_size_3, latent_size),
        )
        
    def forward(self,x):
        x=self.encoder_lin(x)
        return x

class Decoder3(nn.Module):
    
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3):
        super().__init__()
        self.decoder_lin=nn.Sequential(
        nn.Linear(latent_size, hidden_size_3),
        nn.ReLU(True), 
        nn.Linear(hidden_size_3, hidden_size_2),
        nn.ReLU(True),
        nn.Linear(hidden_size_2, hidden_size_1),
        nn.ReLU(True), 
        nn.Linear(hidden_size_1, input_size),
        nn.Sigmoid(),
        )
        
    def forward(self,x):
        x=self.decoder_lin(x)
        return x

class Encoder4(nn.Module):
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3,hidden_size_4):
        super().__init__()
        
    ### Linear section
        self.encoder_lin=nn.Sequential(
        nn.Linear(input_size, hidden_size_1),
        nn.ReLU(True),
        nn.Linear(hidden_size_1, hidden_size_2),
        nn.ReLU(True), 
        nn.Linear(hidden_size_2, hidden_size_3),
        nn.ReLU(True),
        nn.Linear(hidden_size_3, hidden_size_4),
        nn.ReLU(True), 
        nn.Linear(hidden_size_4, latent_size),
        )
        
    def forward(self,x):
        x=self.encoder_lin(x)
        return x

class Decoder4(nn.Module):
    
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3,hidden_size_4):
        super().__init__()
        self.decoder_lin=nn.Sequential(
        nn.Linear(latent_size, hidden_size_4),
        nn.ReLU(True),
        nn.Linear(hidden_size_4, hidden_size_3),
        nn.ReLU(True), 
        nn.Linear(hidden_size_3, hidden_size_2),
        nn.ReLU(True),
        nn.Linear(hidden_size_2, hidden_size_1),
        nn.ReLU(True), 
        nn.Linear(hidden_size_1, input_size),
        nn.Sigmoid(),
        )
        
    def forward(self,x):
        x=self.decoder_lin(x)
        return x

class Encoder7(nn.Module):
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3,hidden_size_4,hidden_size_5,hidden_size_6,hidden_size_7):
        super().__init__()
        
    ### Linear section
        self.encoder_lin=nn.Sequential(
        nn.Linear(input_size, hidden_size_1),
        nn.ReLU(True),
        nn.Linear(hidden_size_1, hidden_size_2),
        nn.ReLU(True), 
        nn.Linear(hidden_size_2, hidden_size_3),
        nn.ReLU(True),
        nn.Linear(hidden_size_3, hidden_size_4),
        nn.ReLU(True), 
        nn.Linear(hidden_size_4, hidden_size_5),
        nn.ReLU(True), 
        nn.Linear(hidden_size_5, hidden_size_6),
        nn.ReLU(True),
        nn.Linear(hidden_size_6, hidden_size_7),
        nn.ReLU(True), 
        nn.Linear(hidden_size_7, latent_size),
        )
        
    def forward(self,x):
        x=self.encoder_lin(x)
        return x

class Decoder7(nn.Module):
    
    def __init__(self,device,latent_size,input_size,hidden_size_1,hidden_size_2,hidden_size_3,hidden_size_4,hidden_size_5,hidden_size_6,hidden_size_7):
        super().__init__()
        self.decoder_lin=nn.Sequential(
        nn.Linear(latent_size, hidden_size_7),
        nn.ReLU(True),
        nn.Linear(hidden_size_7, hidden_size_6),
        nn.ReLU(True), 
        nn.Linear(hidden_size_6, hidden_size_5),
        nn.ReLU(True), 
        nn.Linear(hidden_size_5, hidden_size_4),
        nn.ReLU(True), 
        nn.Linear(hidden_size_4, hidden_size_3),
        nn.ReLU(True), 
        nn.Linear(hidden_size_3, hidden_size_2),
        nn.ReLU(True),
        nn.Linear(hidden_size_2, hidden_size_1),
        nn.ReLU(True), 
        nn.Linear(hidden_size_1, input_size),
        nn.Sigmoid(),
        )
        
    def forward(self,x):
        x=self.decoder_lin(x)
        return x

class simpleEncoder(nn.Module):
    def __init__(self,device,latent_size,input_size,HL):
        super().__init__()
        
        nb_L = len(HL)
        print('nb_L : {:d}'.format(nb_L))
        layers = []
        layers.append(nn.Linear(input_size, HL[0]))
        layers.append(nn.ReLU(True))
        for i in range(0, nb_L - 1):
            layers.append(nn.Linear(HL[i], HL[i+1]))
            layers.append(nn.ReLU(True))
        layers.append(nn.Linear(HL[nb_L - 1], latent_size))
    ### Linear section
        self.encoder_lin=nn.Sequential(*layers)
        #print(self.encoder_lin)
        
    def forward(self,x):
        x=self.encoder_lin(x)
        return x

class simpleDecoder(nn.Module):
    
    def __init__(self,device,latent_size,input_size,HL):
        super().__init__()

        nb_L = len(HL)
        layers = []
        layers.append(nn.Linear(latent_size, HL[nb_L - 1]))
        layers.append(nn.ReLU(True))
        for i in range(0, nb_L - 1):
            layers.append(nn.Linear(HL[nb_L - i - 1], HL[nb_L - i - 2]))
            layers.append(nn.ReLU(True))
        layers.append(nn.Linear(HL[0], input_size))
        #layers.append(nn.Sigmoid())
        self.decoder_lin=nn.Sequential(*layers)
        #print(self.decoder_lin)
        
    def forward(self,x):
        x=self.decoder_lin(x)
        return x

def train_epoch_den(encoder,decoder,device,dataloader,loss_fn,optimizer):
    encoder.train()
    decoder.train()
    train_loss=[]
    for item in dataloader: # "_" ignore labels
        #item = item.to(device)
        encoded_data=encoder(item) # .float()
        decoded_data=decoder(encoded_data)
        loss=loss_fn(decoded_data,item) # .float()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss.append(loss.detach()) # .cpu().numpy()
    train_loss = torch.tensor(train_loss) # .clone().detach()
    return torch.mean(train_loss), encoded_data[0]

def test_epoch_den(encoder,decoder,device,dataloader,loss_fn):
    encoder.eval()
    decoder.eval()
    with torch.no_grad(): # No need to track the gradients
        conc_out=[]
        conc_label=[]
        for item in dataloader:
            #item = item.to(device)
            encoded_data=encoder(item) 
            decoded_data=decoder(encoded_data)
            conc_out.append(decoded_data)
            conc_label.append(item) 
        conc_out=torch.cat(conc_out)
        conc_label=torch.cat(conc_label)
        test_loss=loss_fn(conc_out,conc_label)
    return test_loss.data, decoded_data, encoded_data

def train_epoch_den2(encoder,decoder,device,dataloader,loss_fn,optimizer):
    encoder.train()
    decoder.train()
    train_loss=[]
    for item in dataloader: # "_" ignore labels
        item = item.to(device)
        encoded_data=encoder(item) # .float()
        decoded_data=decoder(encoded_data)
        loss=loss_fn(decoded_data,item) # .float()
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        train_loss.append(loss.detach()) # .cpu().numpy()
    train_loss = torch.tensor(train_loss) # .clone().detach()
    e_o = [encoded_data[0][0].item(), encoded_data[0][1].item()] # = encoded_data[0]
    return torch.mean(train_loss).item(), e_o # , encoded_data[0]
        # train_loss : torch tensor cpu - float
        # encoded_data : torch tensor GPU - tuple 2 elements

def test_epoch_den2(encoder,decoder,device,dataloader,loss_fn):
    encoder.eval()
    decoder.eval()
    with torch.no_grad(): # No need to track the gradients
        conc_out=[]
        conc_label=[]
        for item in dataloader:
            item = item.to(device)
            encoded_data=encoder(item) 
            decoded_data=decoder(encoded_data)
            conc_out.append(decoded_data)
            conc_label.append(item) 
        conc_out=torch.cat(conc_out)
        conc_label=torch.cat(conc_label)
        test_loss=loss_fn(conc_out,conc_label)
    e_o = [encoded_data[0][0].item(), encoded_data[0][1].item()] # = encoded_data[0]
    #return test_loss.data, decoded_data, encoded_data
    return test_loss.item(), decoded_data[0], e_o # , encoded_data[0]
    # test_loss : torch tensor cpu - float
    # decoded_dta : torch tensor GPU - liste
    # encoded_data : torch tensor GPU - tuple 2 elements

def createAEfolderName1(hs1, hs2, hs3, hs4, useHL3, useHL4, ls): # , tF, nbFiles, histoName
    folderName = "/HL_1.{:03d}".format(hs1) + "_HL_2.{:03d}".format(hs2)
    if useHL3 == 1:
        folderName += "_HL_3.{:03d}".format(hs3)
    if useHL4 == 1:
        folderName += "_HL_4.{:03d}".format(hs4)
    folderName += "_LT.{:02d}".format(ls) + '/' # + "{:03d}".format(nbFiles)
    #folderName += '/' + histoName + '/' # tF + 
    return folderName

def createAEfolderName2(HL, useHL, ls): 
    folderName = "/HL_1.{:03d}".format(HL[0]) + "_HL_2.{:03d}".format(HL[1])
    if useHL[2] == 1: # Layer 3
        folderName += "_HL_3.{:03d}".format(HL[2])
    if useHL[3] == 1: # Layer 4
        folderName += "_HL_4.{:03d}".format(HL[3])
    if useHL[4] == 1: # Layer 5
        folderName += "_HL_5.{:03d}".format(HL[4])
    if useHL[5] == 1: # Layer 6
        folderName += "_HL_6.{:03d}".format(HL[5])
    if useHL[6] == 1: # Layer 7
        folderName += "_HL_7.{:03d}".format(HL[6])
    folderName += "_LT.{:02d}".format(ls) + '/' # + "{:03d}".format(nbFiles)
    return folderName

def createAEfolderName(HL, useHL, ls): 
    nb_Layers = len(HL)
    folderName = "/" 
    if (useHL[0] == 1): # Layer 0
        folderName += "HL_1.{:03d}".format(HL[0])
    for i in range(1, nb_Layers):
        if (useHL[i] == 1): # Layer i
            folderName += "_HL_{:1d}.{:03d}".format(i+1, HL[i])
    folderName += "_LT.{:02d}".format(ls) + '/' 
    return folderName

def extractLayerList(HL, useHL):
    t1 = []
    u1 = []
    if (len(HL) != len(useHL)):
        print('HL & useHL MUST have the same length !')
        exit()
    else:
        nb_L = len(HL)
        for i in range(0, nb_L):
            if (useHL[i]):
                u1.append(useHL[i])
                t1.append(HL[i])
    return t1, u1
