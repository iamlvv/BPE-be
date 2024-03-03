from data.repositories.survey_features.section import Section


class Section_service:
    @classmethod
    def create_section(cls, survey_id, name, order_in_survey):
        return Section.create_section(survey_id, name, order_in_survey)

    @classmethod
    def create_sample_sections(cls, survey_id):
        return Section.create_sample_sections(survey_id)
