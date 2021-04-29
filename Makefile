.PHONY: help release requirements clean install

#===============================================
VENV_NAME?=venv
ENV=.env
VENV_ACTIVATE=. ${VENV_NAME}/bin/activate
PYTHON=${VENV_NAME}/bin/python3
PIP=${VENV_NAME}/bin/pip3
PYCODESTYLE=${VENV_NAME}/bin/pycodestyle
PWD=$(shell pwd)
DEPENDENCES=requirements.txt
#DEPENDENCESDEV=requirements-dev.txt
include ${ENV}
RELEASE=release
SOURCE=import_coords
#===============================================

.DEFAULT: help

help:
	@echo "make install	- Build a release"
	@echo "make run	- Build a release"
	@echo "make clean	- Build a release"
	@echo "make release	- Build a release"

#===============================================

#===============================================
# Установка зависимостей для работы приложения
install:
	[ -d $(VENV_NAME) ] || python3 -m $(VENV_NAME) $(VENV_NAME)
	${PIP} install pip wheel -U
	${PIP} install -r ${DEPENDENCES}
#	${PIP} install -r ${DEPENDENCESDEV}

#===============================================
# Активация виртуального окружения для работы приложений
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

#===============================================
# Создание релиза приложения
release: clean ${SOURCE}
	mkdir ${RELEASE}
	zip -r ${RELEASE}/${SOURCE}-$(shell date '+%Y-%m-%d').zip \
	${SOURCE} ${ENV} Makefile *.md *.in *.txt *.py
#===============================================
