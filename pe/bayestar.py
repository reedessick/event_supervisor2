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
    description = "a check that BAYESTAR produced the expected data"
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

#-------------------------------------------------
# hopefully temporary addition to deal with "_no_virgo" skymaps generated in parallel to the original runs
# NOTE: the only difference between the Bayestar processes is the output filename, which means I cannot tell them apart based on only the
#       start or finish message. Therefore, I'm only supporting a "skymap check" for the no_virgo process, which will be triggered by the 
#       addition of psd.xml.gz and run on a separate timeout. This should be documented within eventSupervisor.py as well.

class BayestarNoVirgoItem(esUtils.EventSupervisorQueueItem):
    """
    a check that Bayestar produced the expected data (excluding virgo)

    alert:
        graceid
    options:
        skymap dt
        skymap tagnames
        email on success
        email on failure
        email on exception
    """
    description = "a check that BAYESTAR produced the expected data (excluding virgo)"
    name        = "bayestarNoVirgo"

    def __init__(self, alert, t0, options, gdb, annotate=False, warnings=False, logDir='.', logTag='iQ'):
        graceid = alert['uid']

        skymap_dt = float(options['skymap dt'])
        skymap_tagnames = options['skymap tagnames'].split() if options.has_key('skymap tagnames') else None

        emailOnSuccess = options['email on success'].split()
        emailOnFailure = options['email on failure'].split()
        emailOnException = options['email on exception'].split()

        taskTag = '%s.%s'%(logTag, self.name)
        tasks = [bayestarNoVirgoSkymapCheck(
                     skymap_dt,
                     tagnames=skymap_tagnames,
                     emailOnSuccess=emailOnSuccess,
                     emailOnFailure=emailOnFailure,
                     emailOnException=emailOnException,
                     logDir=logDir,
                     logTag=taskTag,
                 ),
        ]

        super(BayestarNoVirgoItem, self).__init__(
            graceid,
            gdb,
            t0,
            tasks,
            annotate=annotate,
            warnings=warnings,
            logDir=logDir,
            logTag=logTag,
        )

class bayestarNoVirgoSkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that Bayestar produced a skymap which excludes virgo
    """
    description = "a check that bayestar produced a skymap which excludes virgo"
    name        = "bayestarNoVirgoSkymap"

    def __init__(self, timeout, tagnames=None, emailOnSuccess=[], emailOnFailure=[], emailOnException=[], logDir='.', logTag='iQ'):
        self.tagnames = tagnames
        super(bayestarNoVirgoSkymapCheck, self).__init__(
            timeout,
            emailOnSuccess=emailOnSuccess,
            emailOnFailure=emailOnFailure,
            emailOnException=emailOnException,
            logDir=logDir,
            logTag=logTag,
        )

    def bayestarNoVirgoSkymap(self, graceid, gdb, verbose=False, annotate=False, **kwargs):
        """
        a check that bayestar produced a skymap which excludes virgo
        Only checks for a skymap iff Virgo is present in the instrument list. Otherwise, ignores this event (return False)
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            logger = esUtils.genTaskLogger( self.logDir, self.name, logTag=self.logTag )
            logger.info( "%s : %s"%(graceid, self.description) )

        ### FIXME: the following might be fragile...
        if 'V1' not in gdb.event(graceid).json()['instruments'].split(','):
            if verbose or annotate:
                message = 'no action required : V1 not in list of instruments and therefore existence of bayestar_no_virgo.fits.gz is irrelevant'
                if verbose:
                    logger.debug( message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### not the trigger set I was expecting 

        fitsname = "bayestar_no_virgo.fits.gz"
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

