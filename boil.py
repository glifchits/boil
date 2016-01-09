import io
import sys
import shutil
import zipfile
import requests


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
    releases_url = "https://api.github/repos/{}/releases/latest"
    r = requests.get(releases_url)
    zipball_url = r.json().get('zipball_url', None)
    if zipball_url is None:
        raise ValueError("Couldn't get zipball url")
    z = requests.get(zipball_url)
    assert z.ok, "Downloading zipball was not ok"
    zipball = zipfile.ZipFile(io.BytesIO(z.content))
    return zipball


def dump_zip_contents_into_cwd(zipball):
    tmp = './tmp'
    zipball.extractall(tmp)
    walk = os.walk(tmp)
    _, subfolders, _ = next(walk)
    folder = subfolders[0]
    walk = os.walk(os.path.join(tmp, folder))
    # copy files from inside this walk to the cwd
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
        exit(str(e))
