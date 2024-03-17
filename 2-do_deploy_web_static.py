#!/usr/bin/python3
"""Module that includes a Fabric Script."""
from fabric.api import local, put, run, env, sudo


env.hosts = ['52.90.14.162', '100.25.162.4']


def do_pack():
    """Generates a .tgz archive from the contents of `web_static` directory"""
    local("mkdir -p versions")
    local("tar -cvzf versions/web_static_$(date +%Y%m%d%H%M%S).tgz web_static")


def do_deploy(archive_path):
    """Distributes an archive to your web servers.
    Returns:
        False, if the file path `archive path` doesn't exist.
    """
    try:
        put(f"{archive_path}", "/tmp/")
        archive_file = archive_path.split('/')[1]
        archive_no_ext = archive_file.split('.')[0]
        full_archive_dir = f"/data/web_static/releases/{archive_no_ext}"
        run(f"mkdir -p {full_archive_dir}")
        run(f"tar -xzf /tmp/{archive_file} -C {full_archive_dir}/")
        run(f"rm /tmp/{archive_file}")
        run(f"mv {full_archive_dir}/web_static/* {full_archive_dir}")
        run(f"rm -r {full_archive_dir}/web_static")
        run("unlink /data/web_static/current")
        run(f"ln -sf {full_archive_dir}/ /data/web_static/current")
        return (True)
    except:
        return (False)
