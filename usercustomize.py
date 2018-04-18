
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
        self._local_repos = None

    def local_repos(self, path=REPO_ROOT):
        # TODO: needs to recurse into dir to find __init__.py otherwise it might
        #       not be the top level of the code, eg pyserialise

        # find root import path for repos
        def find_root(path, f):
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

        self._local_repos = []
        for f in os.listdir(path):
            repo = find_root(path, f)
            if repo:
                self._local_repos.append(repo)

        return self._local_repos

    def find_module(self, name, dir_):
        """
        Search for a package in local repo path that has a location which
        maps to `name`
        """
        # capture call to importlib because it breaks this import hook
        if "importlib" in name:
            return self

        # search local repos to find the path to load the module from
        repos = self.local_repos()
        for repo in repos:
            if os.path.isdir(os.path.join(REPO_ROOT, repo, *name.split('.'))):
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
        file_path = [self.repo_path]
        # split the full import name and import each part separately
        # so import gmt.grid requires importing gmt then gmt.grid
        for n in name.split('.'):
            mod_path.append(n)
            mod_path_str = '.'.join(mod_path)

            module = imp.find_module(n, [os.path.join(*file_path)])
            if VERBOSE:
                print "loading module \"{}\" from {}".format(
                    mod_path_str, os.path.join(*file_path)
                )
            file_path.append(n)
            m = imp.load_module(mod_path_str, *module)
        return m

    def import_module(self, name, package=None):
        """
        Calls to import importlib get captured returning this class instead.
        importlib in python2 only supports import_module so emulate that
        functionality here, ie, find the module and load it
        """
        if VERBOSE:
            print "intercept importlib.import_module() for {}:{}".format(
                name, package
            )

        # get the file path of the caller for imp to find the module to import
        import inspect
        file_ = os.path.dirname(inspect.stack()[1][1])

        # NOTE: setting this is only needed in one place with relative import
        #       it might break with full path
        # set path for load_module to use for root import
        self.repo_path = file_

        # relative import and have path already so remove '.'
        if name.startswith('.'):
            name = name[1:]

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
# sys.meta_path.append(ShortcutLoader())
