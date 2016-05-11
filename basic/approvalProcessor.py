description = "a module housing checks of approval_processor functionality"
author = "reed.essick@ligo.org"

#---------------------------------------------------------------------------------------------------

import sys
sys.path.append("../")
import eventSupervisorUtils as esUtils

#---------------------------------------------------------------------------------------------------

### methods to identify updates by description

#---------------------------------------------------------------------------------------------------

#-------------------------------------------------
# approval_processor preliminary DQ checks
#-------------------------------------------------

class ApprovalProcessorPrelimDQItem(esUtils.EventSupervisorQueueItem):
    """
    a set of checks for approval_processor's preliminary DQ and vetting
    """
    name = "approval processor prelim dq"
    description = "a set of checks for approval_processor's preliminary DQ and vetting"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        farTimeout = float(options['far dt'])
        segTimeout = float(options['seg start dt'])
        email = options['email'].split()

        tasks = [approvalProcessorFARCheck(farTimeout, email=email),
                 approvalProcessorSegDBStartCheck(segStartTimeout, email=email)
                ]
        super(ApprovalProcessorPrelimDQItem, self).__init__( graceid,
                                                             gdb,
                                                             t0,
                                                             tasks,
                                                             annotate=annotate
                                                           )

class approvalProcessorFARCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor analyzed the FAR as expected
    """
    description = ""
    name = "approvalProcessorFAR"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorFARCheck, self).__init__( timeout, 
                                                         self.approvalProcessorFARCheck, 
                                                         email=email
                                                       )

    def approvalProcessorFARCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor analyzed the FAR as expected
        """
        ### note, we do not delegate to esUtils.check4log because there are multiple possible messages
        if verbose:
            print( "%s : %s"%(graceid, self.description) )
            print( "    retrieving log messages" )
        logs = gdb.logs( graceid ).json()['log']

        if verbose:
            print( "    parsing log" )
        for log in logs:
            comment = log['comment']
            if ("Candidate event has low enough FAR" in comment) \
              or ("Candidate event rejected due to large FAR" in comment) \
              or ("Ignoring new event because we found a hardware injection" in comment):
                self.warning = "found ApprovalProcessor FAR check message"
                if verbose or annotate:
                    message = "no action required : "+self.warning
                    if verbose:
                        print( "    "+message )
                    if annotate:
                        esUtils.writeGDBLog( gdb, graceid, message )
                return False ### action_required = False

        self.warning = "could not find ApprovalProcessor FAR check message"
        if verbose or annotate:
            message = "action required : "+self.warning
            if verbose:
                print( "    "+message )
            if annotate:
                esUtils.writeGDBLog( gdb, graceid, message )
        return True ### action_required = True

class approvalProcessorSegDBStartCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor started checking segments as expected
    """
    description = ""
    name = "approvalProcessorSegDBStart"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBStartCheck, self).__init__( timeout, 
                                                                self.approvalProcessorSegDBStartCheck, 
                                                                email=email
                                                              )

    def approvalProcessorSegDBStartCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor started checking segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


class approvalProcessorSegDBFlagsCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor checked all the segment/flags as expected
    """
    description = ""
    name = "approvalProcessorSegDBFlags"

    def __init__(self, timeout, flags=[], email=[]):
        self.flags = []
        super(approvalProcessorSegDBFlagsCheck, self).__init__( timeout,
                                                                self.approvalProcessorSegDBFlagsCheck,
                                                                email=email
                                                              )

    def approvalProcessorSegDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor checked all the segment/flags as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class approvalProcessorSegDBFinishCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor finished checking segments as expected
    """
    description = ""
    name = "approvalProcessorSegDBFinish"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorSegDBFinishCheck, self).__init__( timeout,
                                                                 self.approvalProcessorSegDBFinishCheck,
                                                                 email=email
                                                               )

    def approvalProcessorSegDBFlagsCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor finished checking all segments as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


#-------------------------------------------------
#  approvalProcessor_idq
#-------------------------------------------------

class ApprovalProcessoriDQItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring approval processor's response to iDQ information
    """
    name = "approval processor idq"
    description = "an item for montitoring approval_processor's response to iDQ information"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        ifos = options['ifos'].split()

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [ approvalProcessoriDQglitchFAPCheck(timeout, ifo, email=email) for ifo in ifos ]
        super(ApprovalProcessoriDQItem, self).__init__( graceid,
                                                        gdb,
                                                        t0,
                                                        tasks,
                                                        annotate=annotate
                                                       )

