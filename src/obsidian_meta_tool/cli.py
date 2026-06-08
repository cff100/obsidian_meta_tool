import argparse

from obsidian_meta_tool.config.config_structuration import process_configuration
from obsidian_meta_tool.config.paths import DataPaths
# from obsidian_meta_tool.database.database_creation import dataframe_creation


def main():
    # 1. Cria o orquestrador principal
    parser = argparse.ArgumentParser(
        prog="meta_tool",
        description="Central Command Line Interface for the Obsidian Meta Tool.",
        epilog="Use 'python cli.py <command> --help' to see specific options for each command."
    )
    
    # 2. Cria o gerenciador de subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Available core commands")

    # ==========================================
    # TASK 1: Configuração (do config.ini)
    # ==========================================
    parser_config = subparsers.add_parser(
        "config", 
        help="Starts the interactive configuration for the vault."
    )
    parser_config.add_argument(
        "--bypass", 
        action="store_true", 
        help="Automatically choose the default config option (option_1) without asking inputs."
    )

    # ==========================================
    # TASK 2: Mapeamento dos caminhos do vault
    # ==========================================
    parser_paths = subparsers.add_parser(
        "update-paths", 
        help="Captures the vault file paths and saves them to a text document."
    )
    parser_paths.add_argument(
        "--vault", 
        type=str, 
        help="Specify the vault option (e.g., option_2). Uses default (option_1) if omitted.", 
        default=None
    )

    # ==========================================
    # TASK 3: Banco de Dados 
    # ==========================================
    # parser_df = subparsers.add_parser(
    #     "create-dataframe", 
    #     help="Reads the captured paths and generates the master Parquet DataFrame."
    # )
    # parser_df.add_argument(
    #     "--vault", 
    #     type=str, 
    #     help="Specify the vault option (e.g., option_2). Uses default if omitted.", 
    #     default=None
    # )

    # 3. Lê e interpreta o que o usuário digitou no terminal
    args = parser.parse_args()

    # 4. Executa a função correspondente ao comando escolhido
    if args.command == "config":
        print("Starting configuration...")
        process_configuration(bypass_input=args.bypass)
        print("Configuration complete!")

    elif args.command == "update-paths":
        print("Capturing vault file paths...")
        if args.vault:
            DataPaths.capture_vault_file_paths(vault_option=args.vault)
        else:
            DataPaths.capture_vault_file_paths()
        print("Paths captured and saved successfully!")

    # elif args.command == "create-dataframe":
    #     print("Building the general DataFrame...")
    #     if args.vault:
    #         dataframe_creation(vault_option=args.vault)
    #     else:
    #         dataframe_creation()
    #     print("DataFrame generated successfully!")

    else:
        # Se o usuário rodar o arquivo sem passar nenhum comando, exibe a ajuda nativa
        parser.print_help()


if __name__ == "__main__":
    main()