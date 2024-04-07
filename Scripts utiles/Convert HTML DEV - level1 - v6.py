import os
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup, NavigableString, Tag

# Ajouter une variable globale pour suivre les fichiers déjà traités
processed_files = set()

def extract_and_process_content(node):
    text = ""
    if isinstance(node, NavigableString):
        content = node.string
        if content:
            if node.parent.name == 'code':
                # Ajouter l'espace après le contenu de <code>
                text += content + (' ' if not content.endswith(' ') else '')
            else:
                text += content.strip() + ' '
    elif isinstance(node, Tag):
        if node.name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            for child in node.children:
                text += extract_and_process_content(child)
            text += "\n\n"
        elif node.name == 'li':
            for child in node.children:
                text += extract_and_process_content(child)
            text += "\n"
        elif node.name == 'ul':
            for child in node.children:
                text += extract_and_process_content(child)
            text += "\n"
        elif node.name == 'br':
            text += "\n"
        elif node.name == 'table':
            for row in node.find_all('tr', recursive=False):
                cells = [extract_and_process_content(cell) for cell in row.find_all(['td', 'th'], recursive=False)]
                text += ' | '.join(cells).strip() + "\n"
            text += "\n"
        elif node.name in ['td', 'th']:
            cell_text = ''.join([extract_and_process_content(child) for child in node.children]).strip()
            text += cell_text + " "
        elif node.name in ['code', 'strong']:
            text += ''.join([extract_and_process_content(child) for child in node.children])
        else:
            text += ''.join([extract_and_process_content(child) for child in node.children])
    return text

def process_html_file(file_path, output_file, base_directory, level=0, max_level=2):
    if level > max_level or file_path in processed_files:
        return

    # Ajouter le fichier actuel à la liste des fichiers traités
    processed_files.add(file_path)

    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file.read(), 'html.parser')
        text = extract_and_process_content(soup)

    with open(output_file, 'a', encoding='utf-8') as output:  # Append mode
        output.write(text)

    # Ne descendre que d'un niveau
    if level < max_level:
        for link_tag in soup.find_all('a', href=True):
            link = link_tag['href']
            # Construire le chemin complet pour le lien
            link_path = os.path.join(os.path.dirname(file_path), link)

            # Vérifier que le fichier existe, qu'il se trouve dans le bon répertoire et qu'il s'agit d'un fichier HTML
            if (os.path.isfile(link_path) and 
                link_path.endswith('.html') and 
                link_path.startswith(base_directory) and 
                link_path not in html_files):  # Vérifier que le lien n'est pas déjà dans la liste html_files
                process_html_file(link_path, output_file, base_directory, level + 1, max_level)


# Exemple d'utilisation
html_files = [
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_2.html',
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_3.html',    
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_4.html',   
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_5.html',   
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_6.html',   
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_7.html',   
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_8.html',           
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_9.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_10.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_11.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_12.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_13.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_14.html',     
    'C:/WORK/SAGE X3 V12/DATA/SAGE X3 V12_DATA/online-help.sageerpx3.com/erp/12/wp-static-content/static-pages/en_US/MCD/ATB_1.html',                                             
]
output_directory = 'C:/WORK/SAGE X3 V12/IA/ATB/'
start_texts_to_remove = {" Mirrored from online-help.sageerpx3", "	window.focus();", "	window[window.","} Index  Home X3"}
for html_file in html_files:
    output_file = os.path.join(output_directory, os.path.basename(html_file).replace('.html', '.txt'))
    base_directory = os.path.dirname(html_file)
    # Créer le fichier de sortie et ouvrir en mode écriture pour initialiser le contenu
    with open(output_file, 'w', encoding='utf-8') as f:
        pass
    process_html_file(html_file, output_file, base_directory)
    processed_files = set()

# Réinitialiser la liste des fichiers traités pour une nouvelle exécution du script
processed_files.clear()
