# equipo!
## Dev set up
- Download Virtual Box at https://www.virtualbox.org/wiki/Downloads
- Download Vagrant at https://www.vagrantup.com/downloads.html
- Clone this repo and cd into the directory that has Vagrantfile in it
- `vagrant up`
- 'vagrant ssh'
- 'cd /vagrant/src'
- `source setup.sh`
- answer yes to all questions, create a root database user when prompted and remember the password because you will be prompted for it again
- when setup.sh is done, run `./manage.py createsuperuser`
- `./manage.py runserver 0.0.0.0:8000`
- go to http://192.168.33.10:8000/admin/ and sign in with the superuser you created. 
- go http://192.168.33.10:8000/api/students/
- Explore

## Daily Workflow
- `git pull` to get any new code
- `vagrant up`
- `vagrant ssh`
- `cd /vagrant/src`
- `python manage.py migrate` if there are any database migrations
- `python manage.py runserver 0.0.0.0:8000`
- code and be merry
- `logout`
- `vagrant halt`
- commit any changes with git
