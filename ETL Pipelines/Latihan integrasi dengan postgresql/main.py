from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, insert

# Membuat database engine
engine = create_engine('postgresql+psycopg2://developer:supersecretpassword@localhost:5432/companydb')

metadata = MetaData()

user_table = Table(
  "users",
  metadata,
  Column("id", Integer, primary_key=True, autoincrement=True),
  Column("first_name", String),
  Column("last_name", String)
)

metadata.create_all(engine)

data_user = [
  {"first_name": "Evans", "last_name": "Sudarsono"},
  {"first_name": "John", "last_name": "Sutiyoso"},
  {"first_name": "Indah", "last_name": "Cahya"},
]

# Menghubungkan database engine
with engine.connect() as connection:
  try:
    print("Terhubung dengan basis data!")
    insert_statement = insert(user_table).values(data_user)
    connection.execute(insert_statement)

    connection.commit()
    print("Data berhasil ditambahkan")
  except Exception as e:
    print(f"Terjadi kesalah: {e}")