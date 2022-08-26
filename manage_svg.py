# Script for manage phosphor icon SVG
from xml.dom import DOMException, minidom
import os
import shutil
from pathlib import Path

RED = '\033[0;31m'
ORANGE = '\033[0;33m'
NC = '\033[0m'
GREEN = '\033[0;32m'


def update_svg(path_file):
    # Update the SVG by removing the SVG tag, the 1st Rect and the tags related to Stroke
    try:
        doc = minidom.parse(path_file)
        if doc.documentElement.tagName != "svg":
            raise DOMException
        delete_stroke = []
        # Supprimes les tag qui concerne la stroke
        for elt in doc.toxml().split():
            if "stroke" in elt:
                if "/>" in elt:
                    delete_stroke.append('/>')
                    delete_stroke.append(elt.split('/>', 1)[1])
                elif ">" in elt:
                    delete_stroke.append('>')
                    delete_stroke.append(elt.split('>', 1)[1])
            else:
                delete_stroke.append(elt)
        svg_without_stroke = ' '.join(delete_stroke)

        # Removes the SVG tag and the first Rect from the svg
        array_split = svg_without_stroke.split('<')
        svg_final = []
        for i, elt in enumerate(array_split):
            if i == len(array_split) - 1:
                break
            if i > 3:
                svg_final.append(elt)

        svg_final.insert(0, '')
        svg_final = '<'.join(svg_final)
        return svg_final
    except Exception:
        raise DOMException


def create_svg(svg_data, svg_path):
    with open(svg_path, 'w') as f:
        f.write(svg_data)


def create_import_object(svg_name, svg_data):
    # Create the object data in str which will be integrated in the final object to manage the icon imports
    return "'" + svg_name[:-4] + "':()=>{ return '"+svg_data+"'},"


def create_import_function(case_list):
    # Created in str the ImportSvg function which will allow to manage via an object the icon imports
    base = """
interface SvgObject {
[key: string]: Function;
}
export function importSvg(icon: string) {
const svg = {
    """
    for case in case_list:
        base += case
        base += '\n'
    base += """} as SvgObject;
return svg[icon]();
}
"""
    return base


def manage_svg(lst_svg, icon_repo, keep_svg, delete_repo_svg):
    # Browse the file list and process SVGs
    path_to_svg_repo = icon_repo + '/svg_minify'
    if delete_repo_svg and os.path.isdir(path_to_svg_repo):
        shutil.rmtree(path_to_svg_repo)
    if keep_svg and not os.path.isdir(path_to_svg_repo):
        os.mkdir(path_to_svg_repo)
    lst_data_svg = []
    for file in lst_svg:
        file_path = icon_repo + '/' + file
        svg_data = None
        try:
            svg_data = update_svg(file_path)
        except Exception:
            print(
                f"{RED}[X] |{file_path.rsplit('/', 1)[-1]}| est un fichier SVG mal formaté{NC}")
        if svg_data and keep_svg:
            create_svg(svg_data, path_to_svg_repo + '/' + file) 
            print(
                f"[-] {GREEN}|{file_path.rsplit('/', 1)[-1]}| a été traité{NC}")
        lst_data_svg.append({file: svg_data})
    return lst_data_svg

def manage_import(lst_svg, icon_repo):
    lst_import = []
    for file in lst_svg:
        lst_import.append(create_import_object(list(file.keys())[0], list(file.values())[0]))
    import_file = create_import_function(lst_import)
    import_file_name = icon_repo + '/importSvg.ts'
    if os.path.exists(import_file_name):
        os.remove(import_file_name)
    with open(import_file_name, 'w') as f:
        f.write(import_file)


def main():
    print("""
#################################################################
#                                                               #
#                Manage Phosphor icon SVG                       #
#                                                               #
#      Reduced the size of SVGs by 3 by removing SVGs,          #
#      unnecessary Rect and stroke attributes to provide        #
#      scalability.   Created a Typescript file with SVG        #
#      minifier with a function to load SVG paths               #
#                                                               #
#                                                               #
#################################################################
          """)

    # Checks if the file provided exists
    icon_repo = input("Path to the folder containing the SVGs to be processed : ")
    if not os.path.isdir(icon_repo):
        exit(
            f"{RED}[X] Errorr : the repository {NC}{ORANGE}'{icon_repo}'{NC}{RED} does not exist{NC}")
    print(
        f"\n{GREEN}[-] the repository to be processed is  {NC}{ORANGE}'{icon_repo}'{NC}")

    # Creates a list of existing files in the repository and keeps only the SVGs
    lst_svg = []
    files = Path(icon_repo).glob('*')

    for file in files:
        if file.name[-4:] == ".svg":
            lst_svg.append(file.name)
    if len(lst_svg) == 0:
        exit(
            f"{RED}[X] No SVG file to process in the {NC}{ORANGE}'{icon_repo}'{NC}{RED} repository{NC}")

    # CHOICE 1: Create SVG minifier files
    while True:
        keep_svg = input(
            f"\nDo you want to create minified SVGs in separate files ? [Y]es | [N]o : ")
        if keep_svg.lower().strip() == 'y':
            keep_svg = True
            print(
                f"{GREEN}[-] The created files will be stored inside the {NC} {NC}{ORANGE}'{icon_repo}/svg_minify'{NC}{GREEN} repository{NC}")
            break
        elif keep_svg.lower().strip() == 'n':
            keep_svg = False
            print(f"{GREEN}[-] No minified SVG files will be created. {NC}")
            break
        else:
            continue
        
    # CHOIX 1.1: Clear svg_minify repository
    delete_repo_svg = False
    if keep_svg:
        while True:
            delete_repo_svg = input(
                f"\n ifthe {ORANGE}'{icon_repo}/svg_minify'{NC} repository already exists, do you want to reset it ? [Y]es | [N]o : ")
            if delete_repo_svg.lower().strip() == 'y':
                delete_repo_svg = True
                print(
                    f"{GREEN}[-] The {NC} {NC}{ORANGE}'{icon_repo}/svg_minify'{NC} repository will be reset")
                break
            elif delete_repo_svg.lower().strip() == 'n':
                delete_repo_svg = False
                print(f"{GREEN}[-] The created files will be added to those already existing in the folder: {NC}{ORANGE}'{icon_repo}/svg_minify'{NC}")
                break
            else:
                continue

    # CHOICE 2: Creating a TypeScript import file
    while True:
        create_import_file = input(
            f"\nWould you like to create a Typescript file to facilitate SVG imports ? [Y]es | [N]o : ")
        if create_import_file.lower().strip() == 'y':
            create_import_file = True
            print(
                f"{GREEN}[-] a {ORANGE}'importSvg.ts'{NC} {GREEN}file will be created inside the repository: {NC} {NC}{ORANGE}'{icon_repo}'{NC}")
            break
        elif create_import_file.lower().strip() == 'n':
            create_import_file = False
            print(f"{GREEN}[-] No Typescript file will be created{NC}")
            break
        else:
            continue
    print("\n[-] Starting SVG processing...")
    lst_data_svg = manage_svg(lst_svg, icon_repo, keep_svg, delete_repo_svg)
    print(f"\n{GREEN}[SUCCES] Processing of SVG files is finished{NC}")
    if create_import_file:
        print("\n[-] Start creating the TypeScript import file...")
        manage_import(lst_data_svg, icon_repo)
        print(f"\n{GREEN}[SUCCES] The import system file {NC}{ORANGE}'importSvg.ts'{NC}{GREEN}has been successfully created in the repository : {NC}{ORANGE}{icon_repo}{NC}")


if __name__ == "__main__":
    main()
