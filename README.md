# atori

… is a self-host TeX compiling service with 

  - Simple HTTP API
  - Result caching
  - Missing package detection (WIP)

and other experimental features.

It is designed to use this with [unamed], a simple JavaScript library that 
finds (La)TeX snippets in a HTML document, turn them into complete (La)TeX 
documents, feeds into this and then get neatly fitted SVGs.

## Motivation

It is inspired by the [karasu][ref-1] project, which allows mixed Markdown and 
LaTeX in the same document; karasu solved this problem by converting LaTeX 
contents to SVGs first. 

[ref-1]: https://github.com/Krasjet/karasu

Comparing Markdown and TeX, Markdown is minimalistic, but TeX is far more 
powerful than Markdown. Being able to use both in the same document would be 
quite interesting. The karasu project managed to do this, but adapting that to 
other environments turns out to be tricky because it is written in Haskell.  
I managed to write a simple Lua filter for Pandoc that does the same, but I 
still don't like the solution. Is there a chance that we can render them on 
the fly?

Other notable projects while I was creating these two projects:

  - [GladTeX][ref-2], a program with similar approach; however it claims to 
    have only partial Unicode support.
  - [LaTeX SVG][ref-3], a Pandoc filter that works in a similar way, written in 
    Haskell.
  - [TinyTeX][ref-4], a customized TeX distribution that manages to implement 
    auto-installing required packages.

[ref-2]: https://github.com/humenda/GladTeX
[ref-3]: https://github.com/phadej/latex-svg
[ref-4]: https://github.com/yihui/tinytex

## General requirement

You will need

  - Python3
  - pip3
  - TeX Live distro. Currently it is recommended to use the full distro, but 
    once the missing package detection is available, you can use a minimized 
    distro for faster deployment. At the very minimum, you should have `tex`, 
    `latex`, `pdftex` and `dvisvgm` available in your `PATH`.
  - Redis, unless you want to use alternative cache backend.

### Setup development env

```bash
# Setup virtual env.
python3 -m venv venv
# Activate the virtual env.
. venv/bin/acvitave
# Install dependencies. 
# Currently, we depend on Flask, Flask-Cache and redis.
# Redis is not required if you choose other caching method.
pip3 install -r requirements.txt
```

### Deploy to production env

WIP

```bash
gunicorn -w 4 -b 127.0.0.1:8080 -k gevent app:app
```
