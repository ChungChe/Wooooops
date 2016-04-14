CC = g++
CFLAGS = -O2 -Wall -lcurl -lgumbo -lgq -MMD
INC = -I /usr/local/include/gq -L /usr/local/lib
mem: url_utility.o html_parser.o main.o
	${CC} url_utility.o html_parser.o main.o ${CFLAGS} ${INC} -o mem
url_utility.o: url_utility.cpp
	${CC} url_utility.cpp ${CFLAGS} ${INC} -c
html_parser.o: html_parser.cpp
	${CC} html_parser.cpp ${CFLAGS} ${INC} -c
main.o: main.cpp
	${CC} main.cpp ${CFLAGS} ${INC} -c
clean:
	@rm -fr *.o
