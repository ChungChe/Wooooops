./rclone lsd amazon:/ | awk '{$1=$2=$3=$4="";printf("%s\n", substr($0,5))}' > ~/ama_root
sed --in-place '/Videos/d' ~/ama_root
sed --in-place '/Documents/d' ~/ama_root
sed --in-place '/Fonts/d' ~/ama_root
sed --in-place '/Photos/d' ~/ama_root
sed --in-place '/uncategorized/d' ~/ama_root
sed --in-place '/Movies/d' ~/ama_root
sed --in-place '/Pictures/d' ~/ama_root
sed --in-place '/Apen/d' ~/ama_root

cat ~/ama_root | xargs -i ./rclone lsd amazon:/\{} | awk '{$1=$2=$3=$4="";printf("%s\n",substr($0,5))}' >> ~/new_files
