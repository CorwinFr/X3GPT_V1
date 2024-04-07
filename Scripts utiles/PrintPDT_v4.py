import os
import requests
from bs4 import BeautifulSoup
import pdfkit
from PyPDF2 import PdfMerger
from urllib.parse import unquote

# Configuration pour pdfkit
config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')

options = {
    'no-images': '',  # Désactive le chargement des images
    'disable-external-links': '',  # Désactive les liens externes
    'disable-javascript': '',  # Désactive le JavaScript
    'no-background': '',  # Désactive le fond de page
    'disable-internal-links': '',  # Désactive les liens internes
    'disable-plugins': '',  # Désactive les plugins comme Flash
    'disable-local-file-access': '',  # Empêche l'accès aux fichiers locaux
    'no-stop-slow-scripts': '',  # Ne pas arrêter les scripts lents
    'no-print-media-type': '',  # N'utilise pas le type de média print pour le CSS
}

# Set pour suivre les pages visitées
visited = set()

def save_pdf(path, depth, current_depth):
    path = unquote(path)

    if path in visited or current_depth > depth:
        return
    visited.add(path)

    # Gérer les chemins locaux
    if not path.startswith('http'):
        if not os.path.isabs(path):
            path = os.path.abspath(path)

        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            content = file.read()
        soup = BeautifulSoup(content, 'html.parser')

        file_name = f'page_{len(visited)}.html'
        with open(file_name, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        links = soup.find_all('a', href=True)
        for link in links:
            next_url = os.path.join(os.path.dirname(path), unquote(link['href']))
            # Vérifie que le lien ne remonte pas dans l'arborescence (pas de '..') et qu'il pointe vers un fichier existant
            if os.path.exists(next_url) and not '..' in os.path.relpath(next_url, os.path.dirname(path)):
                save_pdf(next_url, depth, current_depth + 1)
# Paramètres initiaux
                
               
url = ''
depth = 10

# Lancement du processus de sauvegarde
save_pdf(url, depth, 0)

# Conversion en PDF par lots et fusion
pdf_files = [f'page_{i}.html' for i in range(1, len(visited) + 1)]
pdf_merger = PdfMerger()

for i in range(0, len(pdf_files), 50):  # Traitement par lots de 50
    batch = pdf_files[i:i+50]
    if batch:
        intermediate_pdf = f'intermediate_{i//50}.pdf'
        try:
            pdfkit.from_file(batch, intermediate_pdf, configuration=config, options=options)
        except Exception as e:
            print(f"Error converting {batch} to {intermediate_pdf}: {e}")
        pdf_merger.append(intermediate_pdf)

# Création du fichier PDF final
output_pdf = ''
pdf_merger.write(output_pdf)
pdf_merger.close()

# Nettoyage des fichiers intermédiaires
for i in range(len(pdf_files) // 50 + 1):
    os.remove(f'intermediate_{i}.pdf')
