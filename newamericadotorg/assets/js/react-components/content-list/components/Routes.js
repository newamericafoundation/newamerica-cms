import { Route, Switch } from 'react-router-dom';
import SiteFilter from './SiteFilter';
import ProgramFilter from './ProgramFilter';
import ProjectFilter from './ProjectFilter';
import ProgramIndex from './ProgramIndex';
import ProjectIndex from './ProjectIndex';

export const IndexContentTypeRoute = ({contentType, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <SiteFilter {...rest} {...props}
      programId={new URLSearchParams(props.location.search).get('program_id')}
      contentType={contentType} />
  )}/>
);

export const ProgramRoute = ({program, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProgramIndex {...props} programId={program.id} />
  )} />
);

export const ProgramContentTypeRoute = ({contentType, program, ...rest}) => (
  <Route {...rest} render={(props)=>(
      <ProgramFilter {...props}
        projectId={new URLSearchParams(props.location.search).get('project_id')}
        programId={program.id}
        program={program}
        contentType={contentType} />
    )}/>
);

export const ProjectRoute = ({contentType, projectId, ...rest}) => (
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
  </Switch>
);

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
