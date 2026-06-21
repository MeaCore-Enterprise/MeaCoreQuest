from PIL import Image
import os

def extract_and_resize(input_path, output_path, target_size=(32, 32)):
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
    
    with Image.open(input_path) as img:
        # Para las hojas generadas por AI, intentamos detectar el primer sprite coherente
        # Usualmente están en un grid. Vamos a extraer el frame (0,0) asumiendo un tamaño proporcional
        w, h = img.size
        # Si la imagen es 1920x1920 y parece una hoja de sprites, el primer frame suele estar arriba a la izquierda.
        # Vamos a tomar un área representativa y redimensionarla a 32x32.
        # Para warrior_v3, mage_v3, archer_v3, extraemos el primer frame.
        
        # Un frame de 32x32 en una imagen de 1920 es muy pequeño. 
        # Pero la IA genera sprites grandes que parecen pixel art.
        # Vamos a dividir la imagen en un grid de ej. 8x8 y tomar el primero.
        frame_w = w // 8
        frame_h = h // 8
        
        sprite = img.crop((0, 0, frame_w, frame_h))
        # Limpiamos bordes si hay transparencia parcial o artefactos
        sprite = sprite.resize(target_size, Image.NEAREST)
        sprite.save(output_path)
        print(f"Processed {input_path} -> {output_path}")

# Definimos los mapeos
mappings = {
    "/home/ubuntu/MeaCoreQuest/assets/warrior_v3.png": "/home/ubuntu/MeaCoreQuest/assets/warrior_32x32_v3.png",
    "/home/ubuntu/MeaCoreQuest/assets/mage_v3.png": "/home/ubuntu/MeaCoreQuest/assets/mage_32x32_v3.png",
    "/home/ubuntu/MeaCoreQuest/assets/archer_v3.png": "/home/ubuntu/MeaCoreQuest/assets/archer_32x32_v3.png",
    "/home/ubuntu/MeaCoreQuest/assets/slime_v3.png": "/home/ubuntu/MeaCoreQuest/assets/slime_32x32_v3.png",
    "/home/ubuntu/MeaCoreQuest/assets/skeleton_v3.png": "/home/ubuntu/MeaCoreQuest/assets/skeleton_32x32_v3.png"
}

for inp, outp in mappings.items():
    extract_and_resize(inp, outp)
