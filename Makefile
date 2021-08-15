.PHONY:
build:
	python setup.py build_ext --inplace
.PHONY:
clean:
	rm -rf build libsniff.cpython-39-x86_64-linux-gnu.so libsniff.c

.PHONY:
pypi:
	xdg-open https://pypi.org/project/libsniffpy/

.PHONY:
publish:
	poetry publish --build
