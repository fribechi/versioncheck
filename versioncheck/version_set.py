import versioncheck.utilities as u
class Version_set:
    def __init__(self,version_file, track_log, model):
        self.version_file = version_file
        self.track_log = track_log
        self.old_version = '0.0.0'
        self.new_version = '0.0.0'
        self.model = f'{model}'
        [self.pre, self.post] = self.model.split('0.0.0')

    def log(self):
        u.log(
            "version_file:", self.version_file,
            "track_log:", self.track_log,
            "model:", self.model, self.pre, self.post,
            "old_version:", self.old_version,
            "new_version:", self.new_version
        )

    def set_version(self,root = ''):
        version = '0.0.0'
        t_file = None
        try:
            t_file = open(f'{root}/{self.track_log}')
        except:
            print(f'{root}/{self.track_log} not existing')
        if t_file != None:
            line = t_file.readline()
            version = line.split('# ')[1].split('\n')[0]
            u.log(f"version is {version} for {self.track_log}")
        return version

    def is_version_file_aligned(self, version, root=''):
        v_file = open(f'{root}/{self.version_file}')
        contents = v_file.read()
        internal_version = u.retrieve_string_from_contents(
            contents,self.pre
        ).split(self.post)[0]
        u.log(f'version file has {internal_version} comparing {version}' )
        return internal_version == version

    def align_version_file(self, version, root=''):
        old_file = open(f'{root}/{self.version_file}', 'r')
        contents = old_file.read()
        new_contents = u.modify_string_contents(contents, self.pre, version)
        return new_contents

    def upgrade_track_file(self,version, comment, root=''):
        old_file = open(f'{root}/{self.track_log}','r')
        contents = old_file.read()
        new_contents = f'# {version}{u.LINE_FEED}{u.LINE_FEED} - [CHANGED] ' \
                    f'{comment}{u.LINE_FEED}{u.LINE_FEED}{contents}'
        return new_contents

    def increment_version(self,version):
        digits = version.split('.')
        digits[2]= f'{int(digits[2])+1}'
        return '.'.join(digits)