
# this file is hardlinked (mklink /H on cmd) because windows python can't read symlink
# https://www.usenix.org/system/files/login/articles/09beazley_061-068_online.pdf

import os
import sys
import imp
import pythoncom
import pywintypes
from win32com.shell import shell


REPO_ROOT = 'c:/dev/code/gazprom.mt'
VERBOSE = os.environ.get("VERBOSE")


class GMTLoader(object):
    """
    Import hook to resolve local Python imports. Will search in `REPO_ROOT` for
    """
    def __init__(self):
        self._local_repos = []

    def local_repos(self, path=REPO_ROOT):
        """Find local repos by searching `REPO_ROOT` to find all packages"""

        # find root import path for repos
        def find_root(path, f):
            # recurse into dir to find __init__.py to determine top level of
            # code eg pyserialise
            repo = os.path.join(path, f)
            if os.path.isdir(repo) and not f.startswith('.'):
                subdirs = os.listdir(repo)
                if "__init__.py" in subdirs:
                    if VERBOSE:
                        print "found repo path: {}".format(path)
                    return path

                for sub in subdirs:
                    pp = find_root(os.path.join(path, f), sub)
                    if pp:
                        return pp

        if self._local_repos:
            return self._local_repos

        for f in os.listdir(path):
            repo = find_root(path, f)
            if repo:
                self._local_repos.append(repo)

        return self._local_repos

    def find_module(self, name, path):
        """
        Search for a package in local repo path that has a location which
        maps to `name`
        """
        # capture call to importlib because it breaks this import hook
        if "importlib" in name:
            return self

        # TODO: use dir_
        # search local repos to find the path to load the module from
        if path:
            # TODO: strip name from path to get root path
            # repos = [path]
            repos = self.local_repos()
        else:
            repos = self.local_repos()

        for repo in repos:
            # check path exists in "repo" and is a package
            if(os.path.isdir(os.path.join(REPO_ROOT, repo,
                                          *name.split('.'))) and
               os.path.isfile(
                   os.path.join(os.path.join(
                       REPO_ROOT, repo, *name.split('.')
                   ), "__init__.py"))):
                if VERBOSE:
                    print "found repo matching \"{}\" in {}".format(
                        name, os.path.join(REPO_ROOT, repo, *name.split('.'))
                    )
                self.repo_path = os.path.join(REPO_ROOT, repo)
                return self

    def load_module(self, name):
        """
        Load module from repo path found in `find_module()`. `name` is full
        dotted import path, each part of path must separately be imported to be
        able to find the next part of the package, eg, gazprom.mt.pricing:
        gazprom must be imported, then mt and finally pricing
        """
        # capture call to importlib because it breaks this import hook
        if "importlib" in name:
            return self

        mod_path = []
        # split the full import name and import each part separately
        # so import gmt.grid requires importing gmt then gmt.grid
        for n in name.split('.'):
            # build intermediate module path to be imported
            mod_path.append(n)
            mod_path_str = '.'.join(mod_path)

            # already imported up to `n` so don't need to import again
            if mod_path_str in sys.modules:
                m = sys.modules[mod_path_str]
            else:
                module = imp.find_module(n, [os.path.join(self.repo_path,
                                                          *mod_path[:-1])])
                if VERBOSE:
                    print "loading module \"{}\" from {}".format(
                        mod_path_str, os.path.join(self.repo_path,
                                                   *mod_path[:-1])
                    )
                m = imp.load_module(mod_path_str, *module)
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

        if name.startswith('.'):
            fullname = "{}{}".format(package or '', name)
            name = name[1:]

        # search local repos for repo with path `package`.`name`
        for repo in self.local_repos():
            if os.path.isdir(os.path.join(repo, *fullname.split('.'))):
                self.repo_path = os.path.join(
                    repo, *(package or '').split('.')
                )
                break

        if VERBOSE:
            print "intercept importlib.import_module() for {} ({}) from {}" \
                .format(
                    name, package, self.repo_path
                )

        return self.load_module(name)


class ShortcutLoader(GMTLoader):
    """Import hook to resolve Python imports through Windows shortcuts"""

    def get_shortcut_paths(self, directory):
        """get_shortcut_paths("Programs") => ["...\Internet Explorer.lnk", ...]

        Returns the list of Windows shortcuts contained in a directory.
        """
        return [os.path.join(directory, f) for f in os.listdir(directory)
                if os.path.splitext(f)[1] == '.lnk']

    def resolve_shortcut(self, filename):
        """resolve_shortcut("Notepad.lnk") => "C:\WINDOWS\system32\notepad.exe"

        Returns the path refered to by a windows shortcut (.lnk) file.
        """
        shell_link = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink, None,
            pythoncom.CLSCTX_INPROC_SERVER, shell.IID_IShellLink)

        persistant_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)

        persistant_file.Load(filename)

        shell_link.Resolve(0, 0)
        linked_to_file = shell_link.GetPath(shell.SLGP_UNCPRIORITY)[0]
        return linked_to_file

    def find_module(self, name, dir_):

        if 'structuring' in name:

            dirs = [f for f in os.listdir(REPO_ROOT)
                    if os.path.isdir(os.path.join(REPO_ROOT, f))]

            for d in dirs:
                p = os.path.join(REPO_ROOT, d, *name.split('.')) + ".lnk"
                # windows shortcuts not supported properly, ie os.path.islink
                # doesn't work
                try:
                    self.repo_path = self.resolve_shortcut(p)
                    self.repo_path = os.path.split(self.repo_path)[0]
                    if VERBOSE:
                        print "redirecting repo {} from {} to {}".format(
                            name, p, self.repo_path
                        )
                    return self
                except pywintypes.com_error:
                    pass

    def load_module(self, name):
        actual_name = name.split(".")[-1]
        return super(ShortcutLoader, self).load_module(actual_name)


# import hook to preferentially load git repos rather than site-packages
sys.meta_path.append(GMTLoader())

# redirect structuring imports if link wasn't created with mklink /J
# sys.meta_path.append(ShortcutLoader())
