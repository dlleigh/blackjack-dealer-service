from BlackjackDealerService import BlackjackDealerService

def before_all(context):
    # -- SET LOG LEVEL: behave --logging-level=ERROR ...
    # on behave command-line or in "behave.ini".
    context.config.setup_logging()

BEHAVE_DEBUG_ON_ERROR = False

def setup_debug_on_error(userdata):
    global BEHAVE_DEBUG_ON_ERROR
    BEHAVE_DEBUG_ON_ERROR = userdata.getbool("BEHAVE_DEBUG_ON_ERROR")

def before_all(context):
    setup_debug_on_error(context.config.userdata)
    import ipdb
    #ipdb.set_trace()

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