
from utils.imports import *
from configs.user_constants import *


def wait_for_loader(driver):
    """ """
    pass


def read_input_data(env, test_sub_type):
    """ """
    try:
        if test_sub_type == 'Sanity':
            if env == 'UAT':
                input_data = pd.read_excel(INPUT_SHEET, sheet_name='', index_col=[0])

        json_data = list()
        input_data.fillna('', inplace=True)

        unique_indexes = input_data.index.drop_duplicates()
        for index in unique_indexes:
            test = {}
            filtered_data = input_data[input_data.index.isin([index])]
            test.update({index: filtered_data.to_dict(orient='records')})
            json_data.append(json.dumps(test))

        return json_data
    except Exception as exp:
        raise exp


def elem_exists(driver, identifier):
    """ """
    try:
        if driver.find_element(By.XPATH, identifier).is_displayed() or \
                driver.find_element(By.XPATH, identifier).is_enabled():
            return True
    except NoSuchElementException:
        return False
    except Exception as exp:
        raise exp


def encode_b64(raw_string):
    """ """
    try:
        pass_bytes = raw_string.encode('ascii')
        pass_bytes_b64 = base64.b64encode(pass_bytes)

        pass_encoded = pass_bytes_b64.decode('ascii')
        return pass_encoded
    except Exception as exp:
        raise exp


def decode_b64(encoded_string):
    """ """
    try:
        pass_bytes = encoded_string.encode('ascii')
        pass_bytes_b64_decoded = base64.b64decode(pass_bytes)

        pass_decoded = pass_bytes_b64_decoded.decode('ascii')
        return pass_decoded
    except Exception as exp:
        raise exp

