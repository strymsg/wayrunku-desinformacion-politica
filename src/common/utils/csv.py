"""
 This file is part of Wayrunku.

 Wayrunku is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

 Wayrunku is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License along with Wayrunku. If not, see <https://www.gnu.org/licenses/>.
"""
import csv
from os.path import exists


def csv_write_headers(filename="bbc.csv", headers=["title", "content", "date", "categories", "url"],
                  replace_file=False):
    replace_flag = "w" if replace_file else "a"
    with open(filename, replace_flag, encoding="UTF-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)


def csv_columnnames_exist(
        filename="bbc.csv",
        headers=["title", "content", "date", "categories", "url"]):
    file_exists = exists(filename)
    if not file_exists:
        return False

    with open(filename, "r", encoding="UTF-8", newline="") as f:
        firstline = f.readline().rstrip()
        print(f"firstline of '{filename}': {firstline}")
        return firstline == ",".join(headers)


def append_to_csv(article, keys=["title", "content", "date", "categories", "url"], filename="bbc.csv"):
    '''Agrega el contenido de un artículo como nueva fila del archivo dado, seleccionado
    las propiedades del articulo.
    :article (dictionary) con title, categories, content, date and url
    :
    '''
    with open(filename, 'a', encoding='UTF-8', newline='') as f:
        writer = csv.writer(f, delimiter=',')

        if "categories" in keys:
            article["categories"] = ",".join(article["categories"])

        row = [article[k] for k in keys]
        writer.writerow(row)
        print(f' —> article "{article["title"]}" added to {filename}')
