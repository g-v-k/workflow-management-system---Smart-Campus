def conditionHandler(values, currNode):
    if(currNode == "set_invisilation_register"):
        return [{'nodeID':'mail_invite_invisilation','URL':'http://localhost:3000/set_invisilation/invite_mail_invisilation'}]

    elif(currNode == 'mail_invite_invisilation'):
        return [{'nodeID':'papers_given_to_profs','URL':'http://localhost:3000/papers_given_to_profs/store_info'}]

    elif(currNode == 'papers_given_to_profs'):
        return [{'nodeID':'ans_sheets_returned','URL':'http://localhost:3000/ans_sheets_returned/store_info'}]

    elif(currNode == 'ans_sheets_returned'):
        return [{'nodeID':'thanks_mail_invisilation','URL':'http://localhost:3000/set_invisilation/thanks_mail_invisilation'}]
    elif(currNode == 'thanks_mail_invisilation'):
        return None

