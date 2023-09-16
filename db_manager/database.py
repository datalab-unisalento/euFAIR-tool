import datetime
import inspect
import mysql.connector
import numpy as np

import log.error
import utility.constants

version = 'beta'

# dataBase = mysql.connector.connect(
#     host="localhost",
#     port="3308",
#     user="root",
#     passwd="password",
#     database="euFAIR"
# )

endpoint = 'eufairinstance.ctrcvp1pzgnw.eu-north-1.rds.amazonaws.com'
user = 'admin'
password = 'BymGSSmpDDnzvU5VCj8v'
port = '3306'
database_name = 'euFAIR'

my_database = mysql.connector.connect(
    host=endpoint,
    port=port,
    user=user,
    passwd=password,
    database=database_name
)

cursor_object = my_database.cursor()


def search_dataset(searched):
    searched = searched.strip()
    sql = """SELECT id, name, holder, description, lastUpdate
            FROM Dataset
            WHERE id LIKE %s
            OR name LIKE %s"""

    cursor_object.execute(sql, ('%' + searched + '%', '%' + searched + '%'))
    results = cursor_object.fetchall()
    return results

def search_holder(searched):
    searched = searched.strip()
    sql = """SELECT id, name, description
            FROM Holder
            WHERE id LIKE %s
            OR name LIKE %s"""

    cursor_object.execute(sql, ('%' + searched + '%', '%' + searched + '%'))
    results = cursor_object.fetchall()
    return results


def retrieve_all_id(catalogue=''):
    if catalogue == '':
        sql = """SELECT id
                FROM euFAIR.Dataset"""

    else:

        sql = f"""SELECT id
                    FROM euFAIR.Dataset
                    WHERE catalogue = '{catalogue}'"""

    cursor_object.execute(sql)

    datasets_id = cursor_object.fetchall()

    nor_datasets = []

    for dataset in datasets_id:
        nor_datasets.append(dataset[0])

    return nor_datasets


def retrieve_all_name(catalogue):
    sql2 = f"""SELECT name
                FROM euFAIR.Dataset
                WHERE catalogue = '{catalogue}'"""

    nor_datasets = []

    cursor_object.execute(sql2)

    datasets_name = cursor_object.fetchall()

    for dataset in datasets_name:
        nor_datasets.append(dataset[0])

    return nor_datasets


def retrieve_id_to_update():
    sql = """SELECT id, idEuropa, catalogue
            FROM euFAIR.Dataset
            WHERE lastChecked is NULL
            OR (DATEDIFF(lastChecked, (DATE_ADD(lastUpdate, INTERVAL accPeriodicity HOUR))) < 0
                AND DATEDIFF(NOW(), (DATE_ADD(lastUpdate, INTERVAL accPeriodicity HOUR))) > 0)
            OR accPeriodicity = 0
            ORDER BY accPeriodicity DESC"""

    cursor_object.execute(sql)

    return cursor_object.fetchall()


