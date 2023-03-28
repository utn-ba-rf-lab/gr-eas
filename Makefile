all:
	cd build;\
	cmake ../;\
	sudo make install;\
	sudo ldconfig;\
	gnuradio-companion;

