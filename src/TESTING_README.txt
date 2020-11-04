TO RUN ALL UNITTESTS TYPE:
    python -m unittest

Any merge request with failed tests will not be pushed to master.
Any code with less than 70% coverage will not be pushed to master.

TO VIEW COVERAGE REPORT IN TERMINAL:
    coverage run --omit="*/interface_layer/*" --source app -m unittest discover -s test -p test_*.py
    coverage report



TO CREATE A COVERAGE REPORT IN HTML:
    coverage erase
    coverage run --omit="*/interface_layer/*" --source app -m unittest discover -s test -p test_*.py
    coverage html -d test\report\

    *You can then navigate to test\report and open index.html in browser to see the report







