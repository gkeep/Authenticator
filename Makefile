BINS = bin/poc
LIBS = -lcryptopp
FLAGS = -o $(BINS)

default: do

do:
	@echo "Compiling..."
	g++ proof-of-concept/poc.cpp $(LIBS) $(FLAGS)

clean:
	@echo "Removing binaries..."
	rm $(BINS)
