import runtime.database.functions


def initialize(arguments, database_path):
    runtime.database.functions.create_database(database_path)
    if arguments.client and arguments.target:
        (arguments.target_name,
         arguments.host,
         arguments.port,
         arguments.public,
         arguments.certificate) = runtime.database.retrieve_target(
            target_name=arguments.target,
            database_path=database_path)
    return arguments
