grep -n 'persistent-store' <file> | awk -F: '{print $1+3}' | xargs -I {} sed -n '{}p' <file>
