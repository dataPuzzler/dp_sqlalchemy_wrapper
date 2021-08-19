import pytest 


@pytest.fixture(scope="module")
def BaseConfig():
    from dp_sqlalchemy_wrapper.base_config import BaseConfig
    return BaseConfig


@pytest.fixture(scope="module")
def SampleBaseConfig(BaseConfig):
    from dp_sqlalchemy_wrapper.base_config import UnsetConfigProperty
    class SampleConf(BaseConfig):
        a = UnsetConfigProperty
        b = UnsetConfigProperty

        @classmethod
        def get_required_properties(cls):
            return ["a", "b"]

    return SampleConf


def test_valid_config(SampleBaseConfig):
    class Config(SampleBaseConfig):
        a = 12
        b = 44
    
    assert Config().validate() 

def test_invalid_config_triggers_exception(SampleBaseConfig):

    from dp_sqlalchemy_wrapper.base_config  import UnsetRequiredConfigPropertyException
    with pytest.raises(UnsetRequiredConfigPropertyException):
        class Config(SampleBaseConfig):
            b = 44

        Config().validate()

def test_invalid_config_correct_exception_properties(SampleBaseConfig):

    from dp_sqlalchemy_wrapper.base_config  import UnsetRequiredConfigPropertyException
    try:
        class Config(SampleBaseConfig):
            b = 44

        Config().validate()
    except(UnsetRequiredConfigPropertyException) as ex:
        assert ex.unset_required_properties == ['a']
        