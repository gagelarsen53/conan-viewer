import re
import os
import subprocess
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('remote', help='conan remote to be searched and viewed')
parser.add_argument('-p', '--pattern', dest='pattern', help='pattern to be searched for', default=None)
args = parser.parse_args()

re_conan_package = r"(.*?)/(.*?)@(.*?)/(.*)"
selector_text = '<select class="form-control" id="conan-package-selector">\n'

with open("conans/list.txt", "w") as of:
    if args.pattern:
        subprocess.run(['conan', 'search', '-r', str(args.remote), str(args.pattern)], stdout=of, stderr=of)
    else:
        subprocess.run(['conan', 'search', '-r', str(args.remote)], stdout=of, stderr=of)

# generate the list
with open("conans/list.txt", "r") as lf:
    for line in lf.readlines():
        p = re.match(re_conan_package, line.strip())
        if p:
            package = '{}/{}@{}/{}'.format(p[1], p[2], p[3], p[4])
            html_file = 'conans/{}-{}-{}-{}.html'.format(p[1], p[2], p[3], p[4])
            cmd = ['conan', 'search', '-r', str(args.remote), package, '--table', html_file]
            subprocess.run(cmd)
            selector_text += '\t<option value="{}">{}</option>\n'.format(html_file, package)
            print(package)
            
selector_text += '</select>\n'

with open('selector.html', 'w') as of:
    of.write(selector_text)
