from arquive.sql_to_dataframe import manage_sql_to_df


if __name__ == "__main__":
    df = manage_sql_to_df()
    print(df.head())
    print(df.info())
    print(f'frontmatter example:{df["frontmatter"][800]["dia_da_semana"]}')