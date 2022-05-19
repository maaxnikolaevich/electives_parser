# def with_connection(f):
#     def with_connection_(*args, **kwargs):
#         conn = mysql.connector.Connect("my redacted credentials")
#         try:
#             result = f(*args, connection=conn, **kwargs)
#         except:
#             conn.rollback()
#             print("SQL failed")
#             raise
#         else:
#             conn.commit()
#         finally:
#             conn.close()
#         return result
#     return with_connection_
