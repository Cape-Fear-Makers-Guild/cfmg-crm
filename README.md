# Quick test/install

To build and run a containerized copy of the code:
```console
$ docker compose up -d
```
Or if you don't have docker-compose installed:
```console
$ docker build -t cfmg:latest .
$ docker run -p 127.0.0.1:80:8000 cfmg:latest ./loaddemo.sh
```

Then go to [`http://localhost/`](http://localhost/) and login using
the accounts created & shown to you during the loaddemo.sh script.

# About

This is the server-side of the Cape Fear Maker's Guild's access control
system. The client-side code is a WIP. This repo is a stripped down fork of
[makerspaceleiden's
CRM](https://github.com/MakerSpaceLeiden/makerspaceleiden-crm).

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
