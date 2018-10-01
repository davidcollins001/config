
# this file is hardlinked (mklink /H on cmd) because windows python can't read symlink
# https://www.usenix.org/system/files/login/articles/09beazley_061-068_online.pdf

import os
import sys
import imp
from functools32 import lru_cache

# seperator for user input
SEP = ":"

# sanitise environment paths with normpath
REPO_ROOT = os.path.normcase('c:/dev/code/gazprom.mt')
CONDA_ENV_ROOT = (os.environ.get('CONDA_ENV_ROOT') or
                  os.path.normcase('c:/dev/bin/Anaconda/envs'))
VERBOSE = os.environ.get("VERBOSE")
IMPORT_BLACKLIST = os.environ.get("IMPORT_BLACKLIST", "")
REPOS = os.environ.get("REPOS", "")

IGNORE = ['build', 'dist']


# TODO: add locks
class GMTLoader(object):
    """
    Import hook to resolve local Python imports. Will search in `REPO_ROOT` for

    environment variables that changes the behaviour
    VERBOSE: print more info
    IMPORT_BLACKLIST: colon separated list of import names to ignore
        eg IMPORT_BLACKLIST gmt.grid:gmt.quant.util will mean these two
        libraries get imported from site-packages
    REPOS: colon separated list of windows paths to prepend on the search path,
        this causes that path to preferentially be searched for import

    """
    def __init__(self):
        self.repo_path = None

    @lru_cache()
    def local_repos(self, path=REPO_ROOT):
        """Find local repos by searching `REPO_ROOT` to find all packages"""

        # find root import path for repos
        def find_root(path, f):
            # recurse into dir to find setup.py to determine top level of code
            # eg pyserialise
            repo = os.path.join(path, f)
            if os.path.isdir(repo) and not f.startswith('.'):
                subdirs = os.listdir(repo)
                if "setup.py" in subdirs:  # and f not in IGNORE:
                    if VERBOSE:
                        print "found repo path: {}".format(repo)
                    return repo

                for sub in subdirs:
                    pp = find_root(repo, sub)
                    if pp:
                        return pp

        local_repos = []
        for f in os.listdir(path):
            repo = find_root(path, f)
            if repo:
                local_repos.append(repo)

        return local_repos

    def find_module(self, name, paths=None):
        """
        Search for a package in local repo path that has a location which
        maps to `name`

        Note: using paths doesn't add any performance and python sometimes sends
        us the wrong path anyway.
        """
        # running with conda env - imports should not use checked out code
        if CONDA_ENV_ROOT in os.path.normcase(sys.executable):
            return

        # if a module is listed in IMPORT_BLACKLIST import site package
        blacklist = IMPORT_BLACKLIST.split(SEP)
        if any([b for b in blacklist if name.startswith(b)]):
            return

        # prepend user specified repos
        prepend = REPOS.split(SEP)
        local_repos = prepend + self.local_repos()

        # capture calls to importlib because it breaks this import hook
        if name in ["importlib", "matplotlib.pyplot"]:
            return self

        # search local repos to find the path to load the module from
        for repo in local_repos:
            # check path exists in "repo" and is a package
            name_path = os.path.join(REPO_ROOT, repo, *name.split('.'))
            # ismodule = os.path.isfile(os.path.join(name_path) + ".py")
            isfile = os.path.isfile(os.path.join(name_path, "__init__.py"))
            isdir = os.path.isdir(name_path)
            if isfile and isdir:
                if VERBOSE:
                    print "found repo matching \"{}\" in {}".format(
                        name, name_path
                    )
                self.repo_path = os.path.join(REPO_ROOT, repo)
                return self

    def load_module(self, name, package=None):
        """
        Load module from repo path found in `find_module()`. `name` is full
        dotted import path, each part of path must separately be imported to be
        able to find the next part of the package, eg, gazprom.mt.pricing:
        gazprom must be imported, then mt and finally pricing
        """
        # capture call to importlib because it breaks this import hook
        if "importlib" in name:
            return self

        if "matplotlib.pyplot" in name:
            msg = "replacing {} with dummy function".format(name)
            print msg.center(len(name) + 6, "*")

            def dummy(*a, **k):
                pass
            return dummy

        return self._load_module(name, package=package)

    def _load_module(self, name, package=None):
        """Actually do the import of name"""
        m, mod_path = None, []
        # split the full import name and import each part separately
        # so import a.b.c requires importing a then a.b and finally a.b.c
        for n in name.split('.'):
            # build intermediate module path to be imported
            mod_path.append(n)
            mod_path_str = '.'.join(mod_path)

            # already imported up to `n` so don't need to import again
            if mod_path_str in sys.modules:
                m = sys.modules[mod_path_str]
            else:
                # select correct path, either a local repo, the path of the last
                # module imported or system path
                if self.repo_path:
                    p = [os.path.join(self.repo_path, *mod_path[:-1])]
                elif m:
                    p = [os.path.dirname(m.__file__)]
                else:
                    p = sys.path

                # only need module name, ie a, b or c from import a.b.c
                module = imp.find_module(n, p)

                if VERBOSE:
                    print "loading module \"{}\" from {}".format(
                        mod_path_str, os.path.join(*p)
                    )
                # prepend package name if imported using import_module
                path_str = mod_path_str
                if package:
                    path_str = "{}.{}".format(package, mod_path_str)
                # load module needs full path, ie a, a.b or a.b.c
                m = imp.load_module(path_str, *module)

        # this may not be needed
        self.repo_path = None
        return m

    def import_module(self, name, package=None):
        """
        Calls to import importlib get captured returning this class instead.
        importlib in python2 only supports import_module so emulate that
        functionality here, ie, find the module and load it
        """
        # relative import and have path already so remove '.'
        # build full package import
        fullname = name
        package = package or ''

        # prepend user specified repos
        prepend = REPOS.split(SEP)
        local_repos = prepend + self.local_repos()

        if name.startswith('.'):
            fullname = "{}{}".format(package or '', name)
            name = name[1:]

        # search local repos for repo with path `package`.`name`
        for repo in local_repos:
            path = os.path.join(repo, *fullname.split('.'))
            if(os.path.isdir(path) or os.path.isfile("{}.py".format(path))):
                self.repo_path = os.path.join(repo, *(package or '').split('.'))
                break
        else:
            self.repo_path = None
            return self._load_module(name, package=package)

        if VERBOSE:
            print "intercept importlib.import_module() for {} ({}) from {}" \
                .format(
                    name, package, self.repo_path
                )

        return self.load_module(name, package=package)

    def is_package(self, name):
        return True


