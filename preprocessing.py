import os
import pickle
import sys

import imageio
import numpy as np
import pandas as pd
import skimage.transform
from sklearn.preprocessing import MultiLabelBinarizer


def get_labels(meta_data, pic_id):
    labels = meta_data.loc[meta_data["Image Index"] == pic_id, "Finding Labels"]
    return labels.tolist()[0].split("|")


def main():
    # folder contain all images
    image_folder_path = '/home/qiyuan/2021summer/classification-localization-nih/data/'
    data_entry_path = '/home/qiyuan/2021summer/classification-localization-nih/data/Data_Entry_2017.csv'
    bbox_list_path = '/home/qiyuan/2021summer/classification-localization-nih/data/Data_Entry_2017.csv'
    train_txt_path = '/home/qiyuan/2021summer/classification-localization-nih/data/train_val_list.txt'  # may change
    valid_txt_path = '/home/qiyuan/2021summer/classification-localization-nih/data/train_val_list.txt'  # may change
    # output folder for preprocessed data
    data_path = '/home/qiyuan/2021summer/classification-localization-nih/data'
    # images with bounding boxes
    test_txt_path = "/home/qiyuan/2021summer/classification-localization-nih/data/test_list.txt"

    # load data
    meta_data = pd.read_csv(data_entry_path)
    bbox_list = pd.read_csv(bbox_list_path)
    with open(train_txt_path, "r") as f:
        train_list = [i.strip() for i in f.readlines()]
    with open(valid_txt_path, "r") as f:
        valid_list = [i.strip() for i in f.readlines()]
    with open(test_txt_path, "r") as f:
        test_list = [i.strip() for i in f.readlines()]
    # label_eight = list(np.unique(bbox_list["Finding Label"])) + ["No Finding"]  # length nine

    # transform training images
    print("Training example:", len(train_list))
    print("take care of your RAM here")
    train_x = []

    for i in range(len(train_list)):
        image_path = os.path.join(image_folder_path, train_list[i])
        img = imageio.imread(image_path)
        if img.shape != (1024, 1024):
            img = img[:, :, 0]
        img_resized = skimage.transform.resize(img, (256, 256))  # or use img[::4] here
        train_x.append((np.expand_dims(img_resized, axis=2)))
        if i % 1000 == 0:
            print(i)

    train_x = np.asarray(train_x)
    np.save(os.path.join(data_path, "train_X_small.npy"), train_x)

    # transform validation images
    print("validation example:", len(valid_list))
    valid_x = []
    for i in range(len(valid_list)):
        image_path = os.path.join(image_folder_path, valid_list[i])
        img = imageio.imread(image_path)
        if img.shape != (1024, 1024):
            img = img[:, :, 0]
        img_resized = skimage.transform.resize(img, (256, 256))
        valid_x.append((np.expand_dims(img_resized, axis=2)))
        if i % 1000 == 0:
            print(i)

    valid_x = np.asarray(valid_x)
    np.save(os.path.join(data_path, "valid_X_small.npy"), valid_x)

    # test images
    test_X = []
    print(len(test_list))
    for i in range(len(test_list)):
        image_path = os.path.join(image_folder_path, test_list[i])
        img = imageio.imread(image_path)
        if img.shape != (1024, 1024):
            img = img[:, :, 0]
        img_resized = skimage.transform.resize(img, (256, 256))
        test_X.append((np.array(img_resized)).reshape(256, 256, 1))
        if i % 1000 == 0:
            print(i)

    test_X = np.array(test_X)
    np.save("/home/qiyuan/2021summer/classification-localization-nih/data/test_X_small.npy", test_X)

    # process label
    print("label preprocessing")

    train_y = []
    for train_id in train_list:
        train_y.append(get_labels(meta_data, train_id))
    valid_y = []
    for valid_id in valid_list:
        valid_y.append(get_labels(meta_data, valid_id))
    test_y = []
    for test_id in test_list:
        test_y.append(get_labels(meta_data, test_id))

    encoder = MultiLabelBinarizer()
    encoder.fit(train_y + valid_y)
    train_y_onehot = encoder.transform(train_y)
    valid_y_onehot = encoder.transform(valid_y)
    train_y_onehot = np.delete(train_y_onehot, [2, 3, 5, 6, 7, 10, 12], 1)  # delete out 8 and "No Finding" column
    valid_y_onehot = np.delete(valid_y_onehot, [2, 3, 5, 6, 7, 10, 12], 1)  # delete out 8 and "No Finding" column
    test_y_onehot = encoder.transform(test_y)
    test_y_onehot = np.delete(test_y_onehot, [2, 3, 5, 6, 7, 10, 12], 1)  # delete out 8 and "No Finding" column

    with open(data_path + "/train_y_onehot2.pkl", "wb") as f:
        pickle.dump(train_y_onehot, f)
    with open(data_path + "/valid_y_onehot2.pkl", "wb") as f:
        pickle.dump(valid_y_onehot, f)
    with open(data_path + "/test_bbox_y_onehot.pkl", "wb") as f:
        pickle.dump(test_y_onehot, f)
    with open(data_path + "/label_encoder2.pkl", "wb") as f:
        pickle.dump(encoder, f)


if __name__ == '__main__':
    main()
