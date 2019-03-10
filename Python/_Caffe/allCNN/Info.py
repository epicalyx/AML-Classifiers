############################################################################################
#
# The MIT License (MIT)
# 
# Peter Moss Acute Myeloid/Lymphoblastic Leukemia AI Research Project
# Copyright (C) 2018 Adam Milton-Barker (AdamMiltonBarker.com)
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Title:         Caffe Acute Lymphoblastic Leukemia CNN Info
# Description:   Used to view info Caffe Acute Lymphoblastic Leukemia CNN
# Configuration: required/confs.json
# Last Modified: 2019-03-10
#
############################################################################################

import os, sys, cv2
sys.path.append('/home/upsquared/caffe/python')
import caffe

import numpy as np

from Classes.Helpers import Helpers

class allCNN():

    def __init__(self):
        
        ###############################################################
        #
        # Sets up all default requirements and placeholders 
        # needed for the Caffe Acute Lymphoblastic Leukemia CNN.
        #
        ###############################################################
        
        # Load Helper functions
        self.Helpers = Helpers()
        self.confs = self.Helpers.loadConfs()
        self.logFile = self.Helpers.setLogFile(self.confs["Settings"]["Logs"]["allCNN"])
        
        self.Helpers.logMessage(self.logFile, "allCNN", "Status", "Init complete")

    def loadCaffeNet(self):
        
        ###############################################################
        #
        # Loads the Caffe network using prototxt layer definition.
        #
        ###############################################################
        
        self.net = caffe.Net(self.confs["Settings"]["Classifier"]["layerFile"], caffe.TEST)
        
        self.Helpers.logMessage(self.logFile, "allCNN", "Status", "Caffe net initialized")

    def printDetails(self):
        
        ###############################################################
        #
        # Prints and logs input, blob and parameter info.
        #
        ###############################################################
        
        self.Helpers.logMessage(self.logFile, "allCNN", "Net Inputs", "See below")
        print(self.net.inputs)
        self.Helpers.logMessage(self.logFile, "allCNN", "Net Blobs", "See below")
        print(self.net.blobs)
        self.Helpers.logMessage(self.logFile, "allCNN", "Net Params", "See below")
        print(self.net.params)

    def writeOutputImages(self, image):
        
        ###############################################################
        #
        # Prints input, blob and parameter info.
        #
        ###############################################################

        inp = np.transpose(cv2.imread(image))
        self.net.blobs['data'].reshape(1, *inp.shape)
        self.net.blobs['data'].data[...] = inp
        self.net.forward()

        for i in range(30):
            cv2.imwrite(self.confs["Settings"]["Classifier"]["dataDir"] + self.confs["Settings"]["Classifier"]["infoOutDir"] + 'out_' + str(i) + '.jpg', 255 * self.net.blobs['conv1'].data[0,i])

        self.Helpers.logMessage(self.logFile, "allCNN", "Output Images", "Output images written to " + self.confs["Settings"]["Classifier"]["dataDir"] + self.confs["Settings"]["Classifier"]["infoOutDir"])

    def saveCaffeNet(self):
        
        ###############################################################
        #
        # Saves our Caffe network.
        #
        ###############################################################

        self.net.save(self.confs["Settings"]["Classifier"]["modelFile"])
        
        self.Helpers.logMessage(self.logFile, "allCNN", "Status", "Caffe net saved")

allCNN = allCNN()

def main(argv):

    if(len(argv) < 1):
        
        ###############################################################
        #
        # Incorrect arguments size.
        #
        ###############################################################

        allCNN.Helpers.logMessage(allCNN.logFile, "allCNN", "Arguments", "Please provide NetworkInfo or Outputs argument")

    elif argv[0] == "NetworkInfo":
        
        ###############################################################
        #
        # Provides information about our Caffe network.
        #
        ###############################################################

        allCNN.loadCaffeNet()
        allCNN.printDetails()

    elif argv[0] == "Outputs":
        
        ###############################################################
        #
        # Plots the outputs of each neuron as images.
        #
        ###############################################################

        allCNN.loadCaffeNet()
        allCNN.writeOutputImages(allCNN.confs["Settings"]["Classifier"]["dataDir"] + allCNN.confs["Settings"]["Classifier"]["dataTestDir"] + allCNN.confs["Settings"]["Classifier"]["infoTestImage"])

    elif argv[0] == "Save":
        
        ###############################################################
        #
        # Saves our Caffe network.
        #
        ###############################################################

        allCNN.loadCaffeNet()
        allCNN.saveCaffeNet()

if __name__ == "__main__":
	main(sys.argv[1:])