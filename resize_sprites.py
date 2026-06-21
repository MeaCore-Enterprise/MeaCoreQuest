from PIL import Image
import os

def resize_sprite(path, size=(32, 32)):
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return
    
    img = Image.open(path)
    # Use NEAREST resampling to maintain pixel art quality
    img_resized = img.resize(size, Image.NEAREST)
    img_resized.save(path)
    print(f"Resized {path} to {size}")

sprites = [
    "/home/ubuntu/MeaCoreQuest/assets/warrior_32x32.png",
    "/home/ubuntu/MeaCoreQuest/assets/mage_32x32.png",
    "/home/ubuntu/MeaCoreQuest/assets/archer_32x32.png",
    "/home/ubuntu/MeaCoreQuest/assets/slime_enemy_32x32.png"
]

for sprite in sprites:
    resize_sprite(sprite)
