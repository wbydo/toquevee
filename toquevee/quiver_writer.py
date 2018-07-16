import pathlib
import json

from nbconvert.writers import WriterBase

from traitlets import Unicode

from .err import ToquebeeException

class QuiverWriter(WriterBase):
    quiver_path = Unicode('',
        help='Quiver Library Path'
    ).tag(config=True)

    def __init__(self, filename, created, last_modified, config=None, **kw):
        self._filename = pathlib.PurePath(filename).stem
        self._created = int(created.strftime('%s'))
        self._last_modified = int(last_modified.strftime('%s'))

        super(self.__class__, self).__init__(config=config, **kw)

    def write(self, output, resources, **kw):
        if not self.quiver_path:
            raise ToquebeeException()

        library = pathlib.Path(self.quiver_path)
        dir_ = (library / output['path'])

        dir_.mkdir()

        content = {
            'title': self._filename,
            'cells': output['cells'],
        }
        with dir_.joinpath('content.json').open('w') as f:
            json.dump(content, f, indent=4)

        meta = {
            'created_at': self._created,
            'title': self._filename,
            'updated_at': self._last_modified,
            'uuid': output['path'].stem,
            'tags': [
                'jupyter notebook',
            ]
        }
        with dir_.joinpath('meta.json').open('w') as f:
            json.dump(meta, f, indent=4)

        resources_path = dir_.joinpath('resources')
        resources_path.mkdir()

        for k in resources.keys():
            with resources_path.joinpath(k).open('wb') as f:
                f.write(resources[k])