def add_new_database(dataset, catalogue):
    try:
        if 'id' in dataset and dataset['id']:
            id_ = dataset['id']
            acc_per = 'NULL'
            name = 'NULL'
            metadata_modified = 'NULL'
            holder_identifier = 'NULL'
            notes = 'NULL'

            if 'name' in dataset and dataset['name']:
                name = dataset['name']

            if 'extras' in dataset and dataset['extras']:
                for extra in dataset['extras']:
                    if extra['key'] == 'frequency':
                        for frequency in utility.constants.constants.FREQUENCIES:
                            if extra['value'] == frequency:
                                acc_per = utility.constants.constants.FREQUENCIES[frequency]

            if 'metadata_modified' in dataset and dataset['metadata_modified']:
                metadata_modified = dataset['metadata_modified']

            if 'holder_identifier' in dataset and dataset['holder_identifier']:
                holder_identifier = dataset['holder_identifier']

            if 'notes' in dataset and dataset['notes']:
                notes = dataset['notes']

            sql = """SELECT id
                    FROM euFAIR.Dataset
                    WHERE id = %s"""

            values = (dataset['id'],)

            cursor_object.execute(sql, values)

            if cursor_object.fetchall():
                dataset['id'] += '&2'

            sql = """INSERT INTO euFAIR.Dataset(id, name, lastUpdate, lastChecked, accPeriodicity, holder, description, catalogue)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""

            values = (id_, name, metadata_modified,
                      datetime.datetime.now(), acc_per, holder_identifier, notes, catalogue)
            cursor_object.execute(sql, values)

            my_database.commit()
    except mysql.connector.errors.IntegrityError as e:
        log.error.error(e, inspect.currentframe())
        raise IntegrityError


def create_new_metadata_evaluation(dataset_id, portal, method, result, is_modified, file_id):
    sql = "INSERT INTO `euFAIR`.`Metadata` (`idDataset`, `idFile`, `portal`, `datetime`, `method`, `F1`, `F2`, `F3`, \
    `F4`, `G_F`, `A1`, `A1.1`, `A1.2`, `A2`, `G_A`, `I1`, `I2`, `I3`, `G_I`, `R1`, `R1.1`, `R1.2`, `R1.3`, `G_R`, `isModified`, `v`) \
    VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"

    issued = str(datetime.datetime.now())
    val = (dataset_id, file_id, portal, issued, method,
           result["F"]["F1"], result["F"]["F2"], result["F"]["F3"], result["F"]["F4"], result["F"]["GUIDELINES"],
           result["A"]["A1"], result["A"]["A1.1"], result["A"]["A1.2"], result["A"]["A2"], result["A"]["GUIDELINES"],
           result["I"]["I1"], result["I"]["I2"], result["I"]["I3"], result["I"]["GUIDELINES"],
           result["R"]["R1"], result["R"]["R1.1"], result["R"]["R1.2"], result["R"]["R1.3"], result["R"]["GUIDELINES"],
           is_modified, version)

    cursor_object.execute(sql, val)
    my_database.commit()


def create_new_data_evaluation(dataset_id, file_id, file_name, method, result, is_modified):
    sql = "INSERT INTO `euFAIR`.`Data` (`idDataset`,`idFile`, `fileName`, `datetime`, `method`,  `F1`, `F2`, `F3`, `F4`,\
            `G_F`, `A1`, `A1.1`, `A1.2`, `A2`, `G_A`, `I1`, `I2`, `I3`, `G_I`, `R1`, `R1.1`, `R1.2`, `R1.3`, `G_R`,`isModified`, `v`) \
            VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"

    issued = str(datetime.datetime.now())
    val = (dataset_id, file_id, file_name, issued, method,
           result["F"]["F1"], result["F"]["F2"], result["F"]["F3"], result["F"]["F4"], result["F"]["GUIDELINES"],
           result["A"]["A1"], result["A"]["A1.1"], result["A"]["A1.2"], result["A"]["A2"], result["A"]["GUIDELINES"],
           result["I"]["I1"], result["I"]["I2"], result["I"]["I3"], result["I"]["GUIDELINES"],
           result["R"]["R1"], result["R"]["R1.1"], result["R"]["R1.2"], result["R"]["R1.3"], result["R"]["GUIDELINES"],
           is_modified, version)

    cursor_object.execute(sql, val)
    my_database.commit()


def load_metadata_update(dataset_id):
    sql = "SELECT lastMetadataUpdate FROM `euFAIR`.`Dataset`" \
          "WHERE `idDataset` = %s"

    cursor_object.execute(sql, dataset_id)

    last_update = cursor_object.fetchall()

    return datetime.datetime.strptime(last_update[0][0], "%Y-%m-%d %H:%M:%S.%f")


def check_if_new(dataset_id):
    sql = "SELECT * FROM `euFAIR`.`Dataset`" \
          "WHERE `idDataset` = %s"

    cursor_object.execute(sql, dataset_id)

    if len(cursor_object.fetchall()) > 0:
        sql = "INSERT INTO `euFAIR`.`urlDataset` (`idDataset`)" \
              "VALUES %s"

        cursor_object.execute(sql, dataset_id)


def create_id_list(dataset_id, holder, name):
    sql = "INSERT INTO `euFAIR`.`Dataset` (`idDataset`, `holderDataset`, `nameDataset`)" \
          "VALUES (%s, %s, %s)"

    cursor_object.execute(sql, (dataset_id, holder, name))
    print("added to database")

    my_database.commit()


def add_eu(dataset_id):
    if dataset_id[-3:].find("~~") != -1:
        dataset_id_ita = dataset_id[:-3]
    else:
        dataset_id_ita = dataset_id

    print(f"saving {dataset_id} as {dataset_id_ita}")

    cursor_object = my_database.cursor(buffered=True)

    sql = "SELECT COUNT(*)" \
          "FROM `euFAIR`.`Dataset`" \
          "WHERE `idDataset` LIKE %s" \
          "OR `nameDataset` LIKE %s"

    param = (dataset_id_ita + '%', dataset_id_ita + '%')

    cursor_object.execute(sql, param)

    print(cursor_object.rowcount)

    if cursor_object.rowcount == 1:

        print("query 1 good")

        sql2 = "UPDATE `euFAIR`.`Dataset` " \
               "SET `idEuropa` = %s " \
               "WHERE `idDataset` LIKE %s" \
               "OR `nameDataset` LIKE %s"

        param2 = (dataset_id, dataset_id_ita + '%', dataset_id_ita + '%')

        cursor_object.execute(sql2, param2)

        my_database.commit()

        print("query 2 good")

    else:
        print("error with id: " + dataset_id)


def retrieve_id():
    sql = "SELECT `idDataset`, `idEuropa` " \
          "FROM `euFAIR`.`Dataset` " \
          "WHERE DATEDIFF(%s, lastUpdate) > 3 " \
          "OR lastUpdate is null " \
          "ORDER BY lastUpdate ASC"

    param = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),)

    print(sql)
    cursor_object.execute(sql, param)

    dataset_id = cursor_object.fetchall()

    return dataset_id


def set_update_date(dataset_id):
    sql = "UPDATE `euFAIR`.`Dataset` " \
          "SET `lastUpdate` = %s " \
          "WHERE `id` = %s"

    parameter = (datetime.datetime.now().date(), dataset_id)
    cursor_object.execute(sql, parameter)

    my_database.commit()


def get_last_meta_eval(dataset_id, portal, method):
    try:
        if portal == "data.europa.eu" or portal == "dati.gov.it" or portal == "default":

            sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                            MIN(F2), AVG(F2), MAX(F2),
                            MIN(F3), AVG(F3), MAX(F3),
                            MIN(F4), AVG(F4), MAX(F4),
                            MIN(G_F), AVG(G_F), MAX(G_F),
                            MIN(A1), AVG(A1), MAX(A1),
                            MIN(`A1.1`), AVG(`A1.1`), MAX(`A1.1`),
                            MIN(`A1.2`), AVG(`A1.2`), MAX(`A1.2`),
                            MIN(G_A), AVG(G_A), MAX(G_A),
                            MIN(I1), AVG(I1), MAX(I1),
                            MIN(I2), AVG(I2), MAX(I2),
                            MIN(I3), AVG(I3), MAX(I3),
                            MIN(G_I), AVG(G_I), MAX(G_I),
                            MIN(R1), AVG(R1), MAX(R1),
                            MIN(`R1.1`), AVG(`R1.1`), MAX(`R1.1`),
                            MIN(`R1.2`), AVG(`R1.2`), MAX(`R1.2`),
                            MIN(`R1.3`), AVG(`R1.3`), MAX(`R1.3`),
                            MIN(G_R), AVG(G_R), MAX(G_R)
                    FROM `euFAIR`.`Metadata`
                    WHERE idDataset = %s
                    AND method = %s
                    AND portal= %s"""

            # `Metadata`.`F1`,
            #         `Metadata`.`F2`,
            #         `Metadata`.`F3`,
            #         `Metadata`.`F4`,
            #         `Metadata`.`G_F`,
            #         `Metadata`.`A1`,
            #         `Metadata`.`A1.1`,
            #         `Metadata`.`A1.2`,
            #         `Metadata`.`A2`,
            #         `Metadata`.`G_A`,
            #         `Metadata`.`I1`,
            #         `Metadata`.`I2`,
            #         `Metadata`.`I3`,
            #         `Metadata`.`G_I`,
            #         `Metadata`.`R1`,
            #         `Metadata`.`R1.1`,
            #         `Metadata`.`R1.2`,
            #         `Metadata`.`R1.3`,
            #         `Metadata`.`G_R`
            #         FROM `euFAIR`.`Metadata`
            #         WHERE idDataset = %s
            #         AND method = %s
            #         AND portal= %s
            #         ORDER BY datetime DESC
            #         LIMIT 10"""

            parameter = (dataset_id, method, portal)
            cursor_object.execute(sql, parameter)

            last_eval = cursor_object.fetchall()

        else:
            sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                            MIN(F2), AVG(F2), MAX(F2),
                            MIN(F3), AVG(F3), MAX(F3),
                            MIN(F4), AVG(F4), MAX(F4),
                            MIN(G_F), AVG(G_F), MAX(G_F),
                            MIN(A1), AVG(A1), MAX(A1),
                            MIN(A1.1), AVG(A1.1), MAX(A1.1),
                            MIN(A1.2), AVG(A1.2), MAX(A1.2),
                            MIN(G_A), AVG(G_A), MAX(G_A),
                            MIN(I1), AVG(I1), MAX(I1),
                            MIN(I2), AVG(I2), MAX(I2),
                            MIN(I3), AVG(I3), MAX(I3),
                            MIN(G_I), AVG(G_I), MAX(G_I),
                            MIN(R1), AVG(R1), MAX(R1),
                            MIN(R1.1), AVG(R1.1), MAX(R1.1),
                            MIN(R1.2), AVG(R1.2), MAX(R1.2),
                            MIN(R1.3), AVG(R1.3), MAX(R1.3),
                            MIN(G_R), AVG(G_R), MAX(G_R)
                    FROM `euFAIR`.`Metadata`
                    WHERE idDataset = %s
                    AND method = %s
                    AND NOT portal= "data.europe.eu"
                    AND NOT portal= "dati.gov.it"""

            parameter = (dataset_id, method)

            cursor_object.execute(sql, parameter)

            last_eval = cursor_object.fetchall()[0]
            last_eval = np.array(last_eval).reshape(1, -1)

        print(last_eval[0])


        results = {'F':{'F1': {'min': last_eval[0][0],
                          'avg': float(last_eval[0][1]),
                          'max': last_eval[0][2]},
                   'F2': {'min': last_eval[0][3],
                          'avg': float(last_eval[0][4]),
                          'max': last_eval[0][5]},
                   'F3': {'min': last_eval[0][6],
                          'avg': float(last_eval[0][7]),
                          'max': last_eval[0][8]},
                   'F4': {'min': last_eval[0][9],
                          'avg': float(last_eval[0][10]),
                          'max': last_eval[0][11]},
                   'G_F': {'min': last_eval[0][12],
                          'avg': float(last_eval[0][13]),
                          'max': last_eval[0][14]}},
                   'A':{'A1': {'min': last_eval[0][15],
                          'avg': float(last_eval[0][16]),
                          'max': last_eval[0][17]},
                   'A1.1': {'min': last_eval[0][18],
                          'avg': float(last_eval[0][19]),
                          'max': last_eval[0][20]},
                   'A1.2': {'min': last_eval[0][21],
                          'avg': float(last_eval[0][22]),
                          'max': last_eval[0][23]},
                   'G_A': {'min': last_eval[0][24],
                          'avg': float(last_eval[0][25]),
                          'max': last_eval[0][26]}},
                   'I': {'I1': {'min': last_eval[0][27],
                          'avg': float(last_eval[0][28]),
                          'max': last_eval[0][29]},
                   'I2': {'min': last_eval[0][30],
                          'avg': float(last_eval[0][31]),
                          'max': last_eval[0][32]},
                   'I3': {'min': last_eval[0][33],
                          'avg': float(last_eval[0][34]),
                          'max': last_eval[0][35]},
                   'G_I': {'min': last_eval[0][36],
                          'avg': float(last_eval[0][37]),
                          'max': last_eval[0][38]}},
                  'R':{'R1': {'min': last_eval[0][39],
                          'avg': float(last_eval[0][40]),
                          'max': last_eval[0][41]},
                   'R1.1': {'min': last_eval[0][42],
                          'avg': float(last_eval[0][43]),
                          'max': last_eval[0][44]},
                   'R1.2': {'min': last_eval[0][45],
                          'avg': float(last_eval[0][46]),
                          'max': last_eval[0][47]},
                   'R1.3': {'min': last_eval[0][48],
                          'avg': float(last_eval[0][49]),
                          'max': last_eval[0][50]},
                   'G_R': {'min': last_eval[0][51],
                          'avg': float(last_eval[0][52]),
                          'max': last_eval[0][53]},
                   }}

    except:
        results = None


    return results


