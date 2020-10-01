from invoke import run as local
from invoke.exceptions import Exit
from invoke.tasks import task

PRODUCTION_APP_INSTANCE = "newamericadotorg"
STAGING_APP_INSTANCE = "na-staging"

LOCAL_MEDIA_FOLDER = "/vagrant/media"
LOCAL_IMAGES_FOLDER = "/vagrant/media/original_images"
LOCAL_DATABASE_NAME = "newamerica-cms"


############
# Production
############


@task
def pull_production_media(c):
    """Pull media from production AWS S3"""
    pull_media_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_data(c):
    """Pull database from production Heroku Postgres"""
    pull_database_from_heroku(c, PRODUCTION_APP_INSTANCE)


@task
def production_shell(c):
    """Spin up a one-time Heroku production dyno and connect to shell"""
    open_heroku_shell(c, PRODUCTION_APP_INSTANCE)


@task
def pull_production_images(c):
    """Pull images from production AWS S3"""
    pull_images_from_s3_heroku(c, PRODUCTION_APP_INSTANCE)


#########
# Staging
#########


@task
def pull_staging_media(c):
    """Pull media from staging AWS S3"""
    pull_media_from_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_data(c):
    """Pull database from staging Heroku Postgres"""
    pull_database_from_heroku(c, STAGING_APP_INSTANCE)


@task
def staging_shell(c):
    """Spin up a one-time Heroku staging dyno and connect to shell"""
    open_heroku_shell(c, STAGING_APP_INSTANCE)


@task
def push_staging_media(c):
    """Push local media content to staging isntance"""
    push_media_to_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def pull_staging_images(c):
    """Pull images from staging AWS S3"""
    pull_images_from_s3_heroku(c, STAGING_APP_INSTANCE)


@task
def sync_staging_from_production(c):
    """Copy database from production to staging"""
    copy_heroku_database(
        c,
        destination=STAGING_APP_INSTANCE,
        source=PRODUCTION_APP_INSTANCE,
    )
    sync_heroku_buckets(
        c,
        destination=STAGING_APP_INSTANCE,
        source=PRODUCTION_APP_INSTANCE,
        folders=['original_images', 'documents']
    )
    # The above command just syncs the original images, so we need to
    # delete the contents of the wagtailimages_renditions table so
    # that the renditions will be re-created when requested in the
    # staging environment.
    delete_staging_renditions(c)


#######
# Local
#######


def delete_local_database(c, local_database_name=LOCAL_DATABASE_NAME):
    local(
        "dropdb --if-exists {database_name}".format(database_name=LOCAL_DATABASE_NAME)
    )


########
# Heroku
########


def check_if_logged_in_to_heroku(c):
    if not local("heroku auth:whoami", warn=True):
        raise Exit(
            'Log-in with the "heroku login -i" command before running this ' "command."
        )


def get_heroku_variable(c, app_instance, variable):
    check_if_logged_in_to_heroku(c)
    return local(
        "heroku config:get {var} --app {app}".format(app=app_instance, var=variable)
    ).stdout.strip()


def pull_media_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "S3_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name, folders=['original_images', 'documents']
    )


def pull_database_from_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    delete_local_database(c)
    local(
        "heroku pg:pull --app {app} DATABASE_URL {local_database}".format(
            app=app_instance, local_database=LOCAL_DATABASE_NAME
        )
    )
    answer = (
        input(
            "Any superuser accounts you previously created locally will"
            " have been wiped. Do you wish to create a new superuser? (Y/n): "
        )
        .strip()
        .lower()
    )
    if not answer or answer == "y":
        local("django-admin createsuperuser", pty=True)


def open_heroku_shell(c, app_instance, shell_command="bash"):
    check_if_logged_in_to_heroku(c)
    local(
        "heroku run --app {app} {command}".format(
            app=app_instance, command=shell_command
        )
    )


# The single star (*) below indicates that all the arguments
# afterwards must be given as keywords.  See PEP 3102 to learn more.
def copy_heroku_database(c, *, source, destination):
    check_if_logged_in_to_heroku(c)
    local(
        "heroku pg:copy {source_app}::DATABASE_URL DATABASE_URL --app {destination_app}".format(
            source_app=source, destination_app=destination
        )
    )


