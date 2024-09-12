find . -name "config.xml" -exec sed -n '/<jdbc-store>/,/<\/jdbc-store>/ { /<target>/p }' {} \;
