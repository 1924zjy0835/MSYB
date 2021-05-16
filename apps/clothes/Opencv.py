import cv2 as cv


src1 = cv.imread("./../../cloth_models/1.png")
img_raw = cv.imread("./../../cloth_models/woman_clothes05.jpg")

# 对图片进行高斯模糊
blur = cv.GaussianBlur(img_raw, (5,5), 0)

#  对图片进行双边滤波处理，能够在保持边界清晰的情况下，有效的去除噪音
size = (279, 496)
src2 = cv.resize(img_raw, size)

# cv.imshow("cloth.jpg", blur)


# 可用
# 对两张图片进行逻辑的与操作
def bitwise_and_demo(image1, image2):
    and_image = cv.bitwise_and(image1, image2)
    cv.imshow(" and image demo", and_image)


bitwise_and_demo(src2, src1)

cv.waitKey(0)
cv.destroyAllWindows()

