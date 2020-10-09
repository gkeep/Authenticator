do:
	@echo "Compiling..."
	g++ proof-of-concept/poc.cpp -o bin/poc -lcryptopp

clean:
	@echo "Removing binaries..."
	rm bin/poc
