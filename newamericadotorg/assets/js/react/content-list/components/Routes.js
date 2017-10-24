/**
  Dynamic routes based on
  - sitewide contentTypes and programs data pulled from API
  - a program's contentTypes
    (programs select which contentTypes they use,
    and rename default slugs, so this is also dyanmic)
  - a program's subprograms and that subprogram's contentTypes
    (subprograms can also choose contentTypes and rename slugs)
**/

import { Route, Switch } from 'react-router-dom';
import SiteFilter from './SiteFilter';
import ProgramFilter from './ProgramFilter';
import SubprogramFilter from './SubprogramFilter';
import AuthorFilter from './AuthorFilter';
import ProgramIndex from './ProgramIndex';
import SubprogramIndex from './SubprogramIndex';

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
        subprogramId={new URLSearchParams(props.location.search).get('subprogram_id')}
        before={new URLSearchParams(props.location.search).get('before')}
        after={new URLSearchParams(props.location.search).get('after')}
        programId={program.id}
        program={program}
        contentType={contentType} />
    )}/>
);

export const SubprogramRoute = ({subprogramId, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <SubprogramIndex {...props} subprogramId={subprogramId} />
  )}/>
);

export const SubprogramContentTypeRoute = ({contentType, subprogram, ...rest}) => (
  <Route {...rest} render={(props)=>(
    <SubprogramFilter {...props}
      subprogram={subprogram}
      subprogramId={subprogram.id}
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
    {program.subprograms && program.subprograms.map((p,i)=>(
      <SubprogramRoute path={p.url} subprogramId={p.id} />
    ))}
  </Switch>
);

// Routes for SubprogramIndex `/:program/:subprogram/:contentType`
export const SubprogramRoutes = ({subprogram}) => (
  <Switch>
    <SubprogramContentTypeRoute
      path={`${subprogram.url}publications`}
      contentType={{slug: 'publications', api_name:'', name:'Publications', title: ''}}
      subprogram={subprogram} />
    {subprogram.content_types && subprogram.content_types.map((c,i)=>(
      <SubprogramContentTypeRoute
        path={c.url}
        contentType={c}
        subprogram={subprogram} />
    ))}
  </Switch>
);
