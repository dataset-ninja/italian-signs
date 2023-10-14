Dataset **ItalianSigns** can be downloaded in [Supervisely format](https://developer.supervisely.com/api-references/supervisely-annotation-json-format):

 [Download](https://assets.supervisely.com/supervisely-supervisely-assets-public/teams_storage/c/t/gG/HHkr1USJlG3fVZ8NS8vspUvIw9mhMC3soZp75MFQ9dI1XOY8xA92Pnje5cmFZJxMjiCsEfTE9S6DiKWzYBwwOMbegiJDx1Wb82Oi5zn00XENvRreJWwJAqOqxcj6.tar)

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