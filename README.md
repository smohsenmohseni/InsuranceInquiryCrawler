# Insurance inquiry

[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20static%20analysis-flake8-%eb4034b1?style=flat)](https://github.com/PyCQA/flake8)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

## How to set up project:

install dependencies:

- Production:
    ```bash
    pip install -r requirements/production.txt
    ```
- Development:
    ```bash
    pip install -r requirements/local.txt
    ```

setup commands:

```bash
chmod +x ./scripts/setup

./scripts/setup
```

## How to run project:

```bash
start
```

## Examples:

```bash
curl -X GET "http://localhost:9080/basic?spider_name=sandbox&national_code=12313123"
```

```bash
curl -X GET "http://localhost:9080/supplemental?spider_name=sandbox&national_code=12313123"
```

## Contribute Notes:

#### Spiders:
- Spiders name format: `{InsuranceName}InsuranceSpider`

- Spiders should inherit from: `app.generics.GenericSpider`

- Spiders name automatically set as: `{insurance_name}_insurance`

- Spiders should use start_requests function to start crawl

- If spider parse method return None by default `InvalidInsuranceItem` return instead of None

- By default all spider use httpcache, to disable cache for request function use `app.helpers.decorators.disable_cache`
  decorator

#### Items:

- Items name format: `{InsuranceName}InsuranceItem`

#### Item loaders:

- ItemLoaders name format: `{InsuranceName}InsuranceItemLoader`

#### Performance:

- As here
  said [css selector or xpath selector](https://exadel.com/news/how-to-choose-selectors-for-automation-to-make-your-life-a-whole-lot-easier/#:~:text=CSS%20selectors%20tend%20to%20perform,an%20element%20by%20its%20text.),
  it is better to use `css selector` in most case except need to solve a complex issue

- As documented
  said [selectors shortcut](https://docs.scrapy.org/en/latest/topics/selectors.html#:~:text=By%20using%20response.selector%20or%20one%20of%20these%20shortcuts%20you%20can%20also%20ensure%20the%20response%20body%20is%20parsed%20only%20once.),
  shortcuts selectors ensure the response body is parsed only once, so our prefers is to use shortcuts selectors

#### Type checker:

- static typing checks by [`MyPy`](https://github.com/python/mypy)

- you are allowed to deep into one level for type hint
