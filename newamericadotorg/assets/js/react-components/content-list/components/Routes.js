import { Route } from 'react-router-dom';
import SiteFilter from './SiteFilter';
import ProgramSubRoutes from './ProgramSubRoutes';
import ProgramFilter from './ProgramFilter';

export const PublicationDefault = ({...rest}) => (
  <Route {...rest} render={(props)=>(
    <SiteFilter {...props}
      programId={new URLSearchParams(props.location.search).get('program_id')}
      contentType={{slug: 'publications', api_name:'', name:'Publications', title:'Publications'}} />
  )}/>
);

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

export const ProgramPublicationDefault = ({program, programId, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <ProgramFilter {...props}
      projectId={new URLSearchParams(props.location.search).get('project_id')}
      programId={programId}
      program={program}
      contentType={{slug: 'publications', api_name:'', name:'Publications', title:'Publications'}} />
  )}/>
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