class approvalProcessoriDQglitchFAPCheck(esUtils.EventSupervisorTask):
    """
    a check that approvalProcessor responded to iDQ FAP reports as expected
    """
    description = ""
    name = "approvalProcessoriDQglitchFAP"

    def __init__(self, timeout, ifo, email=[]):
        self.ifo = ifo
        super(approvalProcessoriDQglitchFAPCheck, self).__init__( timeout,
                                                             self.approvalProcessoriDQglitchFAPCheck,
                                                             email=email
                                                           )

    def approvalProcessoriDQglitchFAPCheck(self, graceid, gdb, verbose=False, annotate=False):
        """
        a check that approvalProcessor responded to iDQ FAP reports as expected
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

#-------------------------------------------------
# approvalProcessor VOEvent and GCN
#-------------------------------------------------

class ApprovalProcessorVOEventItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring VOEvent generation and distribution
    """
    name="approval processor voevent"
    description = "check that approval processor generated and distributed VOEvents"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [approvalProcessorVOEventCreationCheck(timeout, email=email),
                 approvalProcessorVOEventDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorVOEventItem, self).__init__( graceid,
                                                            gdb,
                                                            t0,
                                                            tasks,
                                                            annotate=annotate
                                                          )

class approvalProcessorVOEventCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the expected VOEvent
    """
    description = "a check that approval processor created the expected VOEvent"
    name = "approvalProcessorVOEventCreation"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventCreationCheck, self).__init__( timeout,
                                                                     self.voeventCreationCheck,
                                                                     email=email
                                                                   )

    def voeventCreationCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor created the expected VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class approvalProcessorVOEventDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the VOEvent as expected
    """
    description = "a check that approval processor distributed the VOEvent"
    name = "approvalProcessorVOEventDistribution"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventDistributionCheck, self).__init__( timeout,
                                                                     self.voeventDistribCheck,
                                                                     email=email
                                                                   )

    def voeventDistribCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor distributed the VOEvent
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

class ApprovalProcessorGCNItem(esUtils.EventSupervisorQueueItem):
    """
    an item for monitoring GCN generation and distribution
    """
    name = "approval processor gcn"
    description = "check that approval processor generated and distributed GCNs"

    def __init__(self, alert, t0, options, gdb, annotate=False):
        graceid = alert['uid']

        timeout = float(options['dt'])
        email = options['email'].split()

        tasks = [approvalProcessorGCNCreationCheck(timeout, email=email),
                 approvalProcessorGCNDistributionCheck(timeout, email=email)
                ]
        super(ApprovalProcessorVOEventItem, self).__init__( graceid,
                                                            gdb,
                                                            t0,
                                                            tasks,
                                                            annotate=annotate
                                                          )

class approvalProcessorGCNCreationCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor created the GCN as expected
    """
    description = "a check that approval processor created the expected GCN"
    name = "approvalProcessorGCNCreation"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorGCNCreationCheck, self).__init__( timeout,
                                                                     self.gcnCreationCheck,
                                                                     email=email
                                                                   )

    def gcnCreationCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor created the expected GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)


class approvalProcessorGCNDistributionCheck(esUtils.EventSupervisorTask):
    """
    a check that approval processor distributed the GCN as expected
    """
    description = "a check that approval processor distributed the GCN"
    name = "approvalProcessorGCNDistribution"

    def __init__(self, timeout, email=[]):
        super(approvalProcessorVOEventDistributionCheck, self).__init__( timeout,
                                                                     self.gcnDistribCheck,
                                                                     email=email
                                                                   )

    def gcnDistribCheck(self, graceid, gdb, verbose=False, annotate=False ):
        """
        check that approval processor distributed the GCN
        NOT IMPLEMENTED
        """
        raise NotImplementedError(self.name)

#-------------------------------------------------
# labeling?
#-------------------------------------------------
"""
need to monitor the appropriate use of
  INJ
  DQV
  EM_READY
  PE_READY
  else? -> ADVREQ, H1REQ, L1REQ, ADVOK, H1OK, L1OK, ADVNO, H1NO, L1NO, 
"""
