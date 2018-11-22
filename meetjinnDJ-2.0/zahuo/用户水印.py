import PIL
from PIL import ImageFont,Image,ImageDraw

#设置字体，如果没有，也可以不设置
font = ImageFont.truetype(r"../static/font/123.ttf",25)
imageFile = r"../s1.jpeg"
im1=Image.open(imageFile)
draw = ImageDraw.Draw(im1)
a=im1.size
print (a)
draw.text((a[0]-120,a[1]-40),"@ceshi1",(255,255,255),font=font)
draw = ImageDraw.Draw(im1)
im1.save("target.png")