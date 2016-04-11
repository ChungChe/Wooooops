CC = g++
CFLAGS = -O2 -Wall -lcurl -lxml2
INC = -I /usr/include/libxml2
mem: mem.o
	${CC} mem.o ${CFLAGS} ${INC} -o mem
mem.o: mem.cpp
	${CC} mem.cpp ${CFLAGS} ${INC} -lpthread -c
clean:
	@rm -fr *.o
