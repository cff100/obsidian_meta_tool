import configparser
from pathlib import Path
import pytest

from obsidian_meta_tool.config.config_structuration import (
    ValuesNames,
    choose_config_option,
    get_vault_names,
    select_vault_folder,
    create_missing_config_categories,
    save_in_config,
    initialize_config,
    is_config_file_empty,
    access_vault_path,
    access_vault_name,
    access_practical_vault_name,
    access_notes_txt_path,
    auto_access_vault_values
)
from obsidian_meta_tool.config.constants import ConfigNames


# ==============================================================================
# FIXTURES (Ambiente Simulado)
# ==============================================================================

@pytest.fixture
def mock_config_path(tmp_path, monkeypatch):
    """Redireciona o CONFIG_INI_PATH para uma pasta temporária isolada."""
    test_config_file = tmp_path / "test_config.ini"
    monkeypatch.setattr("obsidian_meta_tool.config.config_structuration.CONFIG_INI_PATH", test_config_file)
    return test_config_file


@pytest.fixture
def populated_config(mock_config_path, tmp_path):
    """Cria um arquivo config.ini real na pasta temporária com dados válidos."""
    # Criamos a pasta real simulada para que vault_path.exists() seja True
    fake_vault_dir = tmp_path / "Fake_Vault"
    fake_vault_dir.mkdir()

    config = configparser.ConfigParser()
    opt = ConfigNames.DEFAULT_VAULT_NAME_OPTION
    
    config[ValuesNames.VAULT_PATH.value] = {opt: str(fake_vault_dir)}
    config[ValuesNames.VAULT_NAME.value] = {opt: "Fake Vault"}
    config[ValuesNames.PRACTICAL_VAULT_NAME.value] = {opt: "Fake_Vault"}
    config[ValuesNames.NOTES_TXT_PATH.value] = {opt: "/fake/notes.txt"}
    
    with mock_config_path.open('w', encoding='utf-8') as f:
        config.write(f)
        
    return config, fake_vault_dir, opt


# ==============================================================================
# TESTES DE LÓGICA E TRANSFORMAÇÃO
# ==============================================================================

def test_get_vault_names():
    """Deve extrair o nome da pasta e criar um nome prático sem acentos ou espaços."""
    path = Path("/usuarios/teste/Meu Vault de Anotações")
    name, practical_name = get_vault_names(path)
    
    assert name == "Meu Vault de Anotações"
    assert practical_name == "Meu_Vault_de_Anotacoes"


def test_choose_config_option_bypass():
    """Se bypass_input for True, deve retornar a opção padrão sem pedir input."""
    result = choose_config_option(bypass_input=True)
    assert result == ConfigNames.DEFAULT_VAULT_NAME_OPTION


def test_choose_config_option_default_via_empty_input(monkeypatch):
    """Se o usuário deixar em branco no primeiro input, retorna o padrão."""
    # Simula o usuário apertando 'Enter' sem digitar nada
    monkeypatch.setattr("builtins.input", lambda _: "")
    
    result = choose_config_option(bypass_input=False)
    assert result == ConfigNames.DEFAULT_VAULT_NAME_OPTION


def test_choose_config_option_custom_string(monkeypatch):
    """Deve aceitar e retornar uma string customizada."""
    # side_effect simula múltiplas chamadas do input sequencialmente
    # 1ª chamada: "yes" (não é vazio, então prossegue)
    # 2ª chamada: "option_custom" (escolha final)
    inputs = ["yes", "option_custom"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    
    result = choose_config_option(bypass_input=False)
    assert result == "option_custom"


def test_choose_config_option_digit_shortcut(monkeypatch):
    """Deve transformar atalhos numéricos no formato correto (ex: '3' -> 'option_3')."""
    inputs = ["yes", "3"]
    monkeypatch.setattr("builtins.input", lambda _: inputs.pop(0))
    
    result = choose_config_option(bypass_input=False)
    assert result == "option_3"


# ==============================================================================
# TESTES DE INTERFACE GRÁFICA (TKINTER MOCK)
# ==============================================================================

def test_select_vault_folder_success(monkeypatch):
    """Testa se a seleção da pasta no Tkinter é retornada e o Tk é destruído."""
    class MockTk:
        def withdraw(self): pass
        def destroy(self): self.destroyed = True
        
    mock_tk_instance = MockTk()
    
    # Substituímos o Tkinter real pelos nossos Mocks inofensivos
    monkeypatch.setattr("obsidian_meta_tool.config.config_structuration.Tk", lambda: mock_tk_instance)
    monkeypatch.setattr("obsidian_meta_tool.config.config_structuration.filedialog.askdirectory", lambda **kw: "/fake/selecionado")
    
    result = select_vault_folder()
    
    assert result == "/fake/selecionado"
    assert mock_tk_instance.destroyed is True


# ==============================================================================
# TESTES DE MANIPULAÇÃO DO CONFIG.INI
# ==============================================================================

def test_create_missing_config_categories():
    """Garante que as categorias exigidas são criadas em um config vazio."""
    config = configparser.ConfigParser()
    keys = ["vault_path", "vault_name"]
    
    create_missing_config_categories(config, keys)
    
    assert "vault_path" in config
    assert "vault_name" in config


def test_save_in_config_and_initialize(mock_config_path):
    """Testa o fluxo completo de salvar dados em memória para o disco e ler de volta."""
    values = {
        ValuesNames.VAULT_PATH.value: "/test/path",
        ValuesNames.VAULT_NAME.value: "Test",
        ValuesNames.PRACTICAL_VAULT_NAME.value: "Test",
        ValuesNames.NOTES_TXT_PATH.value: "/test/notes.txt"
    }
    
    # Salva os dados simulando a escolha 'option_1'
    save_in_config(values, "option_1")
    assert mock_config_path.exists()
    
    # Carrega os dados recém-salvos
    config = initialize_config()
    
    assert config[ValuesNames.VAULT_PATH.value]["option_1"] == "/test/path"
    assert not is_config_file_empty(config)


# ==============================================================================
# TESTES DE ACESSO (READERS)
# ==============================================================================

def test_access_functions_success(populated_config):
    """Testa as funções leitoras individuais usando o config populado."""
    config, fake_vault_dir, opt = populated_config
    
    assert access_vault_name(config, opt) == "Fake Vault"
    assert access_practical_vault_name(config, opt) == "Fake_Vault"
    assert access_notes_txt_path(config, opt) == Path("/fake/notes.txt")
    
    # Testa a leitura de path verificando a existência
    path_result = access_vault_path(config, opt)
    assert path_result == fake_vault_dir
    assert isinstance(path_result, Path)


def test_access_vault_path_raises_not_found(populated_config):
    """Deve lançar FileNotFoundError se o Vault configurado foi deletado do disco."""
    config, fake_vault_dir, opt = populated_config
    
    # Simulamos o usuário deletando a pasta do Vault do computador dele
    fake_vault_dir.rmdir() 
    
    with pytest.raises(FileNotFoundError, match="does not exist"):
        access_vault_path(config, opt)


def test_auto_access_vault_values(populated_config):
    """Testa o orquestrador que retorna o dicionário com todas as chaves carregadas."""
    config, fake_vault_dir, opt = populated_config
    
    values = auto_access_vault_values(opt)
    
    assert values[ValuesNames.VAULT_NAME.value] == "Fake Vault"
    assert values[ValuesNames.VAULT_PATH.value] == fake_vault_dir