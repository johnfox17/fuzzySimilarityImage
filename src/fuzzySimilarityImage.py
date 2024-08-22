import constants
import numpy as np
from scipy import signal
import cv2
class fuzzySimilarityImage:
    def __init__(self, pathToMembershipFunction):
        self.pathToMembershipFunction = pathToMembershipFunction
        self.horizon = constants.HORIZON
        self.Nx = constants.NX
        self.Ny = constants.NY
        self.GMask = constants.GMASK

    def loadMembershipFunction(self):
        self.membershipFunction = np.loadtxt(self.pathToMembershipFunction, delimiter=",")
    
    def enumeratePixels(self):
        self.pixelNumbers = np.array(range((self.Nx+int(2*self.horizon))*(self.Ny+int(2*self.horizon)))).reshape((self.Nx+int(2*self.horizon),self.Ny+int(2*self.horizon)))

    def findNeighboringPixels(self, iRow, iCol):
        return self.pixelNumbers[iRow-int(self.horizon):iRow+int(self.horizon)+1,iCol-int(self.horizon):iCol+int(self.horizon)+1]

    def findSimilarityPercent(self, xIdx0, yIdx0, xIdx1, yIdx1):
        image = np.pad(self.inputImage,int(self.horizon),mode='symmetric').astype(float)
        pixelDifferences = np.abs(image[xIdx0,yIdx0]-image[xIdx1,yIdx1]).astype(int)
        indexOfMembership = 2 - self.membershipFunction[pixelDifferences,0]
        similarityPercent = []
        for iPixel in range(len(indexOfMembership)):
            idxMembership = indexOfMembership[iPixel]
            if idxMembership == 2.0:
                similarityPercent.append(1.0)
            elif idxMembership == 1.0:
                similarityPercent.append(0.5)
            elif idxMembership == 0.0:
                 similarityPercent.append(0.0)
        similarityPercent = np.divide(np.dot(similarityPercent,self.membershipFunction[pixelDifferences,1] ),np.sum(indexOfMembership))
        return np.array(similarityPercent)

    def findFuzzySimilarityImage(self):
        similarity = []
        for iCol in range(int(self.horizon),self.Nx+2):
            for iRow in range(int(self.horizon),self.Ny+2):
                currentPixelNeighbors = self.findNeighboringPixels(iRow,iCol).flatten()
                similarityPercent = []
                for iNeighbor in currentPixelNeighbors:
                    iNeighborXIndx, iNeighborYIndx = np.unravel_index([iNeighbor], (self.Nx+int(2*self.horizon),self.Ny+int(2*self.horizon)))
                    currentNeighborsNeighbors = self.findNeighboringPixels(iNeighborXIndx[0], iNeighborYIndx[0]).flatten()
                    if currentNeighborsNeighbors.size != 0:
                        currentNeighborsNeighborsXIdx, currentNeighborsNeighborsYIdx = np.unravel_index(currentNeighborsNeighbors,(self.Nx+int(2*self.horizon),self.Ny+int(2*self.horizon)))
                        currentNeighborsNeighborsXIdx = currentNeighborsNeighborsXIdx
                        currentNeighborsNeighborsYIdx = currentNeighborsNeighborsYIdx
                        similarityPercent.append(self.findSimilarityPercent(iNeighborXIndx[0], iNeighborYIndx[0], currentNeighborsNeighborsXIdx, currentNeighborsNeighborsYIdx))
                similarity.append(np.average(similarityPercent))
        self.fuzzySimilarityImage = np.transpose(np.array(similarity).reshape((self.Nx, self.Ny))) 
   
    def solve(self, inputImage):
        self.inputImage = inputImage
        self.enumeratePixels()
        self.loadMembershipFunction()
        self.findFuzzySimilarityImage()
        #a = input('').split(" ")[0]
