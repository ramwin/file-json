# file-json
In many scenarios, you may want to save a huge list, dict object and use it later.  
The standard json package will load all the data into memroy.  
Hence comes the file-json library. With this package, you can store the list, dict object to local file system.

## How it works
all the rules should 

1. Each object was store in a directory, the data was store in `*.json.gz`
2. the `.file_json.json` file contains some basic info of this object.
3. for time base list, the directory looks like this.
```
.file_json.json
{
    "type": "time_based_list",
    "key": "create_datetime",
}
```

```
2023
  - 12
    - 19
      - 00.json.gz  # this file contains data from 2023-12-19 00:00:00 to 2023-12-19 01:00:00(exclude 2023-12-19 01:00:00)
      - 01.json.gz
      - 02  # if there were too much data between 2023-12-19 02:00:00 and 2023-12-10 03:00：00
        - 00.json.gz
        - 01.json.gz
    - 20
2024
  - 01
    - 01
```
4. for huge size of list, the directory looks like this. 
```
.file_json.json
{
    "type": "sorted_list",
    "key": "id",
}
```

```
- 00.json.gz
- 01.json.gz
- 02
    - 01.json.gz
    - 02.json.gz
- 03.json.gz
```

5. for huge size of dict, the directory looks like this.
```
.file_json.json
{
    "type": "dict",
}
```

```
- key1.json.gz
- key2
    - key2_1.json.gz
    - key2_2.json.gz
- key3.json.gz
```

## Features
* [ ] support time base list
* [ ] support huge size of list
* [ ] support huge size of dict


[![PyPI - Version](https://img.shields.io/pypi/v/file-json.svg)](https://pypi.org/project/file-json)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/file-json.svg)](https://pypi.org/project/file-json)

-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install file-json
```

## License

`file-json` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
