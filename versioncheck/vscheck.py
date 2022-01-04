from versioncheck.version_set import Version_set
from versioncheck.utilities import log
import os
import json
import sys
from __init__ import __version__

from git import Repo

class VersionCheck:
    def __init__(self, setlist, source, start=None, target='master', repo=os.getcwd() ):
        self.repo = repo
        self.pr_repo = Repo(repo)
        self.setlist = [ Version_set(x['version_file'], x['track_log'], x['model'])
                         for x in setlist ]
        if start != None:
            self.start_sha = start
        else:
            self.start_sha = str(self.pr_repo.commit(target))

        self.head_sha = str(self.pr_repo.commit(source)) #head_commit

    def log(self):
        log(
            "repo:", self.repo,
            "start:", self.start_sha,
            "current:", self.head_sha,
            "setlist:"
        )
        for x in self.setlist:
            x.log()

    def get_changes(self, start, current):
        log('loading changes')
        changes = current.diff(start)
        changelist = [str(change).split('\n')[0] for change in changes]
        return changelist

    def extract_changes(self):

        commits_list = list(self.pr_repo.iter_commits())
        a=str(commits_list[0])
        heads = [x for x in range(0, len(commits_list) - 1) if
                 str(commits_list[x]) in [self.start_sha, self.head_sha]]
        if len(heads) < 2:
            return ['This branch is out-of-date with the base branch']

        log('heads_index',heads)
        changes = self.get_changes(
            commits_list[heads[1]], commits_list[heads[0]]
        )
        log('changes', changes)
        return changes

    def version_check(self, changes):
        tocorrect = []
        if len(changes) == 0:
            return tocorrect
        sets = [ x for x in self.setlist if x.version_file in changes]
        if len(sets) == 0:
            return [{'no_version_files': changes}]
        self.pr_repo.git.checkout(self.start_sha)
        log('starting versions')
        for set in sets:
            set.old_version=set.set_version(self.repo)
        self.pr_repo.git.checkout(self.head_sha)
        for set in sets:
            set.log()
            disaligned = ''
            if set.track_log in changes:
                set.new_version = set.set_version(self.repo)
                if set.new_version != set.old_version:
                    if not set.is_version_file_aligned(
                            set.new_version, self.repo
                    ):
                        disaligned = set.version_file
                    else:
                        log('set is ok')

            if set.track_log not in changes \
                    or set.new_version == set.old_version:
                log('track_log version not changed')
                disaligned = set.track_log
                set.new_version = set.old_version
                return False
            if len(disaligned) !=0:
                correction = {
                    disaligned: set.new_version
                }
                tocorrect.append(correction)
        return tocorrect

if __name__ == '__main__':
    setlist = json.load(open("versioncheck/vsset_sample_nodejs.json"))
    parindex = 0
    for par in range(0, len(sys.argv)):
        print(par, sys.argv[par])
    if sys.argv[1] == '--version':
        print (__version__)
        exit(0)
    start = None
    if len(sys.argv) > 2:
        branch = sys.argv[1]
        start = sys.argv[2]
    else:
        exit(0)
    if len(sys.argv) > 3:
        repo = sys.argv[3]
        this_check = VersionCheck(
            setlist, branch, start=start, repo=repo
        )
    else:
        this_check = VersionCheck(
            setlist, branch, start=start
        )
    this_check.log()
    if this_check.pr_repo == 'false':
        print('This is not a pull request')
        exit(0)
    else:
        this_check.log()
        correction_list = this_check.version_check(this_check.extract_changes())
        if len( correction_list ):
            print(correction_list)
            exit(1)

        exit(0)
