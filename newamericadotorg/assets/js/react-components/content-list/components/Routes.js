import { Route } from 'react-router-dom';
import SiteFilter from './SiteFilter';
import ProgramSubRoutes from './ProgramSubRoutes';
import ProgramFilter from './ProgramFilter';
import ProjectFilter from './ProjectFilter';
import ProjectSubRoutes from './ProjectSubRoutes';

export const ContentType = ({contentType, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <SiteFilter {...rest} {...props}
      programId={new URLSearchParams(props.location.search).get('program_id')}
      contentType={contentType} />
  )}/>
);

export const Program = ({program, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProgramSubRoutes {...props} programId={program.id} />
  )} />
);

export const ProgramContentType = ({contentType, programId, program, ...rest}) => (
  <Route {...rest} render={(props)=>(
      <ProgramFilter {...props}
        projectId={new URLSearchParams(props.location.search).get('project_id')}
        programId={programId}
        program={program}
        contentType={contentType} />
    )}/>
);

export const Project = ({contentType, projectId, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProjectSubRoutes {...props} projectId={projectId} />
  )}/>
);

export const ProjectContentType = ({contentType, projectId, project, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProjectFilter {...props}
      project={project}
      projectId={project.id}
      contentType={contentType}
    />
  )}/>
);
