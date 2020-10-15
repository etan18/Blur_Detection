"""finds pupil, exports center and perimeter  """
import math
import sys
#import getopt
import numpy as np
import cv2  #add OpenCV Library
#import argparse
import matplotlib.pyplot as plt

INIT_THRESH = 50#150 #Initial Threshold Value
PUPIL_MIN = 600
PUPIL_MAX = 600000
DEFAULT_FILE_NAME = "right.bmp"
#text
FONT = cv2.FONT_HERSHEY_SIMPLEX

class Point():
    """Dont remember what this is for """
    x = -1
    y = -1
    x_l = -1
    x_r = -1
    y_t = -1
    y_b = -1


def rank_p_filter(imgray, length, rank):
    '''
    #rank_p_filter - 1D horizontal rank-p filter
    #input: grayscale image, Length, rank
    '''
    imgray_out = imgray.copy()

    if (length % 2) == 1:
        mid = int((length-1)/2)  # -----!-----
    else:
        raise ValueError('Length must be odd')

    if rank > length:
        raise ValueError('Rank (rank) cannot be greater than length (length).')

    hight = imgray.shape[0]
    width = imgray.shape[1]

    for i in np.arange(mid, hight-mid):
        for j in np.arange(mid, width-mid):
            window = imgray[i, j-mid:j+mid+1]
            _, index = np.unique(window, return_index=True)

            if index.size < rank: #not enouph ranks
                pass
            else:
                imgray_out[i, j] = window[index[index.size-rank]]
                # print('window', window)
                # print('sorted values',values)
                # print('index', index)
                # print('result',imgray_out[i,j-length:j+length+1])
                # print('result v',imgray_out[i,j])

    cv2.imshow('no lashes?', imgray_out)
    return imgray_out


#pupil_contour
#input: color image, graysacle theshold, minimum pupil size, maximum pupil size
#output contour
def pupil_contour(img, threshold, debug=1):
    #Find contour
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh_img = cv2.threshold(imgray, INIT_THRESH, 255, 0)

    if debug > 1:
        cv2.imshow('threshold', thresh_img)
        cv2.imshow('gray', imgray)
        cv2.waitKey(0) #TODO: make waitkey a flag

    #for threshold testing
    thresh_img_copy = cv2.cvtColor(thresh_img, cv2.COLOR_GRAY2RGB)
    img_copy = img.copy()

    contour_candidates = []
    #find the iris contour
    #for this image
    #print(threshold)
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


    if len(contours) == 1 :
        best_contour = np.empty(contours[0].shape) #Empty Contour
    else:
        best_contour = np.empty(contours[1].shape) #Empty Contour
    for contour in contours:
        area = cv2.contourArea(contour)
        if PUPIL_MAX > area > PUPIL_MIN:

            #circle test
            perimeter = cv2.arcLength(contour, True)
            circularity = 4*math.pi*(area/(perimeter*perimeter))
            if perimeter == 0:
                break

            if debug > 1:
                cv2.drawContours(thresh_img_copy, contour, -1, (0, 255, 0), 3)
                cv2.drawContours(img_copy, contour, -1, (0, 255, 0), 3)
                cv2.imshow("Contour Testing RAW", img_copy)
                cv2.imshow("Contour Testing Thresh", thresh_img_copy)
                print("circularity = ", circularity)
                print("Contour Area = ", cv2.contourArea(contour))
                cv2.waitKey(0)

            if circularity > 0.80:
                contour_candidates.append({'Circularity': circularity, 'Contour': contour})

    # pylint: disable=R1715
    if contour_candidates == []: #if nothing found
        if len(contours) > 1:
            return np.empty(contours[1].shape)
        else:
            return np.empty(contours[0].shape)
    else:
        #get best candidate (top circularity for now)
        sorted_contour_candidates = sorted(contour_candidates, \
                                    key=lambda k: k['Circularity'], reverse=True)
        #print(contour_candidates)
        best_contour = sorted_contour_candidates[0]["Contour"]
        #print(best_contour)
        return best_contour

