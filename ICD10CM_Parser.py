"""
Name: Varsha Ambuga
Class: CS 521 - Spring 2
Date: 4/27/2022
Final Term Project
Description of Project: ICD10CM Parser - module with classes used in the main
program
"""
import re
import os

class ICD10CM_Record:
    '''
    This class carries attribute and methods of a single record from ICD10CM 
    flat file.
    '''
    
    #this dictionary carries column number key, value as tuple with starting 
    #and ending position of the field
    __ICD10CM_col_pos_dict = {1:(0,5),2:(6,13),3:(14,15),4:(16,76),5:(77,None)}
    __ICD10CM_headers_tuple = ('order_num','ICD10CM_code','HIPAA_covered',\
                         'short_desc','long_desc')
        
    #regexs for each field in a record
    __ICD10CM_validation_regex_tuple = ('^[0-9]{5}$',\
                    '^[A-Z][0-9][0-9AB][0-9AB]?[0-9A-Z]{0,4}$','^0|1$',\
                        '^[\x20-\xFF]+$','^[\x20-\xFF]+$')
    
    def __init__(self, record_string = ''):
        '''
        Parameters
        ----------
        record_string : string, optional
            DESCRIPTION. It is each row string in an ICD10CM file
        '''
        #convert string to tuple based on positions in dictionary
        #each tuple element is a record field
        self.record_list = []
        for i in range(len(ICD10CM_Record.__ICD10CM_headers_tuple)):
            self.record_list.append(record_string[ICD10CM_Record.\
                      __ICD10CM_col_pos_dict[i+1][0]:\
                      ICD10CM_Record.__ICD10CM_col_pos_dict[i+1][1]].strip())
            
    def __record_cleaner(self):
        '''
        This is a private method that cleans the input record by removing 
        whitespace and quotes.
        '''
        for field in self.record_list:
            #use regex to replace any embedded whitespace with a single space
            re.sub('[\s]{2,}',' ',field)
            #remove single or double quotes if it is enclosing the text
            field.strip('\"')
            field.strip('\'')
            
    def record_cleaner_and_validator(self):
        '''
        This method cleans and validates the records by matching them 
        with corresponding regexes.
        After validation, record_list only carries the fields that passed.
        '''
        #based on regex, validate each field
        #each tuple in the list has regex pattern as the first element and the 
        #field value as the second. 
        #Validated tuple has only those elements where regex matches
        self.__record_cleaner()
        self.len_before_validation = len(self.record_list)
        validated_list_with_regex = list(filter(lambda x: re.match(x[0], x[1])\
                != None,list(zip(ICD10CM_Record.\
                __ICD10CM_validation_regex_tuple,self.record_list))))
        #leave out the regex patterns and extract only the elements in 
        #the record
        self.record_list = [x[1] for x in validated_list_with_regex]
    
    def is_record_validated(self):
        '''
        If validation passed for all the fields in the record, the lengths
        before and after validation will be equal and the record can be called
        validated
        '''
        return self.len_before_validation == len(self.record_list)
    
    def __repr__(self):
        '''
        Builtin method. Returns record_list as comma-separated string
        '''
        return ','.join(self.record_list)
    
    def get_record(self):
        '''
        Returns record_list as a tuple
        '''
        return tuple(self.record_list)
    
    #getter and setters for the above three private attributes 
    #since they are class attributes, instance is not required to get or 
    #set them
    def get_ICD10CM_position_dict():
        '''read ICD10CM column position dictionary values'''
        return ICD10CM_Record.__ICD10CM_col_pos_dict
    
    def set_ICD10CM_position_with_header(column_name,tuple_of_start_len):
        '''change ICD10CM column position dictionary keys and values'''
        ICD10CM_Record.__ICD10CM_col_pos_dict[column_name] = tuple_of_start_len
        
    def get_ICD10CM_headers():
        '''read ICD10CM column names'''
        return ICD10CM_Record.__ICD10CM_headers_tuple
    
    def set_ICD10CM_header_at_pos(index,col_name):
        '''change ICD10CM column names'''
        temp_list = list(ICD10CM_Record.__ICD10CM_headers_tuple)
        temp_list[index] = col_name
        ICD10CM_Record.__ICD10CM_headers_tuple = tuple(temp_list)
        
    def get_ICD10CM_field_regex_tuple():
        '''read ICD10CM record regexes'''
        return ICD10CM_Record.__ICD10CM_validation_regex_tuple
    
    def set_ICD10CM_regex_at_pos(index,regex):
        '''change ICD10CM regexes used for validating field value'''
        temp_list = list(ICD10CM_Record.__ICD10CM_validation_regex_tuple)
        temp_list[index] = regex
        ICD10CM_Record.__ICD10CM_validation_regex_tuple = tuple(temp_list)

class FileObject:
    def __init__(self,file_name):
        '''Instantiates file path'''
        self.inpt_file_path = os.path.join(os.getcwd(), file_name)
        
    def read_all(self):
        '''Opens file in read mode.
        Returns list of elements where each element corresponds to a row in the
        file'''
        try:
            self.file = open(self.inpt_file_path,'r')
        except FileNotFoundError():
            print('The file in the path \'{0}\' does not exist.'\
                  .format(self.inpt_file_path))
        else:
            return self.file.readlines()

    def write_all(self, write_text):
        '''Opens file in write mode. Erases the contents of the file before
        writing the text to it.
        '''
        self.file = open(self.inpt_file_path,'w')
        if type(write_text)==list and type(write_text[0])==tuple:
                write_text = [','.join(x) for x in write_text if x != '\n']
                self.file.write('\n'.join(write_text))
        else:
            self.file.writelines(write_text)
        FileObject.remove_text(self,'\n')
        
    def remove_output_files(*file_names):
        ''' Deletes the files in the argument from CWD'''
        for i in file_names:
            if os.path.exists(os.path.join(os.getcwd(), i)) is True:
                os.remove(i)
                
    def append_text(self,append_text):
        '''appends append_text to the file'''
        self.file = open(self.inpt_file_path,'a+')
        self.file.write(append_text)
        #removes blank rows
        FileObject.remove_text(self,'\n')
        return 'Appended'
        
    def remove_text(self, remove_text):
        '''this method is used to reverse appended text to the file'''
        read_text = FileObject.read_all(self)
        self.file = open(self.inpt_file_path,'w')
        for i in read_text:
            if i != remove_text and i != '\n':
                self.file.write(i)
        return 'Deleted'
                
    def __del__(self):
        '''magic method implementation
        This method is called explicitly at the end of life of FileObject'''
        self.file.close()
        del self.file
    
    def does_path_exist(self):
        '''says whether the file path created in init exists'''
        return os.path.exists(self.inpt_file_path)

        
    