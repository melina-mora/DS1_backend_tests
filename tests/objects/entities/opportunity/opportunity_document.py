from objects.entities.opportunity.opportunity import Opportunity
import os
from pathlib import Path
from tools.json_tools import *
from requests_toolbelt.multipart.encoder import MultipartEncoder


class OpportunityDocument(Opportunity):

	def __init__(self, user, code):
		super().__init__(user, code)
		self._user = user
		self._code = code
		self._config = super().set_opp_config()

	def patch_opportunity_document(self, opportunity, opportunity_id, document_type, file):
		if document_type == "Taxable":
			apis = self._config["usp_sm_PostOpportunityByIdDocumentsTaxable_v5_Validate"]
		else:
			apis = self._config["usp_sm_PostOpportunityByIdDocumentsProject_v5_Validate"]

		if opportunity_id and not opportunity:
			opportunity = self.get_opportunity_by_id(opportunity_id=opportunity_id)
		elif not opportunity:
			raise ValueError("Must specify opportunity or opportunity id to patch document to.")

		body = opportunity.json()

		if document_type == "Project":
			url = extract(body=body, path='$.links.addProjectDocument')
		else:
			url = "" # TODO Define taxable API

		mp_encoder = MultipartEncoder(
				fields={
					'file': ('project.pdf', file.open(mode='rb+'), 'application/pdf'),
				}
		)

		r = self._user.post(url=url, data=mp_encoder)

		return r
