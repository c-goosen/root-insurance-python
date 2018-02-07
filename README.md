# Getting Started

## Install
```
pip install rootsdk
```
or
```
git clone git@github.com:BrendanBall/root-insurance-python.git
pip install -e root-insurance-python
```

## Environment Variables
```
ROOT_APP_ID
ROOT_APP_SECRET
```

## Code

```python
from root import insurance

client = insurance.Client()
phone_brands = client.gadgets.list_phone_brands()

```

# Upload to pip
```
python setup.py bdist_wheel upload -r pypi
```