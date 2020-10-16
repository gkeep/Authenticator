BINS = bin/poc
LIBS = -lcryptopp
FLAGS = -o $(BINS)
ARGS = "otpauth://totp/ACME%20Co:john@example.com?secret=NYO2G5NPHL556J2HSF4AWOGFOZA3SRDR&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"

default: do

do:
	@echo "Compiling..."
	g++ proof-of-concept/poc.cpp $(LIBS) $(FLAGS)

run:
	make do && bin/poc $(ARGS)

clean:
	@echo "Removing binaries..."
	rm $(BINS)
