import sys
import numpy as np
import cv2
import matplotlib.pyplot as plt
import fuzzySimilarityImage
import constants

def main():
    convertToGrayScale = True
    if sys.platform.startswith('linux'):
        pathToReferenceImage = '../data/simData/Lena.png'
                #'../data/simData/cameraman.png'
                # '../data/simData/Lena.png'
        pathToMembershipFunction = '../data/simData/triangularMembershipFunction.csv'

    else:
        pathToReferenceImage = '..\\data\\simData\\Lena.png'
            #'..\\data\\simData\\cameraman.png'
            #'..\\data\\simData\\Lena.png'
        pathToMembershipFunction = '..\\data\\simData\\triangularMembershipFunction.csv'

    referenceImage = cv2.imread(pathToReferenceImage)

    if convertToGrayScale:
        referenceImage = cv2.cvtColor(referenceImage, cv2.COLOR_BGR2GRAY)
        cv2.imwrite('../data/simData/referenceImageGrayScale.jpg', referenceImage)
        
    
    #Obtain Fuzzy Similarity Image Of Reference Images
    fuzzySimImage = fuzzySimilarityImage.fuzzySimilarityImage(pathToMembershipFunction)
    fuzzySimImage.solve(referenceImage)
    
    np.savetxt('../data/output/fuzzySimilarityImage_lena512x512.csv', fuzzySimImage.fuzzySimilarityImage, delimiter=",")

    print('End of simulation')


if __name__ == "__main__":
    main()

