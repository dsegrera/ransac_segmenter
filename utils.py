import numpy as np
import cv2
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import euclidean_distances


# 4 point algorithm
# p1, p2 are lists of 4 (x, y) points
def find_homography(p1, p2):
    A = np.matrix([[p1[0][0], p1[0][1], 1, 0, 0, 0, -p2[0][0]*p1[0][0], -p2[0][0]*p1[0][1]],
                  [0, 0, 0, p1[0][0], p1[0][1], 1, -p2[0][1]*p1[0][0], -p2[0][1]*p1[0][1]],
                  [p1[1][0], p1[1][1], 1, 0, 0, 0, -p2[1][0]*p1[1][0], -p2[1][0]*p1[1][1]],
                  [0, 0, 0, p1[1][0], p1[1][1], 1, -p2[1][1]*p1[1][0], -p2[1][1]*p1[1][1]],
                  [p1[2][0], p1[2][1], 1, 0, 0, 0, -p2[2][0]*p1[2][0], -p2[2][0]*p1[2][1]],
                  [0, 0, 0, p1[2][0], p1[2][1], 1, -p2[2][1]*p1[2][0], -p2[2][1]*p1[2][1]],
                  [p1[3][0], p1[3][1], 1, 0, 0, 0, -p2[3][0]*p1[3][0], -p2[3][0]*p1[3][1]],
                  [0, 0, 0, p1[3][0], p1[3][1], 1, -p2[3][1]*p1[3][0], -p2[3][1]*p1[3][1]]])
    y = np.matrix([[p2[0][0]],
                  [p2[0][1]],
                  [p2[1][0]],
                  [p2[1][1]],
                  [p2[2][0]],
                  [p2[2][1]],
                  [p2[3][0]],
                  [p2[3][1]]])
    try:
        h = np.linalg.solve(A, y)
    # this exception happens only when 3 points in either p1 or p2 are colinear
    except:
        return None
    retval = np.zeros([3,3], dtype=np.float64)
    c = 0
    for i in range(3):
        for j in range(3):
            if i==2 and j==2:
                retval[i, j] = 1
            else:
                retval[i, j] = h[c]
            c += 1
    return retval


# given SIFT keypoints and descriptors for each image, return pairs of points that are
# likely the same point in the two images
def get_putative_matches(kp1, des1, kp2, des2, train_img):
    # use cv2 to calculate the matches
    matcher = cv2.BFMatcher()
    try:
        matches = matcher.knnMatch(des1, des2, k=2)
    except cv2.error:
        return []
    good_matches = []
    cluster = []
    # prune out matches that are not confident enough,
    # and put matches into tuples of ((x1, y1), (x2, y2))
    for m, n in matches:
        if m.distance / n.distance < 0.65:
            img1_inx = m.queryIdx
            img2_idx = m.trainIdx
            frm = kp1[img1_inx].pt
            # frm = (int(frm[0]), int(frm[1]))
            to = kp2[img2_idx].pt
            # to = (int(to[0]), int(to[1]))
            good_matches.append((frm, to))
            # cluster.append(frm)
    # k_means = KMeans(n_clusters=1, random_state=0).fit(cluster)
    # good_matches = compare_distances(k_means, train_img, cluster, good_matches)
    return good_matches


# def compare_distances(k_means, train_img, cluster, good_matches):
#     # sometimes the sift algorithm matches random points on screen so therefore
#     # it is necessary to determine the euclidean distances between these points
#     distances = euclidean_distances([k_means.cluster_centers_[0]], cluster)
#     height, width, RGB = train_img.shape
#     new_cluster = []
#     new_matches = []
#     # If all the points are greater than np.sqrt((width / 2) ** 2 + (height / 2) ** 2)
#     # Which then we can assume that they are not correct
#     # this will only work on images that fit the same dimensions against the query image
#     for index, distance in enumerate(distances[0]):
#         if distance <= np.sqrt((width / 2) ** 2 + (height / 2) ** 2):
#             new_cluster.append(cluster[index])
#             new_matches.append(good_matches[index])
#     if len(new_cluster) / len(cluster) < .5:
#         return []
#     return new_matches

