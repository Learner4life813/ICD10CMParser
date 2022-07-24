"""
Name: Varsha Ambuga
Class: CS 521 - Spring 2
Date: 4/27/2022
Final Term Project
Description of Project: ICD10CM Parser - main program
"""
import ICD10CM_Parser

#input and output file names as CONSTANTS used in the program
INPUT_FILE_NAME = 'icd10cm_order_2022.txt'
PREVIOUS_RELEASE_FILE_NAME = 'icd10cm_order_2021.txt'

ERROR_FILE_NAME = 'icd10cm_error_rows.txt'
VALIDATED_FILE_NAME = 'icd10cm_validated.txt'
RELEASE_NOTES_FILE_NAME = 'ReleaseNotes.txt'

validated_output_list = []
error_output_list = []
previous_release_list = []

def validate_ICD10CM_records():
    '''
    This method reads the contents of the current release file of ICD10CM,
    validates each record and generates two lists - validated rows and error
    rows
    '''
    file_obj = ICD10CM_Parser.FileObject(INPUT_FILE_NAME)
    file_contents_list = file_obj.read_all()
    del(file_obj)

    for line_str in file_contents_list:
        
        record_obj = ICD10CM_Parser.ICD10CM_Record(line_str.strip('\n'))
        record_obj.record_cleaner_and_validator()
        if record_obj.is_record_validated():
            validated_output_list.append(record_obj.get_record())
        else:
            error_output_list.append(line_str)
        del(record_obj)

def generate_output_files(val_file_name,error_file_name):
    '''
    If error list has elements, error file is created.
    If not, validated rows file is generated
    '''
    #if 'validated' or 'error' files already exist, delete them
    ICD10CM_Parser.FileObject.remove_output_files(val_file_name,\
                                              error_file_name)
    #if error rows>0, create output rows error file
    if len(error_output_list) > 0:
        error_file_obj = ICD10CM_Parser.FileObject(error_file_name)
        error_file_obj.write_all(error_output_list)
        del(error_file_obj)
    else:
        validated_file_obj = ICD10CM_Parser.FileObject(val_file_name)
        validated_file_obj.write_all(validated_output_list)
        del(validated_file_obj) 
        
def extract_ICD10CM_codes(list_of_tuples):
    '''
    Getting the second value in every tuple of the list into a set.
    Second value because in every ICD10CM record, ICD10CM code is the second 
    field.
    '''
    return {x[1] for x in list_of_tuples}

def generate_release_notes(rel_notes_file_name):  
    '''
    If there are no errors in the input file, release notes is generated.
    Release notes carries the difference between the current release being 
    validated and the previous release. It is assumed that the previous 
    release file is always present and is already validated, so there cannot
    be bad data in there.
    '''
    if len(validated_output_list) > 0:
        #Compare current release code sets with that of previous release
        validated_code_set = extract_ICD10CM_codes(validated_output_list)
        #get previous release's code set
        prev_rel_obj = ICD10CM_Parser.FileObject(PREVIOUS_RELEASE_FILE_NAME)
        previous_rel_lines = prev_rel_obj.read_all()
        del(prev_rel_obj)
        
        for line_str in previous_rel_lines:
            record_obj = ICD10CM_Parser.ICD10CM_Record(line_str)
            previous_release_list.append(record_obj.get_record())
            
        previous_code_set = extract_ICD10CM_codes(previous_release_list)
        
        new_codes = validated_code_set.difference(previous_code_set)
        deprecated_codes = previous_code_set.difference(validated_code_set)
        
        release_notes_text = "New codes: "+ ("None" if len(new_codes)==0 \
            else ', '.join(new_codes)) + "\n\nDeprecated codes: " + ('None' \
            if len(deprecated_codes)==0 else ', '.join(deprecated_codes))
        
        rel_notes_file_obj = ICD10CM_Parser.FileObject(rel_notes_file_name)
        rel_notes_file_obj.write_all(release_notes_text)
        del(rel_notes_file_obj)
#############################################################################    
if __name__ == '__main__':
    ########################################################################
    #unittest-1 - scenario: check the contents of release notes
    val_file_name = 'Scenario1-'+VALIDATED_FILE_NAME
    err_file_name = 'Scenario1-'+ERROR_FILE_NAME
    rel_file_name = 'Scenario1-'+RELEASE_NOTES_FILE_NAME
    new_code = 'K31A21'
    
    validate_ICD10CM_records()
    generate_output_files(val_file_name,err_file_name)
    generate_release_notes(rel_file_name)
    file_obj = ICD10CM_Parser.FileObject(rel_file_name)
    print('Test #1 - Scenarios validated')
    print('-'*50)
    assert file_obj.does_path_exist()==True, 'Release Notes file does \
not exist.'
    print('The Release notes file is generated in the CWD: ',rel_file_name)
    Release_notes_content = file_obj.read_all()
    del(file_obj)
    assert new_code in ' '.join(Release_notes_content), 'Release notes does \
not contain the new code: '+new_code
    print('The release notes contain the new code: ',new_code)
    print('-'*50)
    print('Here is the entire release notes:')
    print('-'*50)
    print('\n'.join(Release_notes_content))
    print('-'*50)
    print('Test #1 is successful.')
    print('-'*50)
    
    #######################################################################
    #unittest-2 - scenario: append bad data to input file and assert it in
    #error file
    val_file_name = 'Scenario2-'+VALIDATED_FILE_NAME
    err_file_name = 'Scenario2-'+ERROR_FILE_NAME
    append_str = '95529 HA33X3  1 Noise effects on inner ear, \
bilateral1                       Noise effects on inner ear, bilateral1'
    bad_code = 'HA33X3'
    
    file_obj = ICD10CM_Parser.FileObject(INPUT_FILE_NAME)
    append_status = file_obj.append_text('\n'+append_str)
    del(file_obj)
    #run the program
    if append_status == 'Appended':
        validate_ICD10CM_records()
        generate_output_files(val_file_name,err_file_name)
        print('-'*50)
        print('Test #2 - Scenarios validated')
        print('-'*50)
        file_obj = ICD10CM_Parser.FileObject(err_file_name)
        assert file_obj.does_path_exist()==True, 'Error file is not generated.'
        print('The error file is generated in the CWD: ',err_file_name)
        Error_file_contents = file_obj.read_all()
        del(file_obj)
        assert bad_code in ' '.join(Error_file_contents), 'Error file does \
not contain the bad code: '+bad_code
        print('The error file contains the appended bad code: ',bad_code)
        print('-'*50)
        file_obj = ICD10CM_Parser.FileObject(INPUT_FILE_NAME)
        remove_status = file_obj.remove_text(append_str)
        if remove_status == 'Deleted':
            print('Test #2 is successful.')
        else:
            print('The appended text could not be removed.')
        del(file_obj)
    else:
        print('Test #2 is incomplete.')

