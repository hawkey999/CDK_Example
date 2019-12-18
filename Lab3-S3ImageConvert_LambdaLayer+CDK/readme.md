# Lab 3 Amazon S3 自动转换图片格式（ Lambda Layer与环境变量，CDK部署）
Amazon S3 存储桶 input 目录新增文件自动触发 AWS Lambda。Lambda 取 S3 文件做转换并存回去 S3 同一个桶的 output 目录下。本 Lab 使用 Python Pillow 做图片转换，读者可以参考 Pillow 文档进行功能扩展。  
## 实现以下功能
### 转换格式
指定以下格式转换，或者选择保留原图格式
* Full Suported image formats: BMP, DIB, EPS, GIF, ICNS, ICO, IM, JPEG, JPEG 2000, MSP, PCX, PNG, PPM, SGI, SPIDER, TGA, TIFF, WebP, XBM
* Read-only formats: BLP, CUR, DCX, DDS, FLI, FLC, FPX, FTEX, GBR, GD, IMT, IPTC/NAA, MCIDAS, MIC, MPO, PCD, PIXAR, PSD, WAL, XPM
* Write-only formats: PALM, PDF, XV Thumbnails  

更多详情参考 Pillow 文档: https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html

### 转换图像大小
* 指定图像宽度和高度进行转换
* 按原图的百分比进行缩放
* 可选择是否保留原图的纵横比 Ratio

### 控制图像质量
* 输出 JPEG，WebP 等图像格式式指定输出的图像质量，即压缩率  
* 输出为 JPEG 渐进式格式

### 其他功能
* 自适应旋转图像。根据原图的 Exif 信息，自动旋转图像
   
## 按以下步骤即可完整部署  
1. 本地电脑上新建一个项目目录，并且初始化 CDK，例如  
```
mkdir cdk_img_process && cd cdk_img_process && cdk init app --language=python  
```
2. 把这些文件拷贝到新建的目录下，并替换原文件  
* setup.py
* env.js
* ./lambda/lambda_function.py
* python-pillow-6.2.1.zip 
* ./cdk_img_process/cdk_img_process_stack.py  
注意如果你的项目目录名称不是"cdk_img_process"，则 cdk_img_process_stack.py 文件不要直接替换，请打开文件替换里面的内容，但保留 class 的名称，如： class xxxxxxxStack  
注意保持以上目录结构。  
  
3. 创建虚拟环境，并安装依赖
```
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
cdk bootstrap
```
4. 部署  
```
cdk deploy
```
可以在控制台上看到新建了 CloudFormation Stack 并且创建了对应资源，大约3分钟后，创建完成。  
如果需自己定义 Bucket 名称或者 Lambda 函数名称，可以打开 cdk_img_process_stack.py ，看里面的提示信息修改。  
5. 一键清理所有资源  
```
cdk destroy
```