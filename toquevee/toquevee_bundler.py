from .quiver_exporter import QuiverExporter

from .quiver_writer import QuiverWriter

def _jupyter_bundlerextension_paths():
    return [{
        'name': 'toquebee_bundler',
        'label': 'Quiver Notebook Bundler',
        'module_name': 'toquebee.toquebee_bundler',
        'group': 'deploy'
    }]

def bundle(handler, model):
    exporter = QuiverExporter()
    output, resources = exporter.from_notebook_node(model['content'])

    writer = QuiverWriter(
        filename=model['name'],
        created=model['created'],
        last_modified=model['last_modified'],
        config=handler.config)

    writer.write(output, resources)
    handler.finish('finished.')
