# Create folders e.g. Apen/X/XYZ
cat ~/amazon_bemoved_files | awk '{$1="";substr($2,1);print $0}' | awk 'BEGIN{FS="/"}{printf("~/bin/clouddrive.js mkdir ");printf("\"Apen/%s/",toupper(substr($2,0,1)));printf("%s", substr($1,2));for(j=2;j<NF;++j){printf("/%s/",$j);};printf("\"\n")}' | sort -u > ~/mkk
# Move files  e.g. Move files from Apen/Unordered/XYZ/XYZ-123/XYZ-123.avi to Apen/X/XYZ/
cat ~/amazon_bemoved_files | awk '{$1="";substr($2,1);print $0}' | awk 'BEGIN{FS="/"}{printf("~/bin/clouddrive.js mv \"");printf("Apen/Unordered/%s/", substr($1,2));for(i=2;i<NF;++i){printf("%s/",$i);}printf("%s",$NF);printf("\" \"Apen/%s/",toupper(substr($2,0,1)));printf("%s", substr($1,2));for(j=2;j<NF;++j){printf("/%s/",$j);};printf("\"\n")}' > ~/mmm
