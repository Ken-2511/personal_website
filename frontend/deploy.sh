#!/bin/bash

# 输出开始提示
echo "Starting the build and deployment process..."

# 运行 npm run build
echo "Running npm run build..."
npm run build

# 检查 build 文件夹是否存在
if [ -d "build" ]; then
    echo "Build successful, proceeding with deployment..."
else
    echo "Build failed, exiting."
    exit 1
fi

# 目标路径
TARGET_DIR="/var/www/html/"

# 确保目标目录存在
if [ ! -d "$TARGET_DIR" ]; then
    echo "The target directory $TARGET_DIR does not exist. Please check the path and try again."
    exit 1
fi

# 复制文件到目标目录
echo "Copying files to $TARGET_DIR..."
sudo cp -r build/* "$TARGET_DIR"

# 检查复制是否成功
if [ $? -eq 0 ]; then
    echo "Deployment completed successfully!"
else
    echo "Failed to copy files. Please check your permissions and try again."
    exit 1
fi
