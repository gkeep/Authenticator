BINS = bin/poc
LIBS = -lcryptopp -lssl -lcrypto -std=c++11
FLAGS = -o $(BINS)
ARGS = "otpauth://totp/ACME%20Co:john@example.com?secret=HXDMVJECJJWSRB3HWIZR4IFUGFTMXBOZ&issuer=ACME%20Co&algorithm=SHA1&digits=6&period=30"

default: do

do:
	@echo "Compiling..."
	g++ proof-of-concept/poc.cpp $(LIBS) $(FLAGS)

run:
	make do && bin/poc $(ARGS)

clean:
	@echo "Removing binaries..."
	rm $(BINS)
