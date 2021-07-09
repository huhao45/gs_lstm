from pyflink.dataset import ExecutionEnvironment
from pyflink.table import TableConfig, DataTypes, BatchTableEnvironment
from pyflink.table.descriptors import Schema, OldCsv, FileSystem



exec_env = ExecutionEnvironment.get_execution_environment()
exec_env.set_parallelism(1)
t_config = TableConfig()
t_env = BatchTableEnvironment.create(exec_env, t_config)


t_env.connect(FileSystem().path('/home/hh/flowpredict/tmp/input')) \
    .with_format(OldCsv()
                 .field('ff', DataTypes.STRING())) \
    .with_schema(Schema()
                 .field('ff', DataTypes.STRING())) \
    .create_temporary_table('mySource')
t_env.connect(FileSystem().path('/home/hh/flowpredict/tmp/output')) \
    .with_format(OldCsv()
                 .field_delimiter('\t')
                 .field('ff', DataTypes.STRING())
                 .field('count', DataTypes.BIGINT())) \
    .with_schema(Schema()
                 .field('ff', DataTypes.STRING())
                 .field('count', DataTypes.BIGINT())) \
    .create_temporary_table('mySink')
t_env.from_path('mySource') \
    .group_by('ff') \
    .select('ff, count(1)') \
    .insert_into('mySink')
t_env.execute("python_job")