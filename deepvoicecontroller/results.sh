cd Weights
ls | cat | cut -d'-' -f2 | grep  -o '^[0-9]\+\.[0-9]\+' > ../results.txt
cd -
