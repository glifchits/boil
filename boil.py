import io
import os
import sys
import shutil
import zipfile
import requests

tmp = './tmp'


def exit(msg, code=1):
    sys.stderr.write("{}\n".format(msg))
    sys.exit(code)


def repo_exists(github_repo):
    if len(github_repo.split('/')) != 2:
        raise ValueError("Invalid Github repo: expected format `owner/repo`")
    repo_url = "https://api.github.com/repos/{}".format(github_repo)
    r = requests.get(repo_url)
    if r.status_code == 200:
        return r.json()
    if r.status_code == 404:
        raise LookupError('Repo "{}" was not found'.format(github_repo))


def get_master_zipfile(github_repo):
    """
    :returns: [zip file]
    """
    zip_url = "https://github.com/{}/archive/master.zip".format(github_repo)
    z = requests.get(zip_url)
    assert z.ok, "Downloading zipball was not ok"
    zipball = zipfile.ZipFile(io.BytesIO(z.content))
    return zipball


def dump_zip_contents_into_cwd(zipball):
    cwd = os.getcwd()
    zipball.extractall(tmp)
    walk_zip = os.walk(tmp)
    _, subfolders, _ = next(walk_zip)
    folder = subfolders[0]
    # copy files from inside this walk to the cwd
    walk_subfolder = os.walk(os.path.join(tmp, folder))
    rootfolder, boilerplate_folders, boilerplate_files = next(walk_subfolder)
    for folder in boilerplate_folders:
        srcfolderpath = os.path.join(cwd, rootfolder, folder)
        destfolderpath = os.path.join(cwd, folder)
        shutil.copytree(srcfolderpath, destfolderpath)
    for f in boilerplate_files:
        srcfilepath = os.path.join(cwd, rootfolder, f)
        destfilepath = os.path.join(cwd, f)
        shutil.copy(srcfilepath, destfilepath)
    shutil.rmtree(tmp)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        exit('Need a Github repo as argument')

    github = sys.argv[1]
    try:
        repo_info = repo_exists(github)
        tempzip = get_master_zipfile(github)
        dump_zip_contents_into_cwd(tempzip)
    except Exception as e:
        if os.path.isdir(tmp):
            shutil.rmtree(tmp)
        exit(str(e))
