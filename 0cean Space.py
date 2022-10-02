#!/usr/bin/env
# -*- coding: UTF-8 -*-
__author__ = "Jhong,Dong-You", "SHI, FU-LONG", 'CHOU, HAN-TING', 'Peng, YA-YUN'


def OpenCV_white_to_dark(image):
    import cv2
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # If gray scale >240, shift to 255; gray scale <240, shift to 0
    ret, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    image[thresh == 255] = 0
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    img_erosion = cv2.erode(image, kernel, iterations=1)
    return img_erosion


def OpenCV_png_green_screen(file_path):
    import cv2
    # Ref: https://stackoverflow.com/questions/53732747/
    # load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
    image = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)

    # make mask of where the transparent bits are
    trans_mask = image[:, :, 3] == 0

    # replace areas of transparency with green and not transparent
    image[trans_mask] = [0, 255, 0, 255]

    # new image without alpha channel...
    new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return new_img


def OpenCV_rotate_image(mat, angle, fit_border=False):
    import cv2
    """
    Rotates an image (angle in degrees) and expands image to avoid cropping
    """
    if fit_border:
        height, width = mat.shape[:2]  # image shape has 3 dimensions
        # getRotationMatrix2D needs coordinates in reverse order (width, height) compared to shape
        image_center = (width / 2, height / 2)

        rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

        # rotation calculates the cos and sin, taking absolutes of those.
        abs_cos = abs(rotation_mat[0, 0])
        abs_sin = abs(rotation_mat[0, 1])

        # find the new width and height bounds
        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        # subtract old image center (bringing image back to origo) and adding the new image center coordinates
        rotation_mat[0, 2] += bound_w / 2 - image_center[0]
        rotation_mat[1, 2] += bound_h / 2 - image_center[1]
        # rotate image with the new bounds and translated rotation matrix
        rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))

        return rotated_mat
    else:
        image_center = tuple(np.array(mat.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(mat, rot_mat, mat.shape[1::-1], flags=cv2.INTER_LINEAR)
        return result


def OpenCV_remove_bg_mask(image):
    import cv2
    # threshold on white
    # Define lower and upper limits
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])

    # Create mask to only select black
    thresh = cv2.inRange(image, lower, upper)

    # apply morphology
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # invert morp image
    mask = 255 - morph

    # apply mask to image
    result = cv2.bitwise_and(image, image, mask=mask)

    # save results
    cv2.imwrite('thresh.jpg', thresh)
    cv2.imwrite('morph.jpg', morph)
    cv2.imwrite('mask.jpg', mask)
    cv2.imwrite('result.jpg', result)

    cv2.namedWindow('thresh', cv2.WINDOW_NORMAL)
    cv2.imshow('thresh', thresh)

    cv2.namedWindow('morph', cv2.WINDOW_NORMAL)
    cv2.imshow('morph', morph)

    cv2.namedWindow('mask', cv2.WINDOW_NORMAL)
    cv2.imshow('mask', mask)

    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.imshow('result', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def OpenCV_add_image_to_xy(bg_image, logo_image, x, y):
    """
    x, y should be:
    bg_img = cv2.imread("bg.png")
    # Find logo middle point
    bg_h = bg_img.shape[0]
    bg_w = bg_img.shape[1]
    bg_x = bg_h / 2
    bg_y = bg_w / 2
    """
    h = int(logo_image.shape[0])
    w = int(logo_image.shape[1])
    bg_image[int(y): int(y + h), int(x):int(x + w)] = logo_image[:h, :w]
    # print(h, w, x, y)
    return bg_image


def OpenCV_remove_bg_add_image(bg_image, logo_image, x, y,
                               r_min, g_min, b_min, r_max, g_max, b_max):
    image2 = bg_image.copy()
    h = int(logo_image.shape[0])
    w = int(logo_image.shape[1])
    x = int(x)
    y = int(y)
    # img2[y:y+h,x:x+w] = logo[:h,:w]
    # For every pixel
    for row in range(h):  # Rows
        for column in range(w):  # Columns
            # Every pixel: [B, G, R], '2' is the index of the cell
            r = logo_image[row, column, 2]
            g = logo_image[row, column, 1]
            b = logo_image[row, column, 0]
            if (r >= r_min) and (g >= g_min) and (b >= b_min) and \
                    (r <= r_max) and (g <= g_max) and (b <= b_max):
                continue  # Discard the colors in this range
            else:
                image2[y + row, x + column] = logo_image[row, column]  # Replace pixel by pixel
    return image2


def Folder_path_fix(iPath):
    # To fix path according to OS
    # Get path first before using pathFix
    import sys
    if sys.platform.startswith("linux") or sys.platform == "darwin":  # MAC OS X
        iPath = iPath.replace("\\", "/")
        # print("Folder path fixed!")
    elif sys.platform == "win32":  # Windows (either 32-bit or 64-bit)
        iPath = iPath.replace("/", "\\")
        # print("Folder path fixed!")
    return iPath


def OpenCV_image_rectangle(image):
    import cv2
    image = cv2.rectangle(image,
                          # x, y
                          pt1=(0, 0),  # Start point
                          pt2=(image.shape[1], image.shape[0]),  # End point
                          color=(255, 255, 255),  # B, G, R
                          thickness=3)
    return image


def OpenCV_put_score(image, score_1, image_title=''):
    import cv2
    score_1 = str(score_1)

    image = cv2.putText(image, text='Score: ' + score_1, org=(10, 850), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.7, color=(255, 255, 255), thickness=2)
    image = cv2.putText(image, text='Image: ' + image_title, org=(10, 900), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=0.7, color=(255, 255, 255), thickness=2)
    image = cv2.putText(image, text='Press A or D to control', org=(10, 950),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.7, color=(255, 255, 255),
                        thickness=2)
    return image


if __name__ == '__main__':
    import cv2
    import numpy as np

    # Load the image and show it
    # Ref: https://www.flickr.com/photos/nasawebbtelescope/51412123217/in/album-72157624413830771/
    webb_img = cv2.imread("webb.jpg")
    # Read background file
    # Ref: https://webbtelescope.org/contents/media/images/2022/046/01GCCVQ72QM3D8CM2MRFGZ94HB
    bg_img = cv2.imread("bg.png")
    webb_h = webb_img.shape[0]
    webb_w = webb_img.shape[1]
    webb_mid_x = webb_h / 2
    webb_mid_y = webb_w / 2
    bg_h = bg_img.shape[0]
    bg_w = bg_img.shape[1]
    bg_mid_x = bg_h / 2
    bg_mid_y = bg_w / 2
    webb_x = bg_mid_x - webb_mid_x
    webb_y = bg_mid_y - webb_mid_y
    # To load congrats cat files
    # Ref: Our teammates' lovely cats
    cat_file_list = ["1.png", "2.png", "3.png", "4.png"]
    cat_img_list = []
    for cat_file in cat_file_list:
        path = "cats/" + cat_file
        # Fix file path according to users' OS
        path = Folder_path_fix(path)
        cat_img_list.append(OpenCV_png_green_screen(path))

    # To load star files
    star_file_list = ["“Cosmic Cliffs” in the Carina Nebula (NIRCam and MIRI Composite Image)",
                      "“Cosmic Cliffs” in the Carina Nebula (NIRCam Image)",
                      "Cartwheel Galaxy (MIRI Image)",
                      "Cartwheel Galaxy (NIRCam Image)",
                      "Southern Ring Nebula (MIRI Image)",
                      "Southern Ring Nebula (NIRCam Image)",
                      "Stephan's Quintet (MIRI Image)",
                      "Stephan's Quintet (NIRCam Image)",
                      "Tarantula Nebula (MIRI Image)",
                      "Tarantula Nebula (NIRCam Image)",
                      "Webb's First Deep Field (NIRCam Image)",
                      "Webb’s First Deep Field (MIRI Image)"]

    # Replace characters which cause error while using putText
    mapping = {'“': "'", '” ': "' ", '’': "'", '.png': ''}
    star_img_list = []
    star_name = []
    for star_file in star_file_list:
        path = "stars/" + star_file + ".png"
        # Fix file path according to users' OS
        path = Folder_path_fix(path)
        # Read star files
        star_img = cv2.imread(path)
        for k, v in mapping.items():
            star_file = star_file.replace(k, v)
        star_name.append(star_file)
        # Draw a rectangle to every star image to highlight
        star_img = OpenCV_image_rectangle(star_img)
        star_img_list.append(star_img)

    s = 15  # Range of the R, G, B value you want to remove in the background
    score = 0  # Score that player rotates the Webb to the right angle
    timer = 0  # Seconds that player consumes
    loop = 0  # While loop count
    degree = 0  # Degree that webb rotates
    # 12 stars' positions
    star_x = [50, 750, 60, 97, 722, 428, 441, 727, 232, 703, 171, 684]
    star_y = [50, 60, 622, 452, 704, 160, 691, 409, 236, 653, 444, 245]
    ans_deg = [135, 45, 225, 180, 315, 90, 270, 0, 135, 315, 180, 45]
    while True:
        if score == 12:  # If player finish the game
            cv2.destroyAllWindows()  # Clear previous window
            while True:  # Start congrats window and wait players to press exit buttons
                # Put congrats text on screen
                bg_img = cv2.putText(bg_img, text='Congrats !', org=(350, 400),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=3)
                bg_img = cv2.putText(bg_img, text='You beat the game !', org=(350, 440),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=3)
                bg_img = cv2.putText(bg_img, text='Press Q to exit...', org=(350, 480),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=3)
                bg_img = cv2.putText(bg_img, text='0cean Space Crew', org=(350, 650),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=3)
                bg_img = cv2.putText(bg_img, text='JHONG, DONG-YOU', org=(350, 690),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=2)
                bg_img = cv2.putText(bg_img, text='SHI, FU-LONG', org=(350, 730),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=2)
                bg_img = cv2.putText(bg_img, text='CHOU, HAN-TING', org=(350, 770),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=2)
                bg_img = cv2.putText(bg_img, text='Peng, YA-YUN', org=(350, 810),
                                     fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                                     color=(100, 255, 255), thickness=2)

                # Cat congrats images' positions
                cat_x = [10, 10, 830, 809]
                cat_y = [10, 762, 10, 762]
                # Add cat images to background image
                for cat_num, cat_img in enumerate(cat_img_list):
                    bg_img = OpenCV_remove_bg_add_image(bg_img, cat_img, cat_x[cat_num], cat_y[cat_num],
                                                        0, 255, 0, 0, 255, 0)
                cv2.namedWindow('Congrats!', cv2.WINDOW_NORMAL)
                cv2.imshow("Congrats!", bg_img)
                key = cv2.waitKey(200)
                if (key == 113) or (key == 81) or (key == 27) or (key == 6):  # q or Q or ESC or q in chinese
                    break  # Exit congrats while loop
            break  # Exit the program while loop

        webb_img2 = OpenCV_rotate_image(webb_img, degree, False)
        game_img = OpenCV_remove_bg_add_image(bg_img, webb_img2, webb_x, webb_y,
                                              0, 0, 0, 0 + s, 0 + s, 0 + s)
        game_img = OpenCV_add_image_to_xy(game_img, star_img_list[score], star_x[score], star_y[score])

        game_img = OpenCV_put_score(game_img, score, star_name[score])
        cv2.namedWindow('Game Window', cv2.WINDOW_NORMAL)
        cv2.imshow("Game Window", game_img)
        key = cv2.waitKey(200)

        if (key == 113) or (key == 81) or (key == 27) or (key == 6):  # q or Q or ESC or q in chinese
            break
        elif (key == 97) or (key == 65) or (key == 2):  # a or A or left
            degree = degree + 45
        # You can add more function buttons
        # elif (key == 119) or (key == 87) or (key == 0):          # w or W or up
        #     your functions
        elif (key == 100) or (key == 68) or (key == 3):  # s or S or right
            degree = degree - 45
        # You can add more function buttons
        # elif (key == 115) or (key == 83) or (key == 1):          # d or D or down
        #     your functions

        if degree >= 360 or degree <= -360:
            degree = 0
        if (degree == ans_deg[score]) or (degree + 360 == ans_deg[score]):
            score = score + 1
