CC = g++
CFLAGS = -O2 -Wall -lcurl -lgumbo -lgq -MMD
INC = -I /usr/local/include/gq -L /usr/local/lib
mem: mem.o
	${CC} mem.o ${CFLAGS} ${INC} -o mem
mem.o: mem.cpp
	${CC} mem.cpp ${CFLAGS} ${INC}  -c
clean:
	@rm -fr *.o
