compile:
	pyinstaller main.py --onefile
run:
	./dist/main run
clean:
	rm -rf build dist