cd "$1"
mv "src_tmp.txt" "source.cpp"
g++ "source.cpp" -O -o "source" -std=c++11
