import nox

#nox.options.reuse_existing_virtualenvs = True
nox.options.sessions = ['build']  # default session
nox.options.stop_on_first_error = True

BUILD_CFG = 'pelicanconf.py'
PUBLISH_CFG = 'publishconf.py'

@nox.session
def build(session):
    """ Build local version of site """
    session.install('-r', 'requirements.txt')
    session.run('pelican', '-s', BUILD_CFG, *session.posargs)

@nox.session
def rebuild(session):
    """ `build` with the delete switch """
    session.install('-r', 'requirements.txt')
    session.run('pelican', '-d', '-s', BUILD_CFG, *session.posargs)

@nox.session
def serve(session):
    """ Build the site and then serve it locally, watching for changes """
    session.install('-r', 'requirements.txt')
    session.run('pelican', '-s', BUILD_CFG, *session.posargs)
    session.run('pelican', '-lr', '-s', BUILD_CFG)

@nox.session
def publish(session):
    """ Build published version of site """
    session.install('-r', 'requirements.txt')
    session.run('pelican', '-s', PUBLISH_CFG, *session.posargs)
