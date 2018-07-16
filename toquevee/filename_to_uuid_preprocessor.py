import pathlib
import uuid

from nbconvert.preprocessors import Preprocessor

class FilenameToUUIDPreprocessor(Preprocessor):

    def __init__(self, parent_dir, **kw):
        super(self.__class__, self).__init__(**kw)
        self._parent_dir = parent_dir

    def preprocess(self, nb, resources):
        trans_table = {}
        for k in resources['outputs'].keys():
            old_file_name = pathlib.PurePath(k)
            suffix = old_file_name.suffix

            file_name_uuid = uuid.uuid3(
                uuid.NAMESPACE_URL,
                str(self._parent_dir / old_file_name)
            )

            trans_table[k] = str(file_name_uuid) + suffix

        for old_name, uuid_file_name in trans_table.items():
            data = resources['outputs'].pop(old_name)
            resources['outputs'][uuid_file_name ] = data

        for c_idx, cell in enumerate(nb.cells):
            if not cell.cell_type == 'code':
                continue

            for o_idx, output in enumerate(cell['outputs']):
                if not output.metadata:
                    continue

                output = nb.cells[c_idx].outputs.pop(o_idx)
                old_filename = output.metadata.filenames['image/png']
                output.metadata.filenames['image/png'] = trans_table[old_filename]
                nb.cells[c_idx].outputs.insert(o_idx, output)

        return nb, resources
