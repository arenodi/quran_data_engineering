# Module to setup the database
# Author: arenodi

# Import mariadb module
import mariadb


# function for creating views:
def create_views(database_name, cursor):
    # Flag to return success of database setup
    DID_WORK = True
    # try-except block
    try:
        # Select database
        cursor.execute(f"USE {database_name};")
        cursor.execute("SELECT edition_id FROM editions")
        editions_id = list(sum(cursor.fetchall(), ()))
        for edition_id in editions_id:
            try:
                # Create editions table
                cursor.execute(
                    f"""CREATE OR REPLACE VIEW v_edition{str(edition_id)} AS SELECT
                    jt1.juz_number, jt2.ayah_number, jt2.ayah_text FROM editions edition,
                    json_table(edition, '$.content[*]' columns(
                        juz_number  varchar(10) path '$.number',
                        edId varchar(18) path '$.edId'
                    )) as jt1 inner join
                    json_table(edition, '$.content[*].content[*].ayahs[*]' columns(
                    ayah_number  varchar(10) path '$.number',
                    juz_number varchar(10) path '$.inJuz',
                    ayah_text varchar(1800) path '$.text'
                    )) as jt2 using(juz_number);"""
                )
            except mariadb.Error as e:
                print(f"Error in create editions: {e}")
                raise TypeError(
                    f"Error in the CREATE VIEW v_editions{edition_id} step."
                )
    # handling error
    except (mariadb.Error, TypeError) as error:
        print(f"Error: {error}")
        # Flag false
        DID_WORK = False
    # return boolean value
    return DID_WORK


def test_query(database_name, cursor):
    # Select database
    cursor.execute(f"USE {database_name};")
    cursor.execute(
        """
        SELECT edition INTO @edition FROM editions WHERE edition_id = 1;

        """
    )
    cursor.execute(
        """
        select jt1.juz_number, jt2.ayah_number, jt2.ayah_text from 
            json_table(@edition, '$.content[*]' columns(juz_number  varchar(10) path '$.number')) as jt1 inner join
            json_table(@edition, '$.content[*].content[*].ayahs[*]' columns(
                ayah_number  varchar(10) path '$.number',
                juz_number varchar(10) path '$.inJuz',
                ayah_text varchar(1800) path '$.text'
            )) as jt2 using(juz_number);
            """
    )
    test = cursor.fetchall()
    print(test)
