from PIL import Image
 
img = Image.new('RGB', (320, 240))
pixels = img.load()
pixels[100,100] = (255,0,0)
pixels[100,100] = (0,0,0)
pixels[100,100] = (0,255,0)
img.show()

