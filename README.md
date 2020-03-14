Classification and Localization of Disease with Bounding Boxes from Chest X-Ray Images

Hugo Kitano

This README explains the usage of the python scripts:

1. preprocessing.py sets up data for training. It requires the paths to text files that have the image names for each of the train, validation, and test set, as well as the path to other data and images. Its outputs are numpy and pickle files that contain the image and class data for the train, validation, and test images. These files will be useful throughout the rest of the pipeline.
2. training.py creates the model and trains it. We use data augmentation for the training set, and try to reduce multi-class binary cross-entropy. On validation, we try to minimize mean AUC over all classes. We use a pre-trained DenseNet121 model on ImageNet.
3. test_classify.py simply finds the AUC of the trained model on the test set. Also makes ROC curve for every class.
4. activations.py creates class activation maps for all images with bounding boxes. I use three different kind of Grad-CAM implementations at this step; Grad-CAM++ is the one I ended up using for the final project as it did best.
5. bounding_boxes.py puts bounding boxes around the class activation maps, while creating overlaying them over the images. Then, it calculates the IoU and other statistics.'

This project is shared between two classes. The pdfs are also here.