#Pupillometry
#input1: input_, string of source file or cv2 image
#input2: dubug, debug level
#input3: method 1 = V.S. 2 = ZH
#output: saves CSV file of contour of pupil and avi file, returns imgFile w/ edit
def pupillometry(input_, debug=2, method=1):
    """main function that gets called by others"""
    if isinstance(input_, str):
        img = cv2.imread(input_)
    else:
        img = input_

    img_main = img.copy() #Main to display of what's going on
    base_name = "test"

    if debug > 0:
        cv2.imshow('Main', img)

    # pylint: disable=R1705
    if method == 1: #V.S. method
        #CSV file
        # try:
        #     os.remove("data.csv")
        # except:
        #     return "something went wrong"
        csvdata = open('outputcsv'+'.csv', "w")
        csvdata.write('timestamp (ms),data (radius,radians)\n')
        contour_found = False
        #keep trying with different thresholds, until you find something
        for i in range(0, 20, 5):
            try:
                # #Find best contour
                best_contour = pupil_contour(img, INIT_THRESH + i, debug)
                #Find distance from center of contour and contour
                c_size, _, _ = best_contour.shape
                radius = np.empty(c_size)
                moment = cv2.moments(best_contour)
                contour_found = True
                break #exit loop
            except cv2.error as er:
                print('try again')

        #failed to find something
        if not contour_found:
            SKIP_STR = "skip"
            cv2.putText(img_main, SKIP_STR, (230, 250), FONT, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            rads = np.empty(c_size)
        else:
            cv2.drawContours(img_main, best_contour, -1, (0, 255, 0), 3)
            if debug > 0:
                cv2.imshow('Main', img_main)
                if debug > 1:
                    cv2.waitKey(0)
            index = 0
            centroid_x = int(moment['m10']/moment['m00'])
            centroid_y = int(moment['m01']/moment['m00'])
            cv2.circle(img_main, (centroid_x, centroid_y), 5, (0, 0, 255), -1)
            if debug > 0:
                cv2.imshow('Main', img_main)
                cv2.waitKey(0)

            for n in best_contour:
                delta_x = centroid_x-n[0][0]
                delta_y = centroid_y-n[0][1]
                radius[index] = math.sqrt(delta_x**2 + delta_y**2)
                index += 1
            #Find angle from center of circle and contour
            rads = np.empty(c_size)
            index = 0
            for n in best_contour:
                delta_x = centroid_x-n[0][0]
                delta_y = centroid_y-n[0][1]
                rads[index] = math.atan2(delta_y, delta_x)
                index += 1
            # # #print rads
            time = 1
            #save to csv
            csvdata.write(str(time)+',')
            np.savetxt(csvdata, radius, '%s', delimiter=',', newline=',')
            csvdata.write('\n')
            csvdata.write(str(time))
            np.savetxt(csvdata, rads, '%s', delimiter=',', newline=',')
            csvdata.write('\n')
            if debug > 0:
                plt.ion()
                plt.clf()
                plt.axis([-4, 4, 0, 200])
                plt.plot(rads, radius, 'ro')
                plt.ylabel('radius (pixels)')
                plt.xlabel('angle (radians)')
                plt.show()
                plt.pause(0.10)
                if debug > 1:
                    cv2.waitKey(0)
        return img_main, rads, radius
    elif method == 2: #Zhaofeng He Method.

        #Reflection Removal and Iris Detection
        #"reflection" map
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh_img = cv2.threshold(imgray, 200, 255, 0) #TODO:Make adaptive
        height, width = imgray.shape
        cv2.imshow('pre-E', thresh_img)
        EPSILON = 4 # epsilon in pixels to expand reflection area

        #rank-p filter
        L_RANK_FILTER = 13
        P_RANK_FILTER = 2

        for n in range(0, EPSILON):
            print('n:', n)
            reflection_points = np.where(thresh_img == 255) #reflection points
            list_of_rf_pts = \
                list(zip(reflection_points[0], reflection_points[1])) #list of white point
            for rf_pt in list_of_rf_pts:
                ytemp = rf_pt[0]
                xtemp = rf_pt[1]

                if xtemp + 1 < width:
                    thresh_img[ytemp, xtemp+1] = 255
                if xtemp + 1 < width and ytemp+1 < height:
                    thresh_img[ytemp+1, xtemp+1] = 255
                if ytemp+1 < height:
                    thresh_img[ytemp+1, xtemp] = 255
                if ytemp+1 < height and xtemp-1 >= 0:
                    thresh_img[ytemp+1, xtemp-1] = 255
                if xtemp-1 >= 0:
                    thresh_img[ytemp, xtemp-1] = 255
                if xtemp-1 >= 0 and ytemp-1 >= 0:
                    thresh_img[ytemp-1, xtemp-1] = 255
                if ytemp-1 >= 0:
                    thresh_img[ytemp-1, xtemp] = 255
                if ytemp-1 >= 0 and xtemp + 1 < width:
                    thresh_img[ytemp-1, xtemp+1] = 255

        cv2.imshow('post-E', thresh_img)
        #print(thresh_img[1,1])


        #bilinear interpolation
        L = 2  # separation between the reflection points and their envelope points
        bi_imgray = imgray.copy()
        bi_thresh_img = thresh_img.copy()

        reflection_points = np.where(thresh_img == 255) #white points
        list_of_rf_pts = list(zip(reflection_points[0], reflection_points[1])) #list of white points
        points = np.full((height,width), Point()) #matrix of all points

        for rf_pt in list_of_rf_pts:
            ytemp = rf_pt[0]
            xtemp = rf_pt[1]
            x_l = -1
            x_r = -1
            y_t = -1
            y_b = -1
            #thresh_img[ytemp,xtemp] = 0
            cv2.imshow('threshold', thresh_img)
            #print(ytemp,xtemp)
            #cv2.waitKey(0)

            points[ytemp, xtemp].x = xtemp
            points[ytemp, xtemp].y = ytemp
            #find x_l
            if xtemp > L-1:#not along the edge
                for k in range(xtemp-1, -1, -1):
                    if(thresh_img[ytemp,k] == 0):
                        x_l = k-(L-1)
                        points[ytemp, xtemp].x_l = x_l
                        bi_thresh_img[ytemp, x_l] = 100
                        #print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_l = -1


            #find x_r
            if xtemp < 719-L:#not along the edge
                for l in range(xtemp+1, 719-L):
                    if(thresh_img[ytemp, l] == 0):
                        x_r = l+(L-1)
                        points[ytemp, xtemp].x_r = x_r
                        bi_thresh_img[ytemp, x_r] = 100
                        #print(xtemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                x_r = -1

            #find y_b
            if ytemp > L-1: #not along the edge
                for m in range(ytemp-1, -1, -1):
                    if(thresh_img[m, xtemp] == 0):
                        y_b = m-(L-1)
                        points[ytemp, xtemp].y_b = y_b
                        bi_thresh_img[y_b, xtemp] = 100
                        #print(ytemp)
                        #TODO: move backwards and fill in the rest.
                        break
            else:
                y_b = -1

            #find y_t
            if ytemp < 479-L:
                for n in range(ytemp+1, 479-L):
                    if(thresh_img[n, xtemp] == 0):
                        y_t = n+(L-1)
                        points[ytemp, xtemp].y_t = y_t
                        bi_thresh_img[y_t, xtemp] = 100
                        #print(ytemp)
                        #TODO: move backwarda and fill in the rest.
                        break
            else:
                y_t = -1


            if x_l != -1 and x_r != -1 and  y_b != -1 and y_t != -1:
                # print('xtemp: ', xtemp, 'ytemp: ', ytemp, 'x_l: ', \
                #     x_l, 'x_r: ', x_r, 'y_t: ', y_t, 'y_b: ', y_b)
                # print('I(P_L):', imgray[ytemp, x_l], 'I(P_R):', imgray[ytemp, x_r],\
                #     'I(P_t):', imgray[y_t, xtemp], 'I(P_d):', imgray[y_b, xtemp])
                #cv2.waitKey(0)
                bi_imgray[ytemp, xtemp] = \
                    (imgray[ytemp, x_l]*(x_r-xtemp)+imgray[ytemp, x_r]*(xtemp-x_l))/(2*(x_r-x_l)) + \
                    (imgray[y_t, xtemp]*(ytemp-y_b)+imgray[y_b, xtemp]*(y_t-ytemp))/(2*(y_t-y_b))

        #Eyelid Localization
        #1D rank filter removes eyelashes
        lp_imgray = rank_p_filter(bi_imgray, L_RANK_FILTER, P_RANK_FILTER) #L-length p-rank

        cv2.imwrite("no_lashes.bmp", lp_imgray)

        if debug > 1:
            cv2.imshow('threshold', thresh_img)
            cv2.imshow('gray', imgray)
            cv2.imshow('bi', bi_imgray)
            cv2.imshow('bi_threshold', bi_thresh_img)
            cv2.waitKey(0) #TODO: make this a flag
        #Pupillary & Limbic Bd. Localizatoin
        #Eyelid Localization
        #Eyelash and Shadow Detection
            csvdata.write(str(time)+',')
            np.savetxt(csvdata, radius, '%s', delimiter=',', newline=',')
            csvdata.write('\n')
            csvdata.write(str(time))
            np.savetxt(csvdata, rads, '%s', delimiter=',', newline=',')
            csvdata.write('\n')
        return img_main, rads, radius
if __name__ == "__main__":
    print(len(sys.argv))
    if len(sys.argv) > 1:
        if len(sys.argv) == 2:
            method = int(sys.argv[1])
            filename = DEFAULT_FILE_NAME
        if len(sys.argv) == 3:
            method = int(sys.argv[1])
            filename = sys.argv[2]
    else:
        method = 1
        filename = DEFAULT_FILE_NAME
    print("Method : ", method)
    print("File Name", filename)
    pupillometry(filename, 2, method)
