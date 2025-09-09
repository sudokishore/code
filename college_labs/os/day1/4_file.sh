#!/bin/bash

touch file1.txt

cat > file1.txt <<EOF
Hello World!
Welcome
Linux Shell
EOF

cat file1.txt
