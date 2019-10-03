from warnings import warn

from objects.entities.opportunity.opportunity import Opportunity
from tools.json_tools import *


class OpportunityBusinessLines(Opportunity):

    def __init__(self, user, code):
        super().__init__(user, code)
        self._user = user
        self._code = code
        self._config = super().set_opp_config()

    def put_opportunity_business_lines(self, opportunity=None, opportunity_id=None, bl_codes=None, bl_ids=None,
                                       payload=None):

        # Fetch availability of business lines per opportunity
        if not opportunity and opportunity_id:
            opportunity = super().get_opportunity_by_id(opportunity_id=opportunity_id)
        elif not opportunity and not opportunity_id:
            raise ValueError("Missing parameters: opportunity or opportunity_id")

        if payload:
            bl_ids = extract(body=payload, path="$..businessLine.businessLineId", multiple=True)
        elif not payload and not bl_codes and not bl_ids:
            raise ValueError("Missing parameters: body or business line code")

        url = extract(body=opportunity.json(), path="links.addBusinessLines")
        payload = self.set_business_lines(opportunity=opportunity, req_bl_codes=bl_codes, req_bl_ids=bl_ids)

        r = self._user.put(url=url, payload=payload)
        return r

    def fetch_business_lines_config(self, opportunity):
        url = extract(body=opportunity.json(), path="$.links.configuration")
        config = self._user.get(url=url)

        bls = extract(body=config.json(), path="$.businessLines")

        return bls

    def set_business_lines(self, opportunity, req_bl_codes=None, req_bl_ids=None):

        if req_bl_ids is not None and req_bl_codes is None:
            bls_config, bls = self.validate_business_lines_config(opportunity=opportunity, ids=req_bl_ids)
        elif req_bl_codes is not None and req_bl_ids is None:
            bls_config, bls = self.validate_business_lines_config(opportunity=opportunity, codes=req_bl_codes)
        else:
            raise ValueError(
                "Missing mandatory parameters: req_bl_codes or req_bl_ids (if both are specified, choose only one).")

        body = self.calculate_opp_bl_body(config=bls_config, values=bls)
        return body

    def calculate_opp_bl_body(self, config, values):
        apis = self._config["usp_sm_PatchOpportunityBusinessLineById_v5"]

        bls = []
        for value in values:
            for i in range(0, len(config)):
                if value == config[i]['businessLineId'] and self._code == "O":
                    body_bl = extract(body=apis, path='$.body_quote.opportunityBusinessLines')[0]
                    body_bl = update_json(body=body_bl, values={
                        '$..businessLineId': value,
                        '$..volume.estimated.comment': 'Automated test comment',
                        '$..volume.estimated.quantity.amount': 1000,
                        '$..volume.estimated.quantity.unitOfMeasure.unitId': extract(body=config[i],
                                                                                     path='$.businesslineConfiguration.defaultUnitOfMeasure.unitId')
                    })
                    bls.append(deepcopy(body_bl))
                elif value == config[i]['businessLineId']:
                    body_bl = extract(body=apis, path='$.body.opportunityBusinessLines..businessLine')
                    body_bl = update_json(body=body_bl, values={"$.businessLineId": value})
                    bls.append({"businessLine": deepcopy(body_bl)})

        body = {'opportunityBusinessLines': []}
        body = update_json(body=body, values={'$.opportunityBusinessLines': bls})

        return body

    def validate_business_lines_config(self, opportunity, codes=None, ids=None):
        bls_config = self.fetch_business_lines_config(opportunity=opportunity)

        bls = []
        if codes and isinstance(codes, list):
            config = extract(body=bls_config, path="$..businessLineCode", multiple=True)
            if config is None:
                assert False, "There are no business lines available for this opportunity."
            for value in codes:
                if value not in config:
                    warn(UserWarning("%s not in opportunity configuration. Check test data." % value))
                else:
                    for bl in bls_config:
                        code = extract(body=bl, path='$.businessLineCode')
                        if value == code:
                            value = extract(body=bl, path='$.businessLineId')
                            bls.append(value)
                            break
            if not bls:
                warn(UserWarning(
                    "Empty values for opportunity, using values from configuration. Check test data." % config))
                bls = config
        elif ids:
            config = extract(body=bls_config, path="$..businessLineId", multiple=True)
            if config is None:
                assert False, "There are no business lines available for this opportunity."
            for value in ids:
                if value not in config:
                    warn(UserWarning("%s not in opportunity configuration. Check test data." % value))
                else:
                    bls.append(value)
            if not bls:
                warn(UserWarning(
                    "Empty values for opportunity, using values from configuration. Check test data." % config))
                bls = config

        return bls_config, bls
