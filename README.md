# toquevee
convert jupyter notebook to Quiver notebook

## Usage
```
pip install toquevee
jupyter bundlerextension enable --py toquevee.toquevee_bundler # --sys-prefix
```

```python
# jupyter_notebook_config.py
c.QuiverWriter.quiver_path = '/your/path/to/Quiver.qvlibrary/Inbox.qvnotebook'
```

`File` -> `Deploy as` -> `Quiver Notebook Bundler`
