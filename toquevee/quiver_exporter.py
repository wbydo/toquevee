import pathlib
import uuid

from nbconvert.exporters import Exporter
from nbconvert.preprocessors import ExtractOutputPreprocessor

from .filename_to_uuid_preprocessor import FilenameToUUIDPreprocessor

class QuiverExporter(Exporter):
    def from_notebook_node(self, nb, resources=None, **kw):
        path = pathlib.PurePath(str(uuid.uuid4()) + '.qvnote')

        p = ExtractOutputPreprocessor()
        self.register_preprocessor(p, enabled=True)

        fp = FilenameToUUIDPreprocessor(path)
        self.register_preprocessor(fp, enabled=True)

        nb_cp, resources = super(self.__class__, self).from_notebook_node(nb, resources, **kw)
        quiver_cells = [cell for cell in self._convert_cells(nb_cp)]

        return {'cells': quiver_cells, 'path': path}, resources['outputs']

    def _convert_cells(self, nb):
        for cell in nb.cells:
            if cell.cell_type == 'markdown':
                yield {
                    'type': 'markdown',
                    'data': cell['source']
                }

            elif cell.cell_type == 'raw':
                pass
                # yield {
                #     'type': 'markdown',
                #     'data': '```\n' + cell['source'] + '\n```'
                # }

            elif cell.cell_type == 'code':
                yield {
                    'type': 'code',
                    'language': nb.metadata.language_info.name,
                    'data': cell.source
                }

                for output in cell.outputs:
                    if 'image/png' in output.data.keys():
                        filename = output.metadata.filenames['image/png']
                        yield {
                            'type': 'markdown',
                            'data': f'![](quiver-image-url/{filename})'
                        }
                    elif 'text/html' in output.data.keys():
                        yield {
                            'type': 'markdown',
                            'data': output.data['text/html']
                        }
                    else:
                        yield {
                            'type': 'markdown',
                            'data': '```\n' + output.data['text/plain'] + '\n```'
                        }
