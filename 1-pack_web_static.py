#!/usr/bin/python3
"""Module that includes a Fabric Script."""
from fabric.api import local


def do_pack():
    """Generates a .tgz archive from the contents of `web_static` directory"""
    local("mkdir -p versions", capture=False)
    local("tar -cvzf versions/web_static_$(date +%Y%m%d%H%M%S).tgz web_static")
