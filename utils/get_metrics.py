from os import listdir
from os.path import join, isfile, basename
from typing import List

import numpy as np
import cv2 as cv
import pandas as pd

from baboon_tracking import BaboonTracker
from baboon_tracking.mixins.baboons_mixin import BaboonsMixin
import import_xml

# constants that define screen size
FRAME_WIDTH = 2160
FRAME_HEIGHT = 3840

# create a mask of bools for a given list of centroids(x,y,diameter)
def create_mask(baboons):
    mask = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)
    for b in baboons:
        x = int(b[0])
        y = int(b[1])
        radius = int(b[2] / 2)
        cv.circle(mask, (x, y), radius, (255, 255, 255), lineType=cv.FILLED)
    mask = mask[:, :, 0].squeeze().astype(bool)
    return mask


# given two masks use bitwise logic to classify observations
def categorize_observations(observed_mask, labeled_mask):
    and_mask = np.logical_and(observed_mask, labeled_mask)
    or_mask = np.logical_or(observed_mask, labeled_mask)
    xor_mask = np.logical_xor(observed_mask, labeled_mask)
    true_neg = np.count_nonzero(or_mask == False)
    true_pos = np.count_nonzero(and_mask == True)
    false_neg = np.count_nonzero(np.logical_and(xor_mask, labeled_mask) == True)
    false_pos = np.count_nonzero(np.logical_and(xor_mask, observed_mask) == True)
    return (true_pos, true_neg, false_pos, false_neg)


# get the metrics for the files in the tests folder, labeled data in labels folder
# files named same as test with xml extensions
def get_metrics():
    root = "./data/tests"
    files = [join("tests", d) for d in listdir(root) if isfile(join(root, d))]

    for file in files:
        print('Getting metrics for "' + file + '"')
        baboon_labels = import_xml.listCentroidsFromXML(
            join(root, "labels", basename(file), ".xml")
        )

        baboon_tracker = BaboonTracker(input_file=file)

        baboons_mixin: BaboonsMixin = baboon_tracker.get(BaboonsMixin)

        should_continue = True
        frame_counter = 0
        metrics = []
        while should_continue:
            should_continue = baboon_tracker.step().continue_pipeline
            new_found_baboons = []
            labeled_baboons = []
            if baboons_mixin.baboons is not None:
                new_found_baboons = [
                    (b.centroid[0], b.centroid[1], b.diameter)
                    for b in baboons_mixin.baboons
                ]
            if baboon_labels[frame_counter] is not None:
                labeled_baboons = baboon_labels[frame_counter]

            found_mask = create_mask(new_found_baboons)
            label_mask = create_mask(labeled_baboons)
            metrics.append(categorize_observations(found_mask, label_mask))

            frame_counter += 1

        df = pd.DataFrame(metrics)

        df.to_csv(basename(file) + "_metrics.csv")


def get_region_mask(region):
    mask = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), np.uint8)

    x = int(region[0])
    y = int(region[1])
    radius = int(region[2] / 2)
    mask = cv.circle(mask, (y, x), radius, (255, 255, 255), thickness=cv.FILLED)

    return mask[:, :, 0].squeeze() == 255


def calculate_iou(region_1, region_2):
    mask_1 = get_region_mask(region_1)
    mask_2 = get_region_mask(region_2)

    intersect = np.sum(np.logical_and(mask_1, mask_2).astype(np.float32))
    union = np.sum(np.logical_or(mask_1, mask_2).astype(np.float32))

    if intersect == 0:
        return 0

    return intersect / union


def check_if_same_region(region_1, region_2):
    iou = calculate_iou(region_1, region_2)
    return iou > 0.2


# test function, hard coded to pull from input.mp4 and input.xml
def test_metrics():
    print("testing on input")
    baboon_labels = import_xml.listCentroidsFromXML("./data/input.xml")

    baboon_tracker = BaboonTracker(input_file="input.mp4")
    print("tracker opened")
    baboons_mixin: BaboonsMixin = baboon_tracker.get(BaboonsMixin)

    should_continue = True
    frame_counter = 0
    metrics = []
    while should_continue:
        print("frame: " + str(frame_counter))

        true_positive = 0
        false_positive = 0

        should_continue = baboon_tracker.step().continue_pipeline
        new_found_baboons = []
        labeled_baboons = []
        if baboons_mixin.baboons is not None:
            new_found_baboons = [
                (b.centroid[0], b.centroid[1], b.diameter)
                for b in baboons_mixin.baboons
            ]
        if frame_counter in baboon_labels:
            labeled_baboons = [
                (x, y, diameter) for x, y, diameter in baboon_labels[frame_counter]
            ]

            for new_found_baboon in new_found_baboons:

                baboon_in_labels = any(
                    [
                        check_if_same_region(lb, new_found_baboon)
                        for lb in labeled_baboons
                    ]
                )

                if baboon_in_labels:
                    true_positive += 1
                else:
                    false_positive += 1

                # exit()

            # found_mask = create_mask(new_found_baboons)
            # label_mask = create_mask(labeled_baboons)
            # metrics.append(categorize_observations(found_mask, label_mask))

            print(true_positive)
        else:
            should_continue = False

        frame_counter += 1

    df = pd.DataFrame(metrics)

    df.to_csv("input_metrics.csv")


if __name__ == "__main__":
    test_metrics()
