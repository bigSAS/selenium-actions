import logging
from seleniumactions.actions import Actions

log = logging.getLogger('ASSERTIONS')


def assert_condition(actions: Actions, condition: object, timeout_sec: int = None, message: str = None):
    try:
        actions.wait_for(condition=condition, timeout=timeout_sec)
        log.info(f"met condition :) {condition}")
    except Exception as e:
        msg = f"condition not met :( {condition}\nException: {repr(e)}"
        log.error(msg)
        assert False, f"{message}\n{msg}"
