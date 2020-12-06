# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

from flask import Flask, request
from flask_caching import Cache
import hashlib
import os
import os.path
import subprocess
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config.from_mapping({
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 3600,
    'CACHE_KEY_PREFIX': 'atori.py-',
    'CACHE_REDIS_URL': 'redis://localhost:6379/6',
    'MAX_CONTENT_LENGTH': 1 << 20 # 1MiB, not sure if anyone will have this large files
})
cache = Cache(app)

def hash_file(f):
    chksum = hashlib.sha256(f.read()).hexdigest()
    # Reset stream current pos, so we can read it again
    f.stream.seek(0)
    return chksum

def cache_key(f, engine):
    return f"{engine}-{hash_file(f)}"

def make_dvi(f, chksum, engine = 'latex'):
    """
    Produce a dvi from the given file
    """
    work_dir = os.path.join(tempfile.gettempdir(), 'atori.py', chksum)
    os.makedirs(work_dir, exist_ok = True)
    safe_name = secure_filename(f.filename)
    doc_path = os.path.join(work_dir, safe_name)
    if not os.path.exists(doc_path):
        f.save(doc_path)
    tex_compile = subprocess.run([engine, '-no-shell-escape', safe_name], cwd = work_dir, stdout = subprocess.DEVNULL, stderr = subprocess.STDOUT)
    tex_compile.check_returncode() # Ensure exit on zero
    base_name, ext = os.path.splitext(safe_name)
    return os.path.join(work_dir, f"{base_name}.dvi")

def make_svg(file_path):
    dvi_to_svg = subprocess.run(['dvisvgm', '--no-font=1', '--clipjoin', '--bbox=min', '--exact', '--stdout', file_path], capture_output = True)
    dvi_to_svg.check_returncode()
    return dvi_to_svg.stdout.decode("utf-8")

@cache.cached(make_cache_key = cache_key)
def process_tex(f, engine):
    return make_svg(make_dvi(f, hash_file(f)))

@app.route('/', methods = ['GET', 'POST'])
def root():
    if 'tex' in request.files:
        f = request.files['tex']
        if f.filename != '' and f.filename.endswith('.tex'):
            return process_tex(f, 'latex'), { 'Content-Type': 'image/svg+xml; charset=utf-8' }
        else:
            return 'Only TeX documents and associated files are allowed', 400
    else:
        return 'No TeX document uploaded', 400

if __name__ == '__main__':
    print('Deploying to production environment is NYI.')
