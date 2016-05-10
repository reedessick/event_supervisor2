description = "a module housing checks of cWB-PE functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

class CWBPEStartItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE started
    """
    description = "a check that cWB PE started"

    def __init__(self, graceid, gdb, t0, timeout, annotate=False, email=[]):
        tasks = [cWBPEStartCheck(timeout, email)]
        super(CWBPEStartItem, self).__init__( graceid,
                                              gdb,
                                              t0,
                                              tasks,
                                              description=self.description,
                                              annotate=annotate
                                            )

class cWBPEStartCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE started
    """    
    name = "cWBPEStartCheck"
    description = "a check that cWB PE started"

    def __init__(self, timeout, email=[]):
        super(cWBPEStartCheck, self).__init__( timeout,
                                               self.cWBPEStartCheck,
                                               name=self.name,
                                               description=self.description,
                                               email=email
                                             )

    def cWBPEStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE started
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### NOTE: cWB PE may not have a cannonical "start" statement and may only report data
        ###       if this is the case, then we should NOT have a startCheck.

class CWBPEItem(esUtils.EventSupervisorQueueItem):
    """
    a check that cWB PE produces the expected data and finished
    """
    description = "a check that cWB PE produced the expected data and finished"

    def __init__(self, graceid, gdb, t0, timeout, tagnames=None, annotate=False, email=[]):
        tasks = [cWBPECEDCheck(timeout, email=email),
                 cWBPEEstimateCheck(timeout, email=email),
                 cWBPESkymapCheck(timeout, tagnames=tagnames, email=email),
#                 cWBPEFinishCheck(timeout, email=email)
                ]
        super(CWBPEItem, self).__init__( graceid, 
                                         gdb,
                                         t0,
                                         tasks,
                                         description=self.description,
                                         annotate=annotate
                                       )

class cWBPECEDCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    name = "cWBPEDataCheck"
    description = "a check that cWB PE posted estimates of parameters"

    def __init__(self, timeout, email=[]):
        super(cWBPECEDCheck, self).__init__( timeout,
                                                  self.cWBPECEDCheck,
                                                  name=self.name,
                                                  descripiton=self.description,
                                                  email=email
                                                )

    def cWBPECEDCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB CED", verbose=verbose ):
            self.warning = "found link to cWB CED page"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find link to cWB CED page"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPEEstimateCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted estimates of parameters
    """
    name = "cWBPEstimateCheck"
    description = "a check that cWB PE posted estimates of parameters"

    def __init__(self, timeout, email=[]):
        super(cWBPEEstimateCheck, self).__init__( timeout,
                                                  self.cWBPEEstimateCheck,
                                                  name=self.name,
                                                  descripiton=self.description,
                                                  email=email
                                                )

    def cWBPEEstimateCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE posted posterior samples
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )

        if not esUtils.check4log( graceid, gdb, "cWB parameter estimation", verbose=verbose ):
            self.warning = "found cWB estimates of parameters"
            if verbose or annotate:
                message = "no action required : "+self.warning
                if verbose:
                    print( "    "+message )
                if annotate:
                    esUtils.writeGDBLog( gdb, graceid, message )
            return False ### action_required = False

        self.warning = "could not find cWB estimates of parameters"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+self.warning )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class cWBPESkymapCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE posted a skymap
    """
    name = "cWBPESkymapCheck"
    description = "a check that cWB PE posted a skymap"

    def __init__(self, timeout, tagnames=None, email=[]):
        self.tagnames = tagnames
        super(cWBPESkymapCheck, self).__init__( timeout,
                                                self.cWBPESkymapCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def cWBPESkymapCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE posted a skymap
        looks for the existence of a skymap and the correct tagnames
        """
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
        fitsname = "skyprobcc_cWB.fits"
        self.warning, action_required = check4file( graceid, gdb, fitsname, tagnames=self.tagnames, verbose=verbose )
        if verbose or annotate:
            if action_required:
                message = "action required : "+self.warning
            else:
                message = "no action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return action_required

class cWBPEFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that cWB PE finished
    """
    name = "cWBPEFinishCheck"
    description = "a check that cWB PE finished"

    def __init__(self, timeout, email=[]):
        super(cWBPEFinishCheck, self).__init__( timeout,
                                                self.cWBPEFinishCheck,
                                                name=self.name,
                                                descripiton=self.description,
                                                email=email
                                              )

    def cWBPEFinishCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that cWB PE finished
        NOT IMPLEMENTED
        """
        raise NotImplementedError
        ### NOTE: cWB PE may not have a cannonical "finish" statement and may only report data
        ###       if this is the case, then we should NOT have a finishCheck.
