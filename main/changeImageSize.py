from PIL import Image

# 打开图像
original_image = Image.open('sand.png')

# 缩小图像尺寸
new_width = int(original_image.width * 1)
new_height = int(original_image.height * 1.1)
small_image = original_image.resize((new_width, new_height))

# 水平翻转图像
# flipped_image = original_image.transpose(Image.FLIP_LEFT_RIGHT)

# 保存翻转后的图像到文件
# flipped_image.save('fishSize3.png')

# 保存图像
small_image.save("sand.png")
