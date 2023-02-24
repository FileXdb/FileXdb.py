# Contributing Guidelines

Thank you for investing your time in contributing to our project! Whether it's a bug report, new feature, correction, or additional documentation, we greatly value feedback and contributions from our community. Any contribution you make will be reflected on `github.com/FileXdb/FileXdb-Python`✨.

Contributions to _FileXdb_ are welcome! Here's how to get started:

- Open an [issue](https://github.com/FileXdb/FileXdb-Python/issues) or find for related issues to start a discussion around a feature idea or a bug.
- Fork the [repository](https://github.com/FileXdb/FileXdb-Python) on GitHub.
- Create a new branch of the master branch and start making your changes.
- Make a meaning-full commit.
- Write a test, which shows that the bug is fixed or the feature works as expected.
- Send a pull request and wait until it gets merged and published.



# Coding Conventions

In general the FileXdb source code always follows [PEP 8](http://legacy.python.org/dev/peps/pep-0008/).
Exceptions are allowed in well justified and documented cases. However, we make
a small exception concerning docstrings:

When using multiline docstrings, keep the opening and closing triple quotes
on their own lines and add an empty line after it. 

Here is a demo for you.

```python

    def sum_of_two_num(a: int, b: int ) -> int:
        """
        Documentation ...
        
        :param a: Definition...
        :param b: Definition...
        :return: Definition...
        """
        
        # Implementation Documentation ...
        result = a + b
        
        return result
```



# Version Numbers

FileXdb follows the [SemVer versioning guidelines](http://semver.org).
This implies that backwards incompatible changes in the API will increment
the major version. So think twice before making such changes.