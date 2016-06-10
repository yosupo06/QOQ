cd "$1"
mv "src_tmp.txt" "source.d"
ldc2 "source.d" -O
