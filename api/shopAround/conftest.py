import pytest
from django.core.management import call_command
from django.db.utils import OperationalError
from django.db import connections
from _pytest.runner import TestReport

@pytest.fixture(scope='function', autouse=True)
def seed_test_database():
    # for conn in connections.all():
    #     conn.close()

    # try:
    #     for conn in connections.all():
    #         with conn.cursor() as cursor:
    #             cursor.execute("SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = %s;", [conn.settings_dict['NAME']])
    #         conn.close()

        call_command('seed')

    # except OperationalError as e:
    #     print(f"Error during setup: {e}")

    # yield

    # for conn in connections.all():
    #     conn.close()



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()
    
    # Attach the docstring to the report
    if report.when == 'call':
        docstring = item.function.__doc__
        if docstring:
            report.description = docstring.strip()

def pytest_terminal_summary(terminalreporter):
    # This function is called after the test session to modify the terminal summary
    lines = []
    for report in terminalreporter.stats.get('passed', []):
        if hasattr(report, 'description'):
            lines.append(f"PASSED - {report.description}")
    for report in terminalreporter.stats.get('failed', []):
        if hasattr(report, 'description'):
            lines.append(f"FAILED - {report.description}")
    
    # Print custom summary
    terminalreporter.section("Custom Test Summary", sep="=")
    for line in lines:
        terminalreporter.write_line(line)