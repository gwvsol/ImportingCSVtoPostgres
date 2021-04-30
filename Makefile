.PHONY: help release requirements clean install

#===============================================
VENV_NAME?=venv
ENV=.env
VENV_ACTIVATE=. ${VENV_NAME}/bin/activate
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3
PYCODESTYLE=${VENV_NAME}/bin/pycodestyle
PYFLAKES=${VENV_NAME}/bin/pyflakes
PWD=$(shell pwd)
DEPENDENCES=requirements.txt
DEPENDENCESDEV=requirements-dev.txt
SETUP=setup.py
MAKEFILE=Makefile
README=README.md
include ${ENV}
RELEASE=release
SOURCE=import_coords
#===============================================

.DEFAULT: help

help:
	@echo "make install	- Installing dependencies"
	@echo "make install-dev - Installing dependencies for code validation"
	@echo "make uninstall	- Removal"
	@echo "make run	- Run the app"
	@echo "make check	- Checking the code"
	@echo "make clean	- Cleaning up garbage"
	@echo "make release	- Creating a release"

#===============================================

#===============================================
# Установка зависимостей
install:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -r ${DEPENDENCES}

# Установка зависимостей для проверки кода
install-dev:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -r ${DEPENDENCESDEV}

#===============================================
# Активация виртуального окружения
venv: ${VENV_NAME}/bin/activate
$(VENV_NAME)/bin/activate: ${SETUP}
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -e .
	${VENV_ACTIVATE}

# Запуск приложения
run: ${SOURCE} ${SETUP} venv
	${PYTHON} -m ${SOURCE}

#===============================================
# Очистка мусора
clean:
#	rm -fr dist
#	rm -fr build
	rm -fr .eggs
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
	rm -fr ${RELEASE}

# Удаление
uninstall:
	make clean
	rm -fr venv

#===============================================
# Проверка кода
check: ${PYCODESTYLE} ${PYFLAKES} ${SOURCE}
	@echo "==================================="
	${PYCODESTYLE} ${SOURCE} ${SETUP}
	${PYFLAKES} ${SOURCE} ${SETUP}
	@echo "=============== OK! ==============="

#===============================================
# Создание релиза
release: clean ${SOURCE}
	mkdir ${RELEASE}
	zip -r ${RELEASE}/${SOURCE}-$(shell date '+%Y-%m-%d').zip \
	${SOURCE} ${ENV} ${MAKEFILE} ${README} *.txt ${SETUP}
#===============================================