class MultiRootLoader(object):

    def find_module(self, name, paths=None):

        import site
        site_path = site.getsitepackages()
        code_path = "{}/{}".format(REPO_ROOT, name.rsplit('.')[-1])

        # set path for site/code package import
        m = {
            'gazprom.mt.foo': site_path,
            # 'gazprom.mt.pricing': site_path,
            'gazprom.mt.pricing': code_path,
            'gazprom.mt.structuring': code_path,
        }

        path = m.get(name)
        if path:
            self.repo_path = path
            return self

    def load_module(self, name, package=None):
        """
        Load module from repo path found in `find_module()`. `name` is full
        dotted import path, each part of path must separately be imported to be
        able to find the next part of the package, eg, gazprom.mt.pricing:
        gazprom must be imported, then mt and finally pricing
        """

        mod_path = []
        # split the full import name and import each part separately
        # so import a.b.c requires importing a then a.b and finally a.b.c
        for n in name.split('.'):
            # build intermediate module path to be imported
            mod_path.append(n)
            mod_path_str = '.'.join(mod_path)

            # already imported up to `n` so don't need to import again
            module = imp.find_module(n, [os.path.join(self.repo_path,
                                                      *mod_path[:-1])])

            if VERBOSE:
                print "loading module \"{}\" from {}".format(
                    mod_path_str, os.path.join(self.repo_path,
                                               *mod_path[:-1])
                )
            # prepend package name if imported using import_module
            path_str = mod_path_str
            if package:
                path_str = "{}.{}".format(package, mod_path_str)
            m = imp.load_module(path_str, *module)
        return m


# import hook to preferentially load git repos rather than site-packages
sys.meta_path.append(GMTLoader())

# imports for packages which have multiple roots
# sys.meta_path.append(MultiRootLoader())
