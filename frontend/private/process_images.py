#!/usr/bin/env python

import os
import cv2

def crop_and_resize_images(scr_path, dest_path, size=1024):
    # 确保目标路径存在
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)

    # 遍历源路径下的所有文件
    for filename in os.listdir(scr_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filepath = os.path.join(scr_path, filename)
            
            # 读取图片
            img = cv2.imread(filepath)
            if img is None:
                print(f"无法读取文件: {filename}")
                continue

            # 获取图像尺寸
            height, width = img.shape[:2]

            # 计算裁剪区域，确保正方形
            if width > height:
                offset = (width - height) // 2
                cropped_img = img[:, offset:offset + height]
            else:
                offset = (height - width) // 2
                cropped_img = img[offset:offset + width, :]

            # 调整大小到指定尺寸
            resized_img = cv2.resize(cropped_img, (size, size), interpolation=cv2.INTER_AREA)

            # 保存处理后的图片
            save_path = os.path.join(dest_path, filename)
            cv2.imwrite(save_path, resized_img)
            print(f"已处理并保存: {save_path}")

if __name__ == "__main__":
    scr_path = "./original_images"  # 替换为源图片文件夹路径
    dest_path = "../public/assets"  # 替换为目标文件夹路径
    crop_and_resize_images(scr_path, dest_path)
