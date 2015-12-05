# from --swift list
python hubic.py --swift -- list default | egrep '.avi$|.mp4$|.mkv$|.wmv$|.mpg$|.mpeg$|.rmvb$|.rm$' > filelist
# only output name & md5
cat filelist | xargs -t -I % python hubic.py --swift -- stat default % | egrep 'Object:|ETag:' | awk -F ': ' 'BEGIN{count=0}{count=(count+1)%2; if(count==1){printf("\"%s\" ",$2);}else{printf("%s\n",$2)}}' > ~/hubic_md5s
# change order. md5 first, name second
cat ~/hubic_md5s | awk '{printf("%s ", $NF); for(i=1;i<NF;++i)printf("%s ", $i); printf("\n"); }' | sort > ~/hubic_md5s_sorted
# remove lines that contains Bakup/
sed --in-place '/Bakup\//d' ~/hubic_md5s_sorted
# remove md5's double quote
cat ~/hubic_md5s_sorted | awk '{gsub("\"","",$1);print $1,$2}' > ~/hubic_md5_fil