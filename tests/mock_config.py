from pytest import fixture

from csci_tool.config import Config


@fixture
def config(mocker):
    mocker.patch('csci_tool.config.Config.load_config')
    mock_config = mocker.MagicMock()
    Config.load_config.return_value = mock_config
    return mock_config
