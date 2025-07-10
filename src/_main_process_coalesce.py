from coalesce._cls_etl_coalesce_ import EtlCoalesceTel
import sys
import os

current_folder = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_folder)
sys.path.append(current_folder)    
os.path.join(project_root, 'src')

def main():

    schema = 'bbdd_cos_bog_chubb'

    table = 'tb_asignacion_ban100_v2_coalesce'
    
    cuenta = 'numero_id'
    sql_file_path = os.path.join(project_root, 'sql', '_sql_coalesce_chubb_ban100.sql')

    phone_columns = [
                'celular_personal', 
                    'telefono_domicilio',
                    'repoblacion_repo1',
                    'repoblacion_repo2',
                    'repoblacion_repo3',
                    'repoblacion_repo5',
                    'repoblacion_repo6'
    ]
    processor = EtlCoalesceTel(
        schema=schema,
        table=table,
        sql_file_path=sql_file_path,
        cuenta=cuenta,
        phone_columns=phone_columns
    )

    try:
        processor.coalesce_etl()
        processor.load_data()
    except Exception as e:
        print(f"❌ Error en el proceso principal: {str(e)}")

if __name__ == '__main__':
    main()
