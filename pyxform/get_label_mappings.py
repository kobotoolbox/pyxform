'''
Created on Dec 9, 2014

@author: esmail
'''


from __future__ import absolute_import 

from . import constants
from . import survey
from . import section
from . import question


OPTION_LABEL_MAP_KEY= 'option_label_map'


def get_label_mappings(survey_in):
    question_label_mappings= dict()
    option_label_mappings= dict()
    label_languages= set()

    def get_label_mappings_0(survey_element, variable_name_prefix=''):

        # If a name prefix was passed in, append a trailing slash before adding to it.
        if variable_name_prefix != '':
            variable_name_prefix= variable_name_prefix + '/'

        # Recur into sections.
        if isinstance(survey_element, (survey.Survey, section.Section) ):
            group_prefix= variable_name_prefix + survey_element[constants.NAME].encode('UTF-8')
            for child_element in survey_element.get('children', []):
                get_label_mappings_0(child_element, variable_name_prefix=group_prefix)

        # Get label(s) associated with a question.
        elif isinstance(survey_element, question.Question):
            # Construct the question name including any "path" prefix.
            question_name= variable_name_prefix + survey_element[constants.NAME].encode('UTF-8')
            question_labels= survey_element.get(constants.LABEL)

            # Record the question's label(s) and associated language(s), if any.
            if question_labels:
                question_label_mappings[question_name]= question_labels
                label_languages.update(question_labels.keys())

            # Get labels associated with multiple-choice questions.
            if isinstance(survey_element, question.MultipleChoiceQuestion):
                question_options_map= dict()
                for option in survey_element.get('children', []):
                    option_name= option[constants.NAME].encode('UTF-8')
                    option_labels= option.get(constants.LABEL)
                    
                    # Record the option's label(s) and associated language(s), if any.
                    if option_labels:
                        question_options_map[option_name]= option_labels
                        label_languages.update(option_labels.keys())

                if question_options_map:
                    option_label_mappings[question_name]= question_options_map

        else:
            print 'Unexpected survey element type "{}"'.format(type(survey_element))

        return

    for survey_element in survey_in['children']:
        get_label_mappings_0(survey_element)

    return question_label_mappings, option_label_mappings, label_languages

# DEBUG
if __name__ == '__main__':
    from pyxform import survey_from
    question_label_mappings, option_label_mappings= get_label_mappings(survey_from.xls('/home/esmail/Downloads/MiningGenderSurveyCompletev141031NOSKIP (1).xls'))
    
    for v in question_label_mappings.itervalues():
        if OPTION_LABEL_MAP_KEY in v:
            print v
            break
    