def get_distributions(dataset_id):
    sql = """SELECT DISTINCT `Data`.`fileName`
        FROM `euFAIR`.`Data`
        WHERE id = %s"""

    param = (dataset_id,)

    cursor_object.execute(sql, param)

    distributions = cursor_object.fetchall()

    return distributions


def get_last_data_eval(dataset_id, file_name, method):
    if file_name == "none":
        return [(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)]

    sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                    MIN(F2), AVG(F2), MAX(F2),
                    MIN(F3), AVG(F3), MAX(F3),
                    MIN(F4), AVG(F4), MAX(F4),
                    MIN(G_F), AVG(G_F), MAX(G_F),
                    MIN(A1), AVG(A1), MAX(A1),
                    MIN(`A1.1`), AVG(`A1.1`), MAX(`A1.1`),
                    MIN(`A1.2`), AVG(`A1.2`), MAX(`A1.2`),
                    MIN(G_A), AVG(G_A), MAX(G_A),
                    MIN(I1), AVG(I1), MAX(I1),
                    MIN(I2), AVG(I2), MAX(I2),
                    MIN(I3), AVG(I3), MAX(I3),
                    MIN(G_I), AVG(G_I), MAX(G_I),
                    MIN(R1), AVG(R1), MAX(R1),
                    MIN(`R1.1`), AVG(`R1.1`), MAX(`R1.1`),
                    MIN(`R1.2`), AVG(`R1.2`), MAX(`R1.2`),
                    MIN(`R1.3`), AVG(`R1.3`), MAX(`R1.3`),
                    MIN(G_R), AVG(G_R), MAX(G_R)
            FROM `euFAIR`.`Data`
            WHERE idDataset = %s
            AND fileName = %s
            AND method = %s"""

    param = (dataset_id, file_name, method)

    cursor_object.execute(sql, param)

    last_eval = cursor_object.fetchall()

    results = {'F': {'F1': {'min': last_eval[0][0],
                            'avg': float(last_eval[0][1]),
                            'max': last_eval[0][2]},
                     'F2': {'min': last_eval[0][3],
                            'avg': float(last_eval[0][4]),
                            'max': last_eval[0][5]},
                     'F3': {'min': last_eval[0][6],
                            'avg': float(last_eval[0][7]),
                            'max': last_eval[0][8]},
                     'F4': {'min': last_eval[0][9],
                            'avg': float(last_eval[0][10]),
                            'max': last_eval[0][11]},
                     'G_F': {'min': last_eval[0][12],
                             'avg': float(last_eval[0][13]),
                             'max': last_eval[0][14]}},
               'A': {'A1': {'min': last_eval[0][15],
                            'avg': float(last_eval[0][16]),
                            'max': last_eval[0][17]},
                     'A1.1': {'min': last_eval[0][18],
                              'avg': float(last_eval[0][19]),
                              'max': last_eval[0][20]},
                     'A1.2': {'min': last_eval[0][21],
                              'avg': float(last_eval[0][22]),
                              'max': last_eval[0][23]},
                     'G_A': {'min': last_eval[0][24],
                             'avg': float(last_eval[0][25]),
                             'max': last_eval[0][26]}},
               'I': {'I1': {'min': last_eval[0][27],
                            'avg': float(last_eval[0][28]),
                            'max': last_eval[0][29]},
                     'I2': {'min': last_eval[0][30],
                            'avg': float(last_eval[0][31]),
                            'max': last_eval[0][32]},
                     'I3': {'min': last_eval[0][33],
                            'avg': float(last_eval[0][34]),
                            'max': last_eval[0][35]},
                     'G_I': {'min': last_eval[0][36],
                             'avg': float(last_eval[0][37]),
                             'max': last_eval[0][38]}},
               'R': {'R1': {'min': last_eval[0][39],
                            'avg': float(last_eval[0][40]),
                            'max': last_eval[0][41]},
                     'R1.1': {'min': last_eval[0][42],
                              'avg': float(last_eval[0][43]),
                              'max': last_eval[0][44]},
                     'R1.2': {'min': last_eval[0][45],
                              'avg': float(last_eval[0][46]),
                              'max': last_eval[0][47]},
                     'R1.3': {'min': last_eval[0][48],
                              'avg': float(last_eval[0][49]),
                              'max': last_eval[0][50]},
                     'G_R': {'min': last_eval[0][51],
                             'avg': float(last_eval[0][52]),
                             'max': last_eval[0][53]},
                     }}

    return results


def get_last_meta_eval_holder(holder, portal, method):
    try:
        if portal == "data.europa.eu" or portal == "dati.gov.it" or portal == "default":

            sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                            MIN(F2), AVG(F2), MAX(F2),
                            MIN(F3), AVG(F3), MAX(F3),
                            MIN(F4), AVG(F4), MAX(F4),
                            MIN(G_F), AVG(G_F), MAX(G_F),
                            MIN(A1), AVG(A1), MAX(A1),
                            MIN(`A1.1`), AVG(`A1.1`), MAX(`A1.1`),
                            MIN(`A1.2`), AVG(`A1.2`), MAX(`A1.2`),
                            MIN(G_A), AVG(G_A), MAX(G_A),
                            MIN(I1), AVG(I1), MAX(I1),
                            MIN(I2), AVG(I2), MAX(I2),
                            MIN(I3), AVG(I3), MAX(I3),
                            MIN(G_I), AVG(G_I), MAX(G_I),
                            MIN(R1), AVG(R1), MAX(R1),
                            MIN(`R1.1`), AVG(`R1.1`), MAX(`R1.1`),
                            MIN(`R1.2`), AVG(`R1.2`), MAX(`R1.2`),
                            MIN(`R1.3`), AVG(`R1.3`), MAX(`R1.3`),
                            MIN(G_R), AVG(G_R), MAX(G_R)
                    FROM Metadata as val
                    INNER JOIN Dataset as ds
                    ON val.idDataset = ds.id
                    AND ds.holder = %s
                    AND val.method = %s
                    AND val.portal = %s"""

            # `Metadata`.`F1`,
            #         `Metadata`.`F2`,
            #         `Metadata`.`F3`,
            #         `Metadata`.`F4`,
            #         `Metadata`.`G_F`,
            #         `Metadata`.`A1`,
            #         `Metadata`.`A1.1`,
            #         `Metadata`.`A1.2`,
            #         `Metadata`.`A2`,
            #         `Metadata`.`G_A`,
            #         `Metadata`.`I1`,
            #         `Metadata`.`I2`,
            #         `Metadata`.`I3`,
            #         `Metadata`.`G_I`,
            #         `Metadata`.`R1`,
            #         `Metadata`.`R1.1`,
            #         `Metadata`.`R1.2`,
            #         `Metadata`.`R1.3`,
            #         `Metadata`.`G_R`
            #         FROM `euFAIR`.`Metadata`
            #         WHERE idDataset = %s
            #         AND method = %s
            #         AND portal= %s
            #         ORDER BY datetime DESC
            #         LIMIT 10"""

            parameter = (holder, method, portal)
            cursor_object.execute(sql, parameter)

            last_eval = cursor_object.fetchall()

        else:
            sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                            MIN(F2), AVG(F2), MAX(F2),
                            MIN(F3), AVG(F3), MAX(F3),
                            MIN(F4), AVG(F4), MAX(F4),
                            MIN(G_F), AVG(G_F), MAX(G_F),
                            MIN(A1), AVG(A1), MAX(A1),
                            MIN(A1.1), AVG(A1.1), MAX(A1.1),
                            MIN(A1.2), AVG(A1.2), MAX(A1.2),
                            MIN(G_A), AVG(G_A), MAX(G_A),
                            MIN(I1), AVG(I1), MAX(I1),
                            MIN(I2), AVG(I2), MAX(I2),
                            MIN(I3), AVG(I3), MAX(I3),
                            MIN(G_I), AVG(G_I), MAX(G_I),
                            MIN(R1), AVG(R1), MAX(R1),
                            MIN(R1.1), AVG(R1.1), MAX(R1.1),
                            MIN(R1.2), AVG(R1.2), MAX(R1.2),
                            MIN(R1.3), AVG(R1.3), MAX(R1.3),
                            MIN(G_R), AVG(G_R), MAX(G_R)
                    FROM Metadata as val
                    INNER JOIN Dataset as ds
                    ON val.idDataset = ds.id
                    AND ds.holder = %s
                    AND val.method = %s
                    AND NOT val.portal 'data.europa.eu'
                    AND NOT val.portal 'dati.gov.it'"""

            parameter = (holder, method, portal)

            cursor_object.execute(sql, parameter)

            last_eval = cursor_object.fetchall()[0]
            last_eval = np.array(last_eval).reshape(1, -1)

        print(last_eval[0])


        results = {'F':{'F1': {'min': last_eval[0][0],
                          'avg': float(last_eval[0][1]),
                          'max': last_eval[0][2]},
                   'F2': {'min': last_eval[0][3],
                          'avg': float(last_eval[0][4]),
                          'max': last_eval[0][5]},
                   'F3': {'min': last_eval[0][6],
                          'avg': float(last_eval[0][7]),
                          'max': last_eval[0][8]},
                   'F4': {'min': last_eval[0][9],
                          'avg': float(last_eval[0][10]),
                          'max': last_eval[0][11]},
                   'G_F': {'min': last_eval[0][12],
                          'avg': float(last_eval[0][13]),
                          'max': last_eval[0][14]}},
                   'A':{'A1': {'min': last_eval[0][15],
                          'avg': float(last_eval[0][16]),
                          'max': last_eval[0][17]},
                   'A1.1': {'min': last_eval[0][18],
                          'avg': float(last_eval[0][19]),
                          'max': last_eval[0][20]},
                   'A1.2': {'min': last_eval[0][21],
                          'avg': float(last_eval[0][22]),
                          'max': last_eval[0][23]},
                   'G_A': {'min': last_eval[0][24],
                          'avg': float(last_eval[0][25]),
                          'max': last_eval[0][26]}},
                   'I': {'I1': {'min': last_eval[0][27],
                          'avg': float(last_eval[0][28]),
                          'max': last_eval[0][29]},
                   'I2': {'min': last_eval[0][30],
                          'avg': float(last_eval[0][31]),
                          'max': last_eval[0][32]},
                   'I3': {'min': last_eval[0][33],
                          'avg': float(last_eval[0][34]),
                          'max': last_eval[0][35]},
                   'G_I': {'min': last_eval[0][36],
                          'avg': float(last_eval[0][37]),
                          'max': last_eval[0][38]}},
                  'R':{'R1': {'min': last_eval[0][39],
                          'avg': float(last_eval[0][40]),
                          'max': last_eval[0][41]},
                   'R1.1': {'min': last_eval[0][42],
                          'avg': float(last_eval[0][43]),
                          'max': last_eval[0][44]},
                   'R1.2': {'min': last_eval[0][45],
                          'avg': float(last_eval[0][46]),
                          'max': last_eval[0][47]},
                   'R1.3': {'min': last_eval[0][48],
                          'avg': float(last_eval[0][49]),
                          'max': last_eval[0][50]},
                   'G_R': {'min': last_eval[0][51],
                          'avg': float(last_eval[0][52]),
                          'max': last_eval[0][53]},
                   }}

    except:
        results = None


    return results


def get_last_data_eval_holder(holder, method):

    sql = """SELECT MIN(F1), AVG(F1), MAX(F1),
                    MIN(F2), AVG(F2), MAX(F2),
                    MIN(F3), AVG(F3), MAX(F3),
                    MIN(F4), AVG(F4), MAX(F4),
                    MIN(G_F), AVG(G_F), MAX(G_F),
                    MIN(A1), AVG(A1), MAX(A1),
                    MIN(`A1.1`), AVG(`A1.1`), MAX(`A1.1`),
                    MIN(`A1.2`), AVG(`A1.2`), MAX(`A1.2`),
                    MIN(G_A), AVG(G_A), MAX(G_A),
                    MIN(I1), AVG(I1), MAX(I1),
                    MIN(I2), AVG(I2), MAX(I2),
                    MIN(I3), AVG(I3), MAX(I3),
                    MIN(G_I), AVG(G_I), MAX(G_I),
                    MIN(R1), AVG(R1), MAX(R1),
                    MIN(`R1.1`), AVG(`R1.1`), MAX(`R1.1`),
                    MIN(`R1.2`), AVG(`R1.2`), MAX(`R1.2`),
                    MIN(`R1.3`), AVG(`R1.3`), MAX(`R1.3`),
                    MIN(G_R), AVG(G_R), MAX(G_R)
            FROM Metadata as val
            INNER JOIN Dataset as ds
            ON val.idDataset = ds.id
            AND ds.holder = %s
            AND val.method = %s"""

    param = (holder, method)

    cursor_object.execute(sql, param)

    last_eval = cursor_object.fetchall()

    results = {'F': {'F1': {'min': last_eval[0][0],
                            'avg': float(last_eval[0][1]),
                            'max': last_eval[0][2]},
                     'F2': {'min': last_eval[0][3],
                            'avg': float(last_eval[0][4]),
                            'max': last_eval[0][5]},
                     'F3': {'min': last_eval[0][6],
                            'avg': float(last_eval[0][7]),
                            'max': last_eval[0][8]},
                     'F4': {'min': last_eval[0][9],
                            'avg': float(last_eval[0][10]),
                            'max': last_eval[0][11]},
                     'G_F': {'min': last_eval[0][12],
                             'avg': float(last_eval[0][13]),
                             'max': last_eval[0][14]}},
               'A': {'A1': {'min': last_eval[0][15],
                            'avg': float(last_eval[0][16]),
                            'max': last_eval[0][17]},
                     'A1.1': {'min': last_eval[0][18],
                              'avg': float(last_eval[0][19]),
                              'max': last_eval[0][20]},
                     'A1.2': {'min': last_eval[0][21],
                              'avg': float(last_eval[0][22]),
                              'max': last_eval[0][23]},
                     'G_A': {'min': last_eval[0][24],
                             'avg': float(last_eval[0][25]),
                             'max': last_eval[0][26]}},
               'I': {'I1': {'min': last_eval[0][27],
                            'avg': float(last_eval[0][28]),
                            'max': last_eval[0][29]},
                     'I2': {'min': last_eval[0][30],
                            'avg': float(last_eval[0][31]),
                            'max': last_eval[0][32]},
                     'I3': {'min': last_eval[0][33],
                            'avg': float(last_eval[0][34]),
                            'max': last_eval[0][35]},
                     'G_I': {'min': last_eval[0][36],
                             'avg': float(last_eval[0][37]),
                             'max': last_eval[0][38]}},
               'R': {'R1': {'min': last_eval[0][39],
                            'avg': float(last_eval[0][40]),
                            'max': last_eval[0][41]},
                     'R1.1': {'min': last_eval[0][42],
                              'avg': float(last_eval[0][43]),
                              'max': last_eval[0][44]},
                     'R1.2': {'min': last_eval[0][45],
                              'avg': float(last_eval[0][46]),
                              'max': last_eval[0][47]},
                     'R1.3': {'min': last_eval[0][48],
                              'avg': float(last_eval[0][49]),
                              'max': last_eval[0][50]},
                     'G_R': {'min': last_eval[0][51],
                             'avg': float(last_eval[0][52]),
                             'max': last_eval[0][53]},
                     }}

    return results


def get_name(value, mode):
    if mode =='dataset':
        if value == "default":
            return "default"

        sql = """SELECT DISTINCT fileName
                FROM Data
                WHERE idDataset = %s"""

    elif mode == 'holder':
        sql = """SELECT DISTINCT fileName
                        FROM Data as val
                        INNER JOIN Dataset as ds
                        ON val.idDataset = ds.id
                        AND ds.holder = %s"""

    parameter = (value,)

    cursor_object.execute(sql, parameter)
    results = cursor_object.fetchall()

    file_list = []

    print(results)
    for el in results:
        file_list.append(el[0])


    return file_list


def get_holder_meta_average(holder_name):
    sql = """SELECT AVG(val.F1), AVG(val.F2), AVG(val.F3), AVG(val.F4), AVG(val.G_F), AVG(val.A1), AVG(val.`A1.1`),
        AVG(val.`A1.2`), AVG(val.A2), AVG(val.G_A), AVG(val.I1), AVG(val.I2), AVG(val.I3), AVG(val.G_I),
        AVG(val.R1), AVG(val.`R1.1`), AVG(val.`R1.2`), AVG(val.`R1.3`), AVG(val.G_R)
        FROM Metadata as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.idDataset
        AND ds.holderDataset = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def get_holder_meta_min(holder_name):
    sql = """SELECT MIN(val.F1), MIN(val.F2), MIN(val.F3), MIN(val.F4), MIN(val.G_F), MIN(val.A1), MIN(val.`A1.1`),
        MIN(val.`A1.2`), MIN(val.A2), MIN(val.G_A), MIN(val.I1), MIN(val.I2), MIN(val.I3), MIN(val.G_I),
        MIN(val.R1), MIN(val.`R1.1`), MIN(val.`R1.2`), MIN(val.`R1.3`), MIN(val.G_R)
        FROM Metadata as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.idDataset
        AND ds.holderDataset = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def get_holder_meta_max(holder_name):
    sql = """SELECT MAX(val.F1), MAX(val.F2), MAX(val.F3), MAX(val.F4), MAX(val.G_F), MAX(val.A1), MAX(val.`A1.1`),
        MAX(val.`A1.2`), MAX(val.A2), MAX(val.G_A), MAX(val.I1), MAX(val.I2), MAX(val.I3), MAX(val.G_I),
        MAX(val.R1), MAX(val.`R1.1`), MAX(val.`R1.2`), MAX(val.`R1.3`), MAX(val.G_R)
        FROM Metadata as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.idDataset
        AND ds.holderDataset = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def get_holder_data_average(holder_name):
    sql = """SELECT AVG(val.F1), AVG(val.F2), AVG(val.F3), AVG(val.F4), AVG(val.G_F), AVG(val.A1), AVG(val.`A1.1`),
        AVG(val.`A1.2`), AVG(val.A2), AVG(val.G_A), AVG(val.I1), AVG(val.I2), AVG(val.I3), AVG(val.G_I),
        AVG(val.R1), AVG(val.`R1.1`), AVG(val.`R1.2`), AVG(val.`R1.3`), AVG(val.G_R)
        FROM Data as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.idDataset
        AND ds.holderDataset = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def get_holder_data_min(holder_name):
    sql = """SELECT MIN(val.F1), MIN(val.F2), MIN(val.F3), MIN(val.F4), MIN(val.G_F), MIN(val.A1), MIN(val.`A1.1`),
        MIN(val.`A1.2`), MIN(val.A2), MIN(val.G_A), MIN(val.I1), MIN(val.I2), MIN(val.I3), MIN(val.G_I),
        MIN(val.R1), MIN(val.`R1.1`), MIN(val.`R1.2`), MIN(val.`R1.3`), MIN(val.G_R)
        FROM Data as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.idDataset
        AND ds.holderDataset = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def get_holder_data_max(holder_name):
    sql = """SELECT MAX(val.F1), MAX(val.F2), MAX(val.F3), MAX(val.F4), MAX(val.G_F), MAX(val.A1), MAX(val.`A1.1`),
        MAX(val.`A1.2`), MAX(val.A2), MAX(val.G_A), MAX(val.I1), MAX(val.I2), MAX(val.I3), MAX(val.G_I),
        MAX(val.R1), MAX(val.`R1.1`), MAX(val.`R1.2`), MAX(val.`R1.3`), MAX(val.G_R)
        FROM Data as val
        INNER JOIN Dataset as ds
        ON val.idDataset = ds.id
        AND ds.holder = %s"""

    param = (holder_name[7:],)

    cursor_object.execute(sql, param)

    return cursor_object.fetchall()


def clear_for_close():
    query = "SELECT COUNT(*) FROM information_schema.processlist WHERE `info` LIKE '%INSERT%' OR `info` LIKE " \
            "'%UPDATE%' OR `info` LIKE '%DELETE%'"
    cursor_object.execute(query)
    result = cursor_object.fetchone()

    if result and result[0] > 0:
        return True
    else:
        return False


class IntegrityError(Exception):
    pass


# get_last_meta_eval('cfed2839-1274-4ea9-b4f9-d1016fa87a14','dati.gov.it', 'merged')

# cursor_object.execute("""SELECT * FROM euFAIR.Data WHERE idDataset = '2e68ecef-7353-46fd-b29f-a31b3d37ae01' """)
#
# print(cursor_object.fetchmany(2))

    # 256ce373-6ed3-41f3-8984-190ad1ce1226
# 2e68ecef-7353-46fd-b29f-a31b3d37ae01

# cursor = my_database.cursor()
#
# # Esecuzione della query
# cursor.execute("SELECT * FROM Data LIMIT 1")
#
# # Ottenere i nomi delle colonne
# column_names = [column[0] for column in cursor.description]
#
# # Stampa dei nomi delle colonne
# for column_name in column_names:
#     print(column_name)
