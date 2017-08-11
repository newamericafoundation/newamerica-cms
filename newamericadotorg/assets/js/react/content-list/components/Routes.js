/**
  Dynamic routes based on
  - sitewide contentTypes and programs data pulled from API
  - a program's contentTypes
    (programs select which contentTypes they use,
    and rename default slugs, so this is also dyanmic)
  - a program's projects and that project's contentTypes
    (projects can also choose contentTypes and rename slugs)
**/

import { Route, Switch } from 'react-router-dom';
import SiteFilter from './SiteFilter';
import ProgramFilter from './ProgramFilter';
import ProjectFilter from './ProjectFilter';
import AuthorFilter from './AuthorFilter';
import ProgramIndex from './ProgramIndex';
import ProjectIndex from './ProjectIndex';

export const IndexContentTypeRoute = ({contentType, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <SiteFilter {...rest} {...props}
      programId={new URLSearchParams(props.location.search).get('program_id')}
      before={new URLSearchParams(props.location.search).get('before')}
      after={new URLSearchParams(props.location.search).get('after')}
      contentType={contentType} />
  )}/>
);

export const ProgramRoute = ({program, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProgramIndex {...props} programId={program.id} />
  )} />
);

export const AuthorRoute = (rest) => (
  <Route {...rest} render={(props)=>(
    <AuthorFilter {...props}
      contentTypeAPIName={new URLSearchParams(props.location.search).get('publication_type')} />
  )} />
);

export const ProgramContentTypeRoute = ({contentType, program, ...rest}) => (
  <Route {...rest} render={(props)=>(
      <ProgramFilter {...props}
        projectId={new URLSearchParams(props.location.search).get('project_id')}
        before={new URLSearchParams(props.location.search).get('before')}
        after={new URLSearchParams(props.location.search).get('after')}
        programId={program.id}
        program={program}
        contentType={contentType} />
    )}/>
);

export const ProjectRoute = ({projectId, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProjectIndex {...props} projectId={projectId} />
  )}/>
);

export const ProjectContentTypeRoute = ({contentType, project, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProjectFilter {...props}
      project={project}
      projectId={project.id}
      contentType={contentType}
    />
  )}/>
);

// Sitewide Routes `/:contentType/?...` and `/:program`=> ProgramRoutes
export const IndexRoutes = ({contentTypes, programs}) => (
  <Switch>
    <IndexContentTypeRoute path="/publications"
      contentType={{slug: 'publications', api_name:'', name:'Publications', title:''}} />
    {contentTypes.map((c,i)=>(
      <IndexContentTypeRoute path={`/${c.slug}`} contentType={c} />
    ))}
    {programs.map((p,i)=>(
      <ProgramRoute path={`/${p.slug}`} program={p} />
    ))}
    <AuthorRoute path="/our-people/:authorSlug" />
  </Switch>
);

// Routes for ProgramIndex `/:program/:contentType/`
export const ProgramRoutes = ({program}) => (
  <Switch>
    <ProgramContentTypeRoute
      path={`/${program.slug}/publications`}
      contentType={{slug: 'publications', api_name:'', name:'Publications', title:''}}
      program={program} />
    {program.content_types && program.content_types.map((c,i)=>(
      <ProgramContentTypeRoute
        path={c.url}
        contentType={c}
        program={program} />
    ))}
    {program.projects && program.projects.map((p,i)=>(
      <ProjectRoute path={p.url} projectId={p.id} />
    ))}
  </Switch>
);

// Routes for ProjectIndex `/:program/:project/:contentType`
export const ProjectRoutes = ({project}) => (
  <Switch>
    <ProjectContentTypeRoute
      path={`${project.url}publications`}
      contentType={{slug: 'publications', api_name:'', name:'Publications', title: ''}}
      project={project} />
    {project.content_types && project.content_types.map((c,i)=>(
      <ProjectContentTypeRoute
        path={c.url}
        contentType={c}
        project={project} />
    ))}
  </Switch>
);
