CC = g++
CFLAGS = -O3 -g -Wall -std=c++11
#LIBS =
SRCS = \
       bee.cpp \
       track.cpp \
       main.cpp
PROG = bin/u

$(PROG):$(SRCS)
	$(CC) $(CFLAGS) -o $(PROG) $(SRCS) #$(LIBS)

clean:
	rm $(PROG)