# The single star (*) below indicates that all the arguments
# afterwards must be given as keywords.  See PEP 3102 to learn more.
def sync_heroku_buckets(c, *, source, destination, folders=[]):
    destination_bucket_name = get_heroku_variable(
        c, destination, "S3_BUCKET_NAME"
    )
    if destination_bucket_name == PRODUCTION_APP_INSTANCE:
        raise RuntimeError("Production bucket used as destination for sync_heroku_buckets. Please delete this check if you're absolutely sure you want to do this")
    destination_access_key_id = get_heroku_variable(c, destination, "AWS_ACCESS_KEY_ID")
    destination_secret_access_key = get_heroku_variable(
        c, destination, "AWS_SECRET_ACCESS_KEY"
    )

    source_bucket_name = get_heroku_variable(
        c, source, "S3_BUCKET_NAME"
    )

    # The `--size-only` flag means we don't have to compute the md5
    # hash of every media file, potentially increasing performance
    cmd_template = "s3 sync --size-only --delete s3://{source_bucket_name}/{folder} s3://{destination_bucket_name}/{folder}"
    if folders:
        for folder in folders:
            print('Syncing media folder `{}`. This operation may take a while, and will be interrupted if your computer goes to sleep, is powered off, or loses its connection to the internet.'.format(folder))
            aws_cmd = cmd_template.format(
                source_bucket_name=source_bucket_name,
                destination_bucket_name=destination_bucket_name,
                folder=folder,
            )
            aws(c, aws_cmd, destination_access_key_id, destination_secret_access_key)
    else:
        print('Syncing all media folders. This operation may take a while, and will be interrupted if your computer goes to sleep, is powered off, or loses its connection to the internet.')
        aws_cmd = cmd_template.format(
            source_bucket_name=source_bucket_name,
            destination_bucket_name=destination_bucket_name,
            folder='',
        )
        aws(c, aws_cmd, destination_access_key_id, destination_secret_access_key)


####
# S3
####


def aws(c, command, aws_access_key_id, aws_secret_access_key, **kwargs):
    return local(
        "AWS_ACCESS_KEY_ID={access_key_id} AWS_SECRET_ACCESS_KEY={secret_key} "
        "aws {command}".format(
            access_key_id=aws_access_key_id,
            secret_key=aws_secret_access_key,
            command=command,
        ),
        **kwargs
    )


def pull_media_from_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
    folders=[],
):
    cmd_template = "s3 sync --delete s3://{bucket_name}/{folder} {local_media}"

    if folders:
        for folder in folders:
            aws_cmd = cmd_template.format(
                bucket_name=aws_storage_bucket_name, local_media=local_media_folder,
                folder=folder,
            )
            print('Syncing media folder `{}`. This operation may take a while, and will be interrupted if your computer goes to sleep, is powered off, or loses its connection to the internet.'.format(folder))
            aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)
    else:
        aws_cmd = cmd_template.format(
            bucket_name=aws_storage_bucket_name, local_media=local_media_folder,
            folder='',
        )
        print('Syncing all media folders. This operation may take a while, and will be interrupted if your computer goes to sleep, is powered off, or loses its connection to the internet.')
        aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def push_media_to_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    prompt_msg = (
        "You are about to push your media folder contents to the "
        "S3 bucket. It's a destructive operation. \n"
        'Please type the application name "{app_instance}" to '
        "proceed:\n>>> ".format(app_instance=make_bold(app_instance))
    )
    if input(prompt_msg) != app_instance:
        raise Exit("Aborted")
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "S3_BUCKET_NAME"
    )
    push_media_to_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "S3_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name
    )


def push_media_to_s3(
    c,
    aws_access_key_id,
    aws_secret_access_key,
    aws_storage_bucket_name,
    local_media_folder=LOCAL_MEDIA_FOLDER,
):
    aws_cmd = "s3 sync --delete {local_media} s3://{bucket_name}/".format(
        bucket_name=aws_storage_bucket_name, local_media=local_media_folder
    )
    aws(c, aws_cmd, aws_access_key_id, aws_secret_access_key)


def pull_images_from_s3_heroku(c, app_instance):
    check_if_logged_in_to_heroku(c)
    aws_access_key_id = get_heroku_variable(c, app_instance, "AWS_ACCESS_KEY_ID")
    aws_secret_access_key = get_heroku_variable(
        c, app_instance, "AWS_SECRET_ACCESS_KEY"
    )
    aws_storage_bucket_name = get_heroku_variable(
        c, app_instance, "S3_BUCKET_NAME"
    )
    pull_media_from_s3(
        c, aws_access_key_id, aws_secret_access_key, aws_storage_bucket_name, folders=['original_images']
    )
    # The above command just syncs the original images, so we need to drop the wagtailimages_renditions
    # table so that the renditions will be re-created when requested on the local build.
    delete_local_renditions()


def delete_local_renditions(local_database_name=LOCAL_DATABASE_NAME):
    try:
        local(
            'sudo -u postgres psql  -d {database_name} -c "DELETE FROM images_rendition;"'.format(
                database_name=local_database_name
            )
        )
    except:
        pass

    try:
        local(
            'sudo -u postgres psql  -d {database_name} -c "DELETE FROM wagtailimages_rendition;"'.format(
                database_name=local_database_name
            )
        )
    except:
        pass


def delete_staging_renditions(c):
    check_if_logged_in_to_heroku(c)
    local(
        'heroku pg:psql --app {app} -c "DELETE FROM wagtailimages_rendition;"'.format(
            app=STAGING_APP_INSTANCE
        )
    )


def make_bold(msg):
    return "\033[1m{}\033[0m".format(msg)
