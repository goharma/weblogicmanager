sed -n '/<jdbc-store>/,/<\/jdbc-store>/ { /<target>/p }' config.xml


grep -n 'persistent-store' <file> | awk -F: '{print $1+3}' | xargs -I {} sed -n '{}p' <file>
