description = "a module housing checks of bayestar functionality"
author      = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import eventSupervisor.eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

def is_bayestarStart( description ):
    ''' identify whether description is for a bayestar start alert by matching a string fragment '''
    return "INFO:BAYESTAR:starting sky localization" in description

def is_bayestarSkymap( description ):
    ''' identify whether description is for a bayestar skymap alert by matching a string fragment '''
    return "INFO:BAYESTAR:uploaded sky map" in description

#---------------------------------------------------------------------------------------------------

class BayestarStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that BayesStar started as expected

    alert:
        graceid
    options:
        dt
        email on success
        email on failure
        email on exception
    """
    description = "a check that BAYESTAR started as expected"
    name        = "bayestar start"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        timeout = float(options['dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        tasks = [bayestarStartCheck(
                     timeout, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag='%s.%s'%(logTag, self.name),
                 ),
        ]

        super(BayestarStartItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class bayestarStartCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar started as expected
    """
    description = "a check that bayestar started as expected"
    name        = "bayestarStart"

    def bayestarStart(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar started as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:starting sky localization", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found BAYESTAR starting message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR starting message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True


class BayestarItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced the expected data

    alert:
        graceid
    options:
        skymap dt
        skymap tagnames
        email on success
        email on failure
        email on exception
    """
    description = "a check that BAYESTAR produced the expected data and finished"
    name        = "bayestar"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [bayestarSkymapCheck(
                     skymap_dt, 
                     tagnames=skymap_tagnames, 
                     emailOnSuccess=emailOnSuccess, 
                     emailOnFailure=emailOnFailure, 
                     emailOnException=emailOnException, 
                     logDir=logDir, 
                     logTag=taskTag,
                 ),
        ]

        super(BayestarItem, self).__init__( 
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class bayestarSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayestar produced a skymap
    """
    description = "a check that bayestar produced a skymap"
    name        = "bayestarSkymap"

    def __init__(self, timeout, tagnames=None, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(bayestarSkymapCheck, self).__init__( 
            timeout, 
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def bayestarSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar produced a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        fitsname = "bayestar.fits.gz"
        self.warning, action_required = esUtils.check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose, logTag=logger.name if verbose else None )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

class BayestarFinishItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced a finish statement

    alert:
        graceid
    options:
        finish dt
        email on success
        email on failure
        email on exception
    """
    description = "a check that BAYESTAR finished"
    name        = "bayestar finish"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        finish_dt = float(options['finish dt'])

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [bayestarFinishCheck(
                     finish_dt,
                     emailOnSuccess=emailOnSuccess,
                     emailOnFailure=emailOnFailure,
                     emailOnException=emailOnException,
                     logDir=logDir,
                     logTag=taskTag,
                 ),
        ]

        super(BayestarFinishItem, self).__init__(
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )


class bayestarFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that bayestar finished as expected
    """
    description = "a check that bayestar finished as expected"
    name        = "bayestarFinish"

    def bayestarFinish(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar finished as expected
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag ) 
            logger.info( "%s : %s"%(graceid, self.description) )
        if not esUtils.check4log( graceid, gdb, "INFO:BAYESTAR:sky localization complete", verbose=verbose, logTag=logger.name if verbose else None ):
            self.warning = "found BAYESTAR completion message"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find a BAYESTAR completion message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                logger.debug( message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True
