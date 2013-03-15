SIMP: Simple Inventory Management Program
=========================================

Installation
------------
  1. If you haven't already, install virtualenvwrapper
     `sudo pip install virtualenvwrapper`
  1. Check out SIMP codebase to a folder in $PROJECT\_HOME
     `git clone http://www.github.com/mverteuil/SIMP/ $PROJECT_HOME/SIMP`
  1. Make a virtual environment for SIMP
     `mkvirtualenv SIMP`
  1. Change directories to the SIMP project folder
     `cd $PROJECT_HOME/SIMP`
  1. Associate the SIMP project folder with the virtual environment
     `setvirtualenvproject $VIRTUAL_ENV`
  1. Install dependencies
     `pip install -r requirements.pip`
  1. Build documentation
     `cd docs; make html; cd ..;`
  1. Create the database and set up an administrator account
     `python manage.py syncdb; python manage.py migrate;`
  1. Run the server
     `python manage.py runserver 0:8000`
  1. Navigate to the running server at http://localhost:8000/admin/


Build Status
------------
[![Build Status](https://travis-ci.org/mverteuil/SIMP.png?branch=master)](https://travis-ci.org/mverteuil/SIMP)
