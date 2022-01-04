## versioncheck
versioncheck is a tool that compare a branch version against master to see if version is changed and if a description 
related to that version is available in the documrent tracking changes.

### setlist
it needs a list of jsons containing the following settings:
- name of version file
        "version_file": "package.json",
- name of the document tracking changes
        "track_log": "CHANGES.md",
- line in version file containing version number set to version 0.0.0
        "model": "\"version\": \"0.0.0\","
### parameters
It has following parameters:
- setlist - list of jsons contianing version info
- source - name of the branch containing changes
- start - last commit number from master
- repo - path to the clone of the repository
- target - usually master, target branch to merge into

### sample issue
 python3 versioncheck/vscheck.py fst 8fab466f0e9b5ea375205852bff6b9773c5a5250 ../../git/hello-devops
