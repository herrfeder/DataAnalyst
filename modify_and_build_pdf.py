import sys
import re
import pdb
import imgkit
import os
import requests


latex_template_url = "https://raw.githubusercontent.com/herrfeder/DataAnalyst/master/eisvogel.tex"

div_tags_start_re = re.compile("<div>")
div_tags_end_re = re.compile("</div")

python_start_re = re.compile("```python")
python_start_sub = "~~~ {.python breaklines=rue bgcolor=bg fontsize=\\\\tiny}"

python_end_re = re.compile("```")
python_end_sub = "~~~"

output_start_re = re.compile(".*#nbos")
output_start_sub = "~~~ {.text breaklines=true bgcolor=win fontsize=\\\\footnotesize framesep=2mm frame=single rulecolor=att}\nOutput:"

output_end_re = re.compile(".*#nboe")
output_end_sub = "~~~"

title = sys.argv[2]
date = sys.argv[3]

imgkit_table_css = '''
tr:nth-child(even) {background-color: #f2f2f2;}
table {
    border-collapse: separate;
    border-spacing: 0;
    border: 1px solid #000;
}
th, td {
    width: 25%;
    text-align: left;
    vertical-align: top;
}

'''

markdown_header = '''---
linetitle: "Udacity Data Analyst Nanodegree"
title: {}
author: David Lassig 
date: {}
subject: "Data Analyst"
tags: [udacity]
header-includes:
    - \usepackage{{minted}}
    - \usepackage{{xcolor}}
    - \definecolor{{bg}}{{rgb}}{{0.95,0.95,0.95}}
    - \definecolor{{lin}}{{rgb}}{{0.67, 0.88, 0.69}}
    - \definecolor{{win}}{{rgb}}{{0.6, 0.73, 0.89}}
    - \definecolor{{met}}{{rgb}}{{0.93,0.79,0.69}}
    - \definecolor{{att}}{{rgb}}{{0.0,1.0,0.0}}
    - \definecolor{{vic}}{{rgb}}{{0.8,0.0,0.0}}
---
'''.format(title,date)


imgkit_options = {
        'quiet': ''
        }

pandoc_cmd="pandoc --standalone --number-sections --filter pandoc-minted -o {1} --template=eisvogel.tex --toc {0} -V toc-own-page=true -V titlepage=true -V urlcolor=cyan && pdflatex -interaction=nonstopmode -shell-escape {1}".format(sys.argv[1].split(".")[0] + "_final.md",sys.argv[1] + ".tex")


def convert_html_table_to_png(filename,filename_tablemod):

    with open(filename,'r') as f:
        content = f.read()

    DIV_EXIST=True
    it = 0
    while DIV_EXIST==True:
        it = it + 1
        start_match = div_tags_start_re.finditer(content)
        end_match = div_tags_end_re.finditer(content)
        start_match
        try:
            start_table,append_to =  next((x_start.span()[0],x_start.span()[0]-1) for x_start in start_match)
            end_table,append_from =  next((x_end.span()[1]+1,x_end.span()[1]+1) for x_end in end_match)

            html_table = content[start_table:end_table]
            imgkit.from_string(html_table,"table_{}.png".format(str(it)),options=imgkit_options,css="imgkit_table.css")

            image_link = "![](table_{}.png)\n".format(str(it)) 
            content = content[:append_to] + image_link + content[append_from:]
        
        except StopIteration:
            DIV_EXIST=False
            break

    content = markdown_header + content

    with open(filename_tablemod,'w') as f:
        f.write(content)


def convert_code_enclosing(filename):

    with open(filename,"r") as f:
        content = f.read()

    content = python_start_re.sub(python_start_sub,content)
    content = python_end_re.sub(python_end_sub,content)

    content = output_start_re.sub(output_start_sub,content)
    content = output_end_re.sub(output_end_sub,content)


    with open(filename.split(".")[0] + "_final.md","w") as f:
        f.write(content)

def remove_temporary_files():

    os.system("rm *.aux")
    os.system("rm *.log")
    os.system("rm -r _minted*")
    os.system("rm *.out")
    os.system("rm "+ sys.argv[1] + "_1")
    os.system("rm *.tex")

if __name__ == "__main__":

    filename_tablemod = sys.argv[1]+"_1"

    if not os.path.isfile("imgkit_table.css"):
        with open("imgkit_table.css","w") as f:
            f.write(imgkit_table_css)

    convert_html_table_to_png(sys.argv[1],filename_tablemod)
    convert_code_enclosing(filename_tablemod)

    if not os.path.isfile("eisvogel.tex"):
        html_content = requests.get(latex_template_url)
        with open("eisvogel.tex","w") as f:
            f.write(html_content.text.encode("utf-8"))

    os.system(pandoc_cmd)

    remove_temporary_files()
