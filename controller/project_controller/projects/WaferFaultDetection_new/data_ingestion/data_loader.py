from project_library_layer.initializer.initializer import Initializer
from exception_layer.data_getter_exception.data_getter_exception import DataGetterException

import sys


class DataGetter:
    """
    This class shall  be used for obtaining the data from the source for training.

    Written By: iNeuron Intelligence
    Version: 1.0
    Revisions: None

    """

    def __init__(self, project_id, file_object, logger_object):
        try:
            self.initializer = Initializer()
            self.training_file_path = self.initializer.get_training_file_from_db_path(project_id=project_id)
            self.training_file_name = self.initializer.get_training_input_file_name()
            self.file_object = file_object
            self.logger_object = logger_object
        except Exception as e:
            data_getter_exception = DataGetterException(
                "Failed during object instantiation in module [{0}] class [{1}] method [{2}]"
                    .format(self.__module__, DataGetter.__name__,
                            "__init__"))
            raise Exception(data_getter_exception.error_message_detail(str(e), sys)) from e

    def get_data(self):
        """
        Method Name: get_data
        Description: This method reads the data from source.
        Output: A pandas DataFrame.
        On Failure: Raise Exception

         Written By: iNeuron Intelligence
        Version: 1.0
        Revisions: None

        """
        try:
            self.logger_object.log('Entered the get_data method of the Data_Getter class')
            # self.data= pd.read_csv(self.training_file) # reading the data file
            response = self.file_object.read_file_content(self.training_file_path, self.training_file_name)
            if not response['status']:
                raise Exception(response)
            data = None
            if 'file_content' in response:
                data = response['file_content']
            if data is None:
                raise Exception("data not found for training")
            if data.shape[0] == 0:
                raise Exception("Empty dataset. we don't have any data")
            self.logger_object.log('Data Load Successful.Exited the get_data method of the Data_Getter class')
            return data
        except Exception as e:
            data_getter_exception = DataGetterException(
                "Failed in getting data in module [{0}] class [{1}] method [{2}]"
                    .format(self.__module__, DataGetter.__name__,
                            self.get_data.__name__))
            raise Exception(data_getter_exception.error_message_detail(str(e), sys)) from e
