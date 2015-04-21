from BlackjackDealerService import BlackjackDealerService
from subprocess import Popen
import time, os

BEHAVE_DEBUG_ON_ERROR = False

def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")

def before_all(context):
    context.config.setup_logging()
    setup_debug_on_error(context.config.userdata)
    import ipdb
    #ipdb.set_trace()
    # run mock player service
    context.mockProcess = Popen('/usr/bin/python MockPlayerService.py',shell=True)
    print("MockProcess pid: %s" % context.mockProcess.pid)
    time.sleep(float(5))  # maybe later we poll to see if the MockPlayerService is started

def after_all(context):
    # context.mockProcess.terminate()
    Popen("for i in $(ps -ef | grep MockPlayerService | awk '{print $2}'); do kill $i ; done ",shell=True)

def after_scenario(context, scenario):
    context.page = context.client.get('/deleteAll')

def after_step(context, step):
    if BEHAVE_DEBUG_ON_ERROR and step.status == "failed":
        # -- ENTER DEBUGGER: Zoom in on failure location.
        # NOTE: Use IPython debugger, same for pdb (basic python debugger).
        import ipdb
        ipdb.post_mortem(step.exc_traceback)

def before_feature(context, feature):
    BlackjackDealerService.config['TESTING'] = True
    context.client = BlackjackDealerService.test_client()