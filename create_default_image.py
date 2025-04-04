from PIL import Image, ImageDraw, ImageFont
import os

# Créer une image 400x600 avec un fond blanc
img = Image.new('RGB', (400, 600), color='white')
d = ImageDraw.Draw(img)

# Ajouter du texte
text = "Tenue par défaut"
# Utiliser une police système par défaut
d.text((100, 280), text, fill='black')

# Créer le dossier static/images s'il n'existe pas
os.makedirs('static/images', exist_ok=True)

# Sauvegarder l'image
img.save('static/images/default_outfit.jpg') 