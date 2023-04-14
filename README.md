![you shall not pass](assets/gandalf.jpg)

# Gandalf

Gandalf is Cape Fear Maker's Guild's access control system. This repo hosts the
server-side code. The client-side ESP8266 code is a WIP. This repo is a stripped
down fork of [makerspaceleiden's
CRM](https://github.com/MakerSpaceLeiden/makerspaceleiden-crm).

# Quick test/install

To run the latest pre-built image:
```console
$ docker run -p 127.0.0.1:80:8000 ghcr.io/cape-fear-makers-guild/gandalf:main ./loaddemo.sh
```

To build and run a containerized copy of the code:
```console
$ docker compose up -d
```
Or if you don't have docker-compose installed:
```console
$ docker build -t gandalf:latest .
$ docker run -p 127.0.0.1:80:8000 gandalf:latest ./loaddemo.sh
```

Then go to [`http://localhost/`](http://localhost/) and login using
the accounts created & shown to you during the loaddemo.sh script.

# Requirements

## Trustees

  - Create member, progress status from initial to full (i.e. with 24x7 key)
  - Checkboxes for things such as 'form on file', member-in-good-standing
  - Management of groups (e.g. people that can give instruction)
  - Creation of new machines and groups
  - Overview rfid cards

## Instructors
  - record whom you have given instruction to

## API

  - lists or OK/deny on RFID tags based on:
    - being a member
    - having a waiver on file
    - having had the proper instructions
    - the machine not being out-of-order

# Current design

  - Normal Django users; Members adds a field to that (form on file). May add
    more in the future (e.g. emergency contact).
  - Machines
    - Machines or things that you can interact with (like doors).
    - May require the waiver to be on file.
    - May require instructions
  - Entitlements
    - of a specific permit
    - Assigned to a user (owner) by an issuer.
    - issuer must have the entitlement themself.
    - issuer must ALSO have the permit specified in the permit
