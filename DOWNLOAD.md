Dataset **ItalianSigns** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/remote/eyJsaW5rIjogImZzOi8vYXNzZXRzLzI1MTBfSXRhbGlhblNpZ25zL2l0YWxpYW5zaWducy1EYXRhc2V0TmluamEudGFyIiwgInNpZyI6ICJpZzg3NHlEWmd0cGcwcytLRW11R255NU11TUluOFoyU3I0L2Z3cUNJdzZvPSJ9)

As an alternative, it can be downloaded with *dataset-tools* package:
``` bash
pip install --upgrade dataset-tools
```

... using following python code:
``` python
import dataset_tools as dtools

dtools.download(dataset='ItalianSigns', dst_dir='~/dataset-ninja/')
```
Make sure not to overlook the [python code example](https://developer.supervisely.com/getting-started/python-sdk-tutorials/iterate-over-a-local-project) available on the Supervisely Developer Portal. It will give you a clear idea of how to effortlessly work with the downloaded dataset.

The data in original format can be [downloaded here](https://www.kaggle.com/datasets/officialprojecto/italiansigns/download?datasetVersionNumber=1).