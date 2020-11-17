# Wagtail-based CMS for [newamerica.org](https://www.newamerica.org/)

## Contents

- [Dependencies](#dependencies)
- [Back-end setup](#back-end-setup)
- [Front-end setup](#front-end-setup)

Old instructions for back-end setup without Vagrant can be found [here](https://github.com/newamericafoundation/newamerica-cms/blob/80311b9a4f9a62d4a9651d2aba01e2d8ec9bb2f4/README.md).

## Dependencies

Back-end

- [Vagrant](https://www.vagrantup.com/downloads)
- [VirtualBox](https://www.virtualbox.org/wiki/Downloads)

Front-end

- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)

## Back-end setup

_Old instructions for back-end setup without Vagrant can be found [here](https://github.com/newamericafoundation/newamerica-cms/blob/80311b9a4f9a62d4a9651d2aba01e2d8ec9bb2f4/README.md)._

Make sure you have the latest version of Vagrant installed.
The base box only works with VirtualBox so you will need that too.

After cloning the site, run the following commands to set up the Vagrant box,
pull data from staging then launch the web server.

```bash
vagrant up
vagrant ssh
fab pull-production-data
djrun
```

You may also want to run `fab pull-production-images`, but it downloads a few GB of images so you may not want to.

Note that `./manage.py` does work in the box if you want to use it that way,
it's been aliased to `dj` for convenience. The `djrun` command is an alias of
`./manage.py runserver 0.0.0.0:8000`.

Within Vagrant, all of PostgreSQL's utilities are all configured and `psql` is
configured to use the 'newamerica-cms' database by default.

To exit Vagrant and shut off the virtual machine:

```bash
exit
vagrant halt
```

## Front-end setup

Install front-end dependencies

```bash
npm install
```

Grab static assets (fonts, icons, etc.). This requires `aws configure`.

```bash
npm run get-static
```

Start webpack for development

```bash
npm run dev
```
